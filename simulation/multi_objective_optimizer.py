import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional, Callable
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel
from scipy.optimize import minimize
from scipy.stats import qmc


@dataclass
class ObjectiveResult:
    power_density: float
    cost_euro: float
    lifetime_days: float
    compostability_pct: float


COST_PER_GRAM = {
    'carbon_black': 0.012,
    'graphite': 0.008,
    'cnf': 0.020,
    'laccase': 0.150,
    'abts': 0.060,
    'glucose': 0.005,
    'yeast': 0.003,
}

COST_SCALE = 0.001


def cost_objective(params: np.ndarray) -> float:
    carbon = params[0]
    graphite = params[1]
    yeast = params[2]
    layer_h = params[3]
    laccase = params[4]
    o2 = params[5]
    mediator = params[6]
    layers = params[7]

    volume_cm3 = 2.0 * 0.08 * (layers * layer_h * 1e-4)
    cnf_frac = max(0, 1.0 - (carbon + graphite) / 100.0)

    material_cost = (
        carbon * COST_PER_GRAM['carbon_black']
        + graphite * COST_PER_GRAM['graphite']
        + cnf_frac * 40 * COST_PER_GRAM['cnf']
        + laccase * COST_PER_GRAM['laccase']
        + mediator * COST_PER_GRAM['abts']
        + yeast * COST_PER_GRAM['yeast']
    ) * volume_cm3 * COST_SCALE

    labor = 0.50
    overhead = 0.10

    return material_cost + labor + overhead


def lifetime_objective(params: np.ndarray) -> float:
    carbon = params[0]
    graphite = params[1]
    yeast = params[2]
    laccase = params[4]
    layers = params[7]

    conductivity_factor = 0.3 * (carbon / 5.0) + 0.7 * (graphite / 10.0)
    effective_power = 50.0 * max(conductivity_factor, 0.05) * max(laccase, 0.1)

    daily_consumption_uj = 800.0
    degradation_rate = 0.02

    cum_supply = 0.0
    cum_demand = 0.0
    for day in range(1, 366):
        power_today = effective_power * (1 - degradation_rate / 100) ** day
        cum_supply += power_today * 24 * 3600
        cum_demand += daily_consumption_uj
        if cum_demand > cum_supply:
            return float(day)
    return 365.0


def compostability_objective(params: np.ndarray) -> float:
    carbon = params[0]
    graphite = params[1]
    total_solids = carbon + graphite + 30.0

    bio_fraction = 30.0 / total_solids
    return min(100.0, bio_fraction * 100 * 0.95)


def all_objectives(params: np.ndarray) -> ObjectiveResult:
    from ai_optimizer import evaluate_formulation
    power, _, _, _ = evaluate_formulation(params)
    return ObjectiveResult(
        power_density=power,
        cost_euro=cost_objective(params),
        lifetime_days=lifetime_objective(params),
        compostability_pct=compostability_objective(params),
    )


def all_objectives_fast(params: np.ndarray) -> np.ndarray:
    r = all_objectives(params)
    return np.array([r.power_density, r.cost_euro, r.lifetime_days,
                     r.compostability_pct])


@dataclass
class ParetoResult:
    solutions: List[dict]
    objectives: np.ndarray
    weights_used: np.ndarray

    @property
    def n_solutions(self) -> int:
        return len(self.solutions)

    def plot(self, path: str = "pareto_front.png"):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        if self.n_solutions == 0:
            return

        fig, axes = plt.subplots(2, 3, figsize=(16, 10))
        labels = ['Power (\u00b5W/cm\u00b2)', 'Cost (\u20ac)', 'Lifetime (days)',
                  'Compost (%)']
        pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

        for ax, (i, j) in zip(axes.flatten(), pairs):
            ax.scatter(self.objectives[:, i], self.objectives[:, j],
                       c=self.objectives[:, 0], cmap='viridis', s=40)
            ax.set_xlabel(labels[i])
            ax.set_ylabel(labels[j])
            ax.grid(alpha=0.3)

        plt.suptitle("Multi-Objective Pareto Front", fontsize=14)
        plt.tight_layout()
        plt.savefig(path, dpi=150, bbox_inches='tight')
        plt.close()


def dominates(a: np.ndarray, b: np.ndarray, directions: List[str]) -> bool:
    better_in_all = True
    strictly_better_in_one = False
    for i, d in enumerate(directions):
        if d == 'max':
            if a[i] < b[i]:
                better_in_all = False
            if a[i] > b[i]:
                strictly_better_in_one = True
        else:
            if a[i] > b[i]:
                better_in_all = False
            if a[i] < b[i]:
                strictly_better_in_one = True
    return better_in_all and strictly_better_in_one


def pareto_filter(objectives: np.ndarray, directions: List[str]) -> np.ndarray:
    n = len(objectives)
    is_pareto = np.ones(n, dtype=bool)
    for i in range(n):
        if not is_pareto[i]:
            continue
        for j in range(n):
            if i == j or not is_pareto[j]:
                continue
            if dominates(objectives[j], objectives[i], directions):
                is_pareto[i] = False
                break
    return is_pareto


class MultiObjectiveOptimizer:
    DIRECTIONS = ['max', 'min', 'max', 'max']

    def __init__(self, bounds: np.ndarray, objective_fn: Callable = None,
                 n_weight_samples: int = 30, n_bo_iterations: int = 30,
                 seed: int = 42):
        self.bounds = bounds
        self.dim = bounds.shape[0]
        self.n_objectives = 4
        self.n_weight_samples = n_weight_samples
        self.n_bo_iterations = n_bo_iterations
        self.seed = seed
        self.objective_fn = objective_fn or all_objectives_fast

    def _sample_weights(self) -> np.ndarray:
        rng = np.random.RandomState(self.seed)
        return rng.dirichlet(np.ones(self.n_objectives), size=self.n_weight_samples)

    def _scalarized_objective(self, params: np.ndarray, weights: np.ndarray) -> float:
        raw = self.objective_fn(params)
        obj = np.zeros(self.n_objectives)
        for i, d in enumerate(self.DIRECTIONS):
            if d == 'min':
                obj[i] = -raw[i]
            else:
                obj[i] = raw[i]
        return -float(np.dot(weights, obj))

    def optimize(self) -> ParetoResult:
        weights = self._sample_weights()
        all_solutions = []
        all_objectives_raw = []

        for w in weights:
            rng = np.random.RandomState(self.seed)
            for _ in range(self.n_bo_iterations):
                x0 = rng.uniform(self.bounds[:, 0], self.bounds[:, 1])
                try:
                    res = minimize(
                        lambda x: self._scalarized_objective(x, w),
                        x0, method='L-BFGS-B',
                        bounds=self.bounds,
                        options={'maxiter': 50}
                    )
                    if res.success or res.fun < 0:
                        raw = self.objective_fn(res.x)
                        all_solutions.append({'params': res.x.copy()})
                        all_objectives_raw.append(raw)
                except Exception:
                    pass

        if not all_solutions:
            return ParetoResult(solutions=[], objectives=np.empty((0, 4)),
                                weights_used=weights)

        all_obj = np.array(all_objectives_raw)
        mask = pareto_filter(all_obj, self.DIRECTIONS)

        return ParetoResult(
            solutions=[s for s, m in zip(all_solutions, mask) if m],
            objectives=all_obj[mask],
            weights_used=weights,
        )

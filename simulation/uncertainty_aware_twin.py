import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional, Callable
from sklearn.ensemble import RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel


@dataclass
class PredictionResult:
    mean: np.ndarray
    std: np.ndarray
    lower_95: np.ndarray
    upper_95: np.ndarray
    samples: np.ndarray = field(repr=False)

    @property
    def n_samples(self) -> int:
        return self.samples.shape[0]

    @property
    def n_outputs(self) -> int:
        if self.mean.ndim == 1:
            return 1
        return self.mean.shape[-1]

    @property
    def n_points(self) -> int:
        if self.mean.ndim == 1:
            return 1
        return self.mean.shape[0]

    @staticmethod
    def from_samples(samples: np.ndarray, confidence: float = 0.95) -> 'PredictionResult':
        alpha = 1.0 - confidence
        mean = np.mean(samples, axis=0)
        std = np.std(samples, axis=0)
        lower = np.percentile(samples, alpha / 2 * 100, axis=0)
        upper = np.percentile(samples, (1 - alpha / 2) * 100, axis=0)
        return PredictionResult(mean=mean, std=std, lower_95=lower,
                                 upper_95=upper, samples=samples)

    def confidence_width(self, output_idx: int = 0) -> float:
        return float(self.upper_95[output_idx] - self.lower_95[output_idx])

    def plot(self, path: str = "uncertainty.png", output_names: List[str] = None):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        n_out = self.n_outputs
        if self.mean.ndim == 1:
            self_mean = self.mean.reshape(1, -1)
            self_std = self.std.reshape(1, -1)
        else:
            self_mean = self.mean
            self_std = self.std

        n_points = self_mean.shape[0] if self_mean.ndim > 1 else 1
        cols = min(n_out, 4)
        rows = max(1, (n_out + cols - 1) // cols)
        fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
        if n_out == 1 and rows == 1 and cols == 1:
            axes = np.array([[axes]])
        elif rows == 1:
            axes = np.array([axes])
        elif cols == 1:
            axes = np.array([[a] for a in axes])
        axes = axes.flatten()

        for i, ax in enumerate(axes):
            if i >= n_out:
                ax.set_visible(False)
                continue
            x = np.arange(n_points)
            name = output_names[i] if output_names and i < len(output_names) else f"Output {i}"
            yerr = self_std[:, i] * 1.96 if n_points > 1 else self_std[0, i] * 1.96
            y = self_mean[:, i] if n_points > 1 else np.array([self_mean[0, i]])
            ax.bar(x, y, yerr=np.array([yerr]) if n_points == 1 else yerr,
                   color='#3498db', alpha=0.7, capsize=3)
            ax.set_xlabel("Configuration")
            ax.set_ylabel(name)
            ax.set_title(f"{name} (mean +/- 95% CI)")
            ax.grid(alpha=0.3, axis='y')

        plt.suptitle("Uncertainty-Aware Digital Twin Predictions", fontsize=14)
        plt.tight_layout()
        plt.savefig(path, dpi=150, bbox_inches='tight')
        plt.close()


class UncertainDigitalTwin:
    def __init__(self, evaluate_fn: Callable, bounds: np.ndarray,
                 n_ensembles: int = 100, n_train_samples: int = 100,
                 seed: int = 42):
        self.evaluate_fn = evaluate_fn
        self.bounds = bounds
        self.dim = bounds.shape[0]
        self.n_ensembles = n_ensembles
        self.n_train_samples = n_train_samples
        self.seed = seed
        self._rf_models = []
        self._n_outputs = None
        self._trained = False

    def fit(self, X_obs: Optional[np.ndarray] = None):
        rng = np.random.RandomState(self.seed)

        if X_obs is None:
            X_obs = rng.uniform(self.bounds[:, 0], self.bounds[:, 1],
                                 (self.n_train_samples, self.dim))

        y_obs = np.array([self.evaluate_fn(x) for x in X_obs])
        if y_obs.ndim == 1:
            y_obs = y_obs.reshape(-1, 1)

        self._n_outputs = y_obs.shape[1]
        self._rf_models = []

        for output_idx in range(self._n_outputs):
            rf = RandomForestRegressor(
                n_estimators=self.n_ensembles,
                max_depth=None,
                min_samples_leaf=2,
                bootstrap=True,
                random_state=self.seed,
                n_jobs=-1,
            )
            rf.fit(X_obs, y_obs[:, output_idx])
            self._rf_models.append(rf)

        self._trained = True
        return self

    def predict(self, X: np.ndarray, n_samples: int = 1000) -> PredictionResult:
        if X.ndim == 1:
            X = X.reshape(1, -1)

        n_points = X.shape[0]
        n_trees = len(self._rf_models[0].estimators_)

        tree_predictions = []
        for output_idx, rf in enumerate(self._rf_models):
            preds = np.array([tree.predict(X) for tree in rf.estimators_])
            tree_predictions.append(preds)

        if n_samples <= n_trees:
            indices = np.arange(n_samples)
        else:
            rng = np.random.RandomState(self.seed + 1)
            indices = rng.choice(n_trees, size=n_samples, replace=True)

        combined = np.zeros((n_points, n_samples, self._n_outputs))
        for output_idx in range(self._n_outputs):
            combined[:, :, output_idx] = tree_predictions[output_idx][indices].T

        means = combined.mean(axis=1)
        stds = combined.std(axis=1)
        lowers = np.percentile(combined, 2.5, axis=1)
        uppers = np.percentile(combined, 97.5, axis=1)

        return PredictionResult(
            mean=means,
            std=stds,
            lower_95=lowers,
            upper_95=uppers,
            samples=combined.reshape(n_points * n_samples, self._n_outputs),
        )

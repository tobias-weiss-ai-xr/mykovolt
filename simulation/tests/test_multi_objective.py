import os
import numpy as np
import pytest


def _make_params(carbon=5.0, graphite=10.0, yeast=1.0, layer_h=100.0,
                laccase=1.0, o2=1.0, mediator=20.0, layers=7.0):
    return np.array([carbon, graphite, yeast, layer_h, laccase, o2, mediator, layers])


def _cheap_objectives(params):
    return np.array([
        params[0] * 2 + params[1],
        (params[0] + params[1]) * 0.01,
        params[0] * 0.5 + 5,
        100 - params[0],
    ])


class TestObjectiveFunctions:

    def test_cost_model_defaults(self):
        from multi_objective_optimizer import cost_objective
        p = _make_params()
        c = cost_objective(p)
        assert 0 < c < 2.0
        assert isinstance(c, float)

    def test_cost_model_scales_with_carbon(self):
        from multi_objective_optimizer import cost_objective
        p_low = _make_params(carbon=1.0)
        p_high = _make_params(carbon=15.0)
        assert cost_objective(p_low) < cost_objective(p_high)

    def test_lifetime_model_returns_positive(self):
        from multi_objective_optimizer import lifetime_objective
        p = _make_params()
        lt = lifetime_objective(p)
        assert lt > 0
        assert isinstance(lt, float)

    def test_lifetime_increases_with_power(self):
        from multi_objective_optimizer import lifetime_objective
        p_low = _make_params(carbon=0.5, graphite=1.0, laccase=0.1)
        p_high = _make_params(carbon=14.0, graphite=24.0, laccase=10.0)
        lt_low = lifetime_objective(p_low)
        lt_high = lifetime_objective(p_high)
        assert lt_high >= lt_low

    def test_compostability_returns_pct(self):
        from multi_objective_optimizer import compostability_objective
        p = _make_params()
        c = compostability_objective(p)
        assert 0 <= c <= 100

    def test_compostability_decreases_with_more_carbon(self):
        from multi_objective_optimizer import compostability_objective
        p_low = _make_params(carbon=1.0)
        p_high = _make_params(carbon=15.0)
        assert compostability_objective(p_low) > compostability_objective(p_high)

    def test_all_objectives_returns_result(self):
        from multi_objective_optimizer import all_objectives
        p = _make_params()
        r = all_objectives(p)
        assert hasattr(r, 'power_density')
        assert hasattr(r, 'cost_euro')
        assert hasattr(r, 'lifetime_days')
        assert hasattr(r, 'compostability_pct')
        assert r.power_density > 0


class TestParetoFront:

    def test_pareto_result_structure(self):
        from multi_objective_optimizer import ParetoResult
        pf = ParetoResult(
            solutions=[{'params': np.array([1, 2, 3, 4, 5, 6, 7, 8])}],
            objectives=np.array([[10.0, 0.5, 30.0, 60.0]]),
            weights_used=np.array([[0.25, 0.25, 0.25, 0.25]]),
        )
        assert pf.n_solutions == 1
        assert pf.objectives.shape == (1, 4)

    def test_dominates_simple(self):
        from multi_objective_optimizer import ParetoResult, dominates
        a = np.array([10.0, 0.5, 30.0, 60.0])
        b = np.array([8.0, 0.6, 30.0, 60.0])
        assert dominates(a, b, directions=['max', 'min', 'max', 'max'])

    def test_not_dominates(self):
        from multi_objective_optimizer import dominates
        a = np.array([10.0, 0.5, 30.0, 60.0])
        b = np.array([8.0, 0.6, 40.0, 60.0])
        assert not dominates(a, b, ['max', 'min', 'max', 'max'])

    def test_pareto_filter(self):
        from multi_objective_optimizer import pareto_filter
        objectives = np.array([
            [10.0, 0.5, 30.0, 60.0],
            [8.0, 0.6, 25.0, 60.0],
            [12.0, 0.7, 35.0, 50.0],
        ])
        mask = pareto_filter(objectives, ['max', 'min', 'max', 'max'])
        assert mask.sum() >= 1


class TestMultiObjectiveOptimizer:

    def test_init(self, param_bounds):
        from multi_objective_optimizer import MultiObjectiveOptimizer
        opt = MultiObjectiveOptimizer(
            bounds=param_bounds,
            n_weight_samples=5,
            n_bo_iterations=3,
        )
        assert opt.n_objectives == 4
        assert opt.n_weight_samples == 5

    def test_optimize_runs(self, param_bounds):
        from multi_objective_optimizer import MultiObjectiveOptimizer
        opt = MultiObjectiveOptimizer(
            bounds=param_bounds,
            objective_fn=_cheap_objectives,
            n_weight_samples=3,
            n_bo_iterations=2,
        )
        result = opt.optimize()
        assert result.n_solutions >= 1
        assert result.objectives.shape[1] == 4
        for obj in result.objectives:
            assert obj[0] >= 0
            assert obj[1] >= 0
            assert obj[2] >= 0
            assert obj[3] >= 0

    def test_optimize_reproducible(self, param_bounds):
        from multi_objective_optimizer import MultiObjectiveOptimizer
        opt1 = MultiObjectiveOptimizer(param_bounds, _cheap_objectives, 3, 2, seed=99)
        opt2 = MultiObjectiveOptimizer(param_bounds, _cheap_objectives, 3, 2, seed=99)
        r1 = opt1.optimize()
        r2 = opt2.optimize()
        np.testing.assert_array_equal(r1.objectives, r2.objectives)


class TestVisualization:

    def test_plot_pareto(self, param_bounds, tmp_plot_dir):
        from multi_objective_optimizer import MultiObjectiveOptimizer
        opt = MultiObjectiveOptimizer(
            bounds=param_bounds, objective_fn=_cheap_objectives,
            n_weight_samples=5, n_bo_iterations=3,
        )
        result = opt.optimize()
        if result.n_solutions < 2:
            opt.n_weight_samples = 10
            opt.n_bo_iterations = 5
            result = opt.optimize()
        path = str(tmp_plot_dir / "pareto.png")
        result.plot(path=path)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 5000

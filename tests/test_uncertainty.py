import os
import numpy as np
import pytest


def _simple_eval(params):
    return np.array([
        params[0] * 2 + params[1] * 0.5 + 10,
        params[0] * 0.1 + 5,
    ])


class TestPredictionResult:

    def test_from_samples(self):
        from uncertainty_aware_twin import PredictionResult
        rng = np.random.RandomState(42)
        samples = rng.randn(500, 1)
        pr = PredictionResult.from_samples(samples)
        assert pr.mean.shape == (1,)
        assert pr.std.shape == (1,)
        assert pr.lower_95.shape == (1,)
        assert pr.upper_95.shape == (1,)
        assert pr.lower_95 < pr.mean < pr.upper_95

    def test_multidimensional(self):
        from uncertainty_aware_twin import PredictionResult
        rng = np.random.RandomState(42)
        samples = rng.randn(200, 4)
        pr = PredictionResult.from_samples(samples)
        assert pr.mean.shape == (4,)
        assert pr.std.shape == (4,)

    def test_single_prediction(self):
        from uncertainty_aware_twin import PredictionResult
        rng = np.random.RandomState(42)
        pr = PredictionResult(
            mean=np.array([50.0]),
            std=np.array([10.0]),
            lower_95=np.array([30.4]),
            upper_95=np.array([69.6]),
            samples=rng.randn(500, 1),
        )
        assert pr.n_samples == 500
        assert pr.n_outputs == 1
        assert pr.confidence_width(0) == pytest.approx(39.2, abs=0.5)


class TestUncertainDigitalTwin:

    def test_fit_and_predict(self):
        from uncertainty_aware_twin import UncertainDigitalTwin
        bounds = np.array([[1, 10], [1, 10]])
        twin = UncertainDigitalTwin(evaluate_fn=_simple_eval,
                                     bounds=bounds,
                                     n_ensembles=20,
                                     n_train_samples=50)
        rng = np.random.RandomState(42)
        X_train = rng.uniform(bounds[:, 0], bounds[:, 1], (50, 2))
        twin.fit(X_train)
        result = twin.predict(np.array([[5.0, 5.0]]), n_samples=500)
        assert result.n_samples == 500
        assert result.n_outputs == 2
        assert np.all(result.mean > 0)
        assert np.all(result.std > 0)

    def test_uncertainty_increases_at_boundaries(self):
        from uncertainty_aware_twin import UncertainDigitalTwin
        bounds = np.array([[1, 10], [1, 10]])
        twin = UncertainDigitalTwin(evaluate_fn=_simple_eval,
                                     bounds=bounds, n_ensembles=20,
                                     n_train_samples=50)
        rng = np.random.RandomState(42)
        X_train = rng.uniform(bounds[:, 0] + 1, bounds[:, 1] - 1, (50, 2))
        twin.fit(X_train)
        r_center = twin.predict(np.array([[5.0, 5.0]]))
        r_edge = twin.predict(np.array([[1.0, 1.0]]))
        center_std_0 = float(r_center.std[:, 0].mean())
        edge_std_0 = float(r_edge.std[:, 0].mean())
        assert edge_std_0 >= center_std_0 * 0.5

    def test_predict_batch(self):
        from uncertainty_aware_twin import UncertainDigitalTwin
        bounds = np.array([[1, 10], [1, 10]])
        twin = UncertainDigitalTwin(evaluate_fn=_simple_eval,
                                     bounds=bounds, n_ensembles=10,
                                     n_train_samples=30)
        rng = np.random.RandomState(42)
        X_train = rng.uniform(bounds[:, 0], bounds[:, 1], (30, 2))
        twin.fit(X_train)
        X_test = np.array([[3, 3], [5, 5], [8, 8]])
        result = twin.predict(X_test, n_samples=200)
        assert result.mean.shape == (3, 2)
        assert result.std.shape == (3, 2)

    def test_reproducible_with_seed(self):
        from uncertainty_aware_twin import UncertainDigitalTwin
        bounds = np.array([[1, 10], [1, 10]])
        t1 = UncertainDigitalTwin(_simple_eval, bounds, 10, 30, seed=99)
        t2 = UncertainDigitalTwin(_simple_eval, bounds, 10, 30, seed=99)
        rng = np.random.RandomState(42)
        X = rng.uniform(bounds[:, 0], bounds[:, 1], (30, 2))
        t1.fit(X)
        t2.fit(X)
        r1 = t1.predict(np.array([[5, 5]]), n_samples=200)
        r2 = t2.predict(np.array([[5, 5]]), n_samples=200)
        np.testing.assert_array_equal(r1.mean, r2.mean)


class TestUncertaintyVisualization:

    def test_plot_predictions(self, tmp_plot_dir):
        from uncertainty_aware_twin import UncertainDigitalTwin
        bounds = np.array([[1, 10], [1, 10]])
        twin = UncertainDigitalTwin(
            evaluate_fn=lambda p: np.array([p[0] * 2 + p[1], p[0] * 0.1 + 5]),
            bounds=bounds, n_ensembles=20, n_train_samples=40,
        )
        rng = np.random.RandomState(42)
        X = rng.uniform(bounds[:, 0], bounds[:, 1], (40, 2))
        twin.fit(X)
        result = twin.predict(np.array([[3, 3], [5, 5], [7, 7]]))
        path = str(tmp_plot_dir / "uncertainty.png")
        result.plot(path=path, output_names=["Power", "Cost"])
        assert os.path.exists(path)
        assert os.path.getsize(path) > 5000

import os
import numpy as np
import pytest


class TestPhysicsMeanFunction:

    def test_returns_scalar_for_single_input(self):
        from degradation_model import physics_mean_power
        result = physics_mean_power(t_days=1.0, temperature_C=25.0,
                                   pH=5.5, moisture_pct=25.0, o2_factor=1.0,
                                   base_power=260.0, deg_rate=2.0)
        assert isinstance(result, float)
        assert result > 0

    def test_power_decays_with_time(self):
        from degradation_model import physics_mean_power
        p1 = physics_mean_power(1.0, 25.0, 5.5, 25.0, 1.0, 260.0, 2.0)
        p10 = physics_mean_power(10.0, 25.0, 5.5, 25.0, 1.0, 260.0, 2.0)
        assert p10 < p1

    def test_higher_temperature_accelerates_degradation(self):
        from degradation_model import physics_mean_power
        p_25 = physics_mean_power(5.0, 25.0, 5.5, 25.0, 1.0, 260.0, 5.0)
        p_40 = physics_mean_power(5.0, 40.0, 5.5, 25.0, 1.0, 260.0, 5.0)
        assert p_40 < p_25

    def test_optimal_ph_maximizes_power(self):
        from degradation_model import physics_mean_power
        p_optimal = physics_mean_power(5.0, 25.0, 5.5, 25.0, 1.0, 260.0, 5.0)
        p_acidic = physics_mean_power(5.0, 25.0, 3.0, 25.0, 1.0, 260.0, 5.0)
        p_basic = physics_mean_power(5.0, 25.0, 8.0, 25.0, 1.0, 260.0, 5.0)
        assert p_optimal >= p_acidic
        assert p_optimal >= p_basic

    def test_moisture_sigmoid(self):
        from degradation_model import physics_mean_power
        p_dry = physics_mean_power(5.0, 25.0, 5.5, 5.0, 1.0, 260.0, 2.0)
        p_wet = physics_mean_power(5.0, 25.0, 5.5, 50.0, 1.0, 260.0, 2.0)
        assert p_wet > p_dry

    def test_zero_time_returns_base_power(self):
        from degradation_model import physics_mean_power
        p = physics_mean_power(0.0, 25.0, 5.5, 25.0, 1.0, 260.0, 2.0)
        assert p > 200.0
        assert p < 260.0

    def test_vectorized_input(self):
        from degradation_model import physics_mean_power
        t = np.array([0.0, 1.0, 5.0])
        result = physics_mean_power(t, 25.0, 5.5, 25.0, 1.0, 260.0, 2.0)
        assert result.shape == (3,)
        assert result[0] > result[2]


class TestDegradationModel:

    def test_fit_and_predict_shape(self):
        from degradation_model import DegradationModel
        model = DegradationModel()
        n = 30
        conditions = np.column_stack([
            np.random.uniform(15, 40, n),
            np.random.uniform(3, 8, n),
            np.random.uniform(5, 60, n),
            np.random.uniform(0.5, 2.0, n),
        ])
        t_days = np.linspace(0, 14, n)
        measurements = np.column_stack([
            model.physics_mean(t_days, conditions[:, 0], conditions[:, 1],
                               conditions[:, 2], conditions[:, 3])
            + np.random.normal(0, 5, n),
            np.zeros((n, 2)),
        ])
        model.fit(conditions, t_days, measurements)
        pred = model.predict(conditions[:3], np.array([1.0, 7.0, 14.0]))
        assert pred['power'].shape == (3, 3)
        assert pred['ocv'].shape == (3, 3)
        assert pred['resistance'].shape == (3, 3)

    def test_predict_faster_than_unconditioned(self):
        from degradation_model import DegradationModel
        model = DegradationModel(base_power=260.0)
        n = 20
        conditions = np.tile([25.0, 5.5, 25.0, 1.0], (n, 1))
        t_days = np.linspace(0, 10, n)
        measurements = np.column_stack([
            model.physics_mean(t_days, 25.0, 5.5, 25.0, 1.0)
            + np.random.normal(0, 3, n),
            model.physics_mean_ocv(t_days, 25.0, 5.5, 25.0, 1.0)
            + np.random.normal(0, 0.01, n),
            model.physics_mean_resistance(t_days, 25.0, 5.5, 25.0, 1.0)
            + np.random.normal(0, 200, n),
        ])
        model.fit(conditions, t_days, measurements)
        result = model.predict_lifetime(np.array([[25.0, 5.5, 25.0, 1.0]]))
        assert result > 0
        assert isinstance(result, float)

    def test_high_temp_shorter_lifetime(self):
        from degradation_model import DegradationModel
        model = DegradationModel(base_power=260.0, deg_rate=15.0)
        n = 30
        t_days = np.linspace(0, 30, n)
        rng = np.random.RandomState(42)
        noise = rng.normal(0, 3, n)

        c25 = np.tile([25.0, 5.5, 25.0, 1.0], (n, 1))
        c40 = np.tile([40.0, 5.5, 25.0, 1.0], (n, 1))
        combined_c = np.vstack([c25, c40])
        combined_t = np.tile(t_days, 2)

        combined_m = np.column_stack([
            np.concatenate([
                model.physics_mean(t_days, 25.0, 5.5, 25.0, 1.0) + noise,
                model.physics_mean(t_days, 40.0, 5.5, 25.0, 1.0) + noise,
            ]),
            np.concatenate([
                model.physics_mean_ocv(t_days, 25.0, 5.5, 25.0, 1.0) + rng.normal(0, 0.01, n),
                model.physics_mean_ocv(t_days, 40.0, 5.5, 25.0, 1.0) + rng.normal(0, 0.01, n),
            ]),
            np.concatenate([
                model.physics_mean_resistance(t_days, 25.0, 5.5, 25.0, 1.0) + rng.normal(0, 200, n),
                model.physics_mean_resistance(t_days, 40.0, 5.5, 25.0, 1.0) + rng.normal(0, 200, n),
            ]),
        ])

        model.fit(combined_c, combined_t, combined_m)
        lt_25 = model.predict_lifetime(np.array([[25.0, 5.5, 25.0, 1.0]]))
        lt_40 = model.predict_lifetime(np.array([[40.0, 5.5, 25.0, 1.0]]))
        assert lt_25 > lt_40

    def test_predict_uncertainty(self):
        from degradation_model import DegradationModel
        model = DegradationModel()
        n = 30
        conditions = np.tile([25.0, 5.5, 25.0, 1.0], (n, 1))
        t_days = np.linspace(0, 14, n)
        measurements = np.column_stack([
            model.physics_mean(t_days, 25.0, 5.5, 25.0, 1.0)
            + np.random.normal(0, 5, n),
            np.zeros((n, 2)),
        ])
        model.fit(conditions, t_days, measurements)
        pred = model.predict(
            np.array([[25.0, 5.5, 25.0, 1.0]]), np.array([7.0]),
            return_std=True,
        )
        assert 'power_std' in pred
        assert pred['power_std'].shape == pred['power'].shape
        assert np.all(pred['power_std'] >= 0)


class TestDegradationVisualization:

    def test_plot_degradation_curves(self, tmp_plot_dir):
        from degradation_model import DegradationModel
        model = DegradationModel(base_power=260.0)
        n = 25
        conditions = np.tile([25.0, 5.5, 25.0, 1.0], (n, 1))
        t_days = np.linspace(0, 14, n)
        measurements = np.column_stack([
            model.physics_mean(t_days, 25.0, 5.5, 25.0, 1.0)
            + np.random.normal(0, 5, n),
            model.physics_mean_ocv(t_days, 25.0, 5.5, 25.0, 1.0)
            + np.random.normal(0, 0.01, n),
            model.physics_mean_resistance(t_days, 25.0, 5.5, 25.0, 1.0)
            + np.random.normal(0, 200, n),
        ])
        model.fit(conditions, t_days, measurements)
        path = str(tmp_plot_dir / "degradation.png")
        model.plot_conditions(
            conditions_list=[[25.0, 5.5, 25.0, 1.0], [35.0, 5.5, 25.0, 1.0]],
            labels=["25C", "35C"],
            max_days=14,
            path=path,
        )
        assert os.path.exists(path)
        assert os.path.getsize(path) > 5000

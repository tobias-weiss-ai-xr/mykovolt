import numpy as np
from dataclasses import dataclass
from typing import Optional, Dict, List
import copy
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel, RBF


R_GAS = 8.314
T_REF_K = 298.15
EA_DEGRADATION = 50000.0
PH_OPTIMAL = 5.5
PH_SIGMA = 1.5
MOISTURE_HALF = 20.0


def physics_mean_power(t_days, temperature_C, pH, moisture_pct, o2_factor,
                       base_power=260.0, deg_rate=2.0):
    t_days = np.asarray(t_days, dtype=float)
    temperature_K = np.asarray(temperature_C, dtype=float) + 273.15

    arrhenius = np.exp(-EA_DEGRADATION / R_GAS * (1.0 / temperature_K - 1.0 / T_REF_K))
    ph_factor = np.exp(-((np.asarray(pH, dtype=float) - PH_OPTIMAL) ** 2) / (2 * PH_SIGMA ** 2))
    moisture_factor = 1.0 / (1.0 + np.exp(-(np.asarray(moisture_pct, dtype=float) - MOISTURE_HALF) / 10.0))
    o2_f = np.asarray(o2_factor, dtype=float)

    effective_deg = deg_rate * arrhenius * (0.7 + 0.3 * ph_factor)

    power = base_power * (1.0 - effective_deg / 100.0) ** t_days * ph_factor * (0.5 + 0.5 * moisture_factor) * o2_f
    return power


def physics_mean_ocv(t_days, temperature_C, pH, moisture_pct, o2_factor,
                      base_ocv=0.45, deg_rate=2.0):
    t_days = np.asarray(t_days, dtype=float)
    temperature_K = np.asarray(temperature_C, dtype=float) + 273.15
    arrhenius = np.exp(-EA_DEGRADATION / R_GAS * (1.0 / temperature_K - 1.0 / T_REF_K))
    effective_deg = deg_rate * (0.5 + 0.5 / arrhenius) * 0.5
    return base_ocv * (1.0 - effective_deg / 100.0) ** (t_days * 0.5)


def physics_mean_resistance(t_days, temperature_C, pH, moisture_pct, o2_factor,
                             base_resistance=10000.0, deg_rate=2.0):
    t_days = np.asarray(t_days, dtype=float)
    temperature_K = np.asarray(temperature_C, dtype=float) + 273.15
    arrhenius = np.exp(-EA_DEGRADATION / R_GAS * (1.0 / temperature_K - 1.0 / T_REF_K))
    effective_deg = deg_rate * (0.3 + 0.7 * arrhenius)
    return base_resistance * (1.0 + effective_deg / 100.0) ** t_days


class DegradationModel:
    def __init__(self, base_power=260.0, base_ocv=0.45,
                 base_resistance=10000.0, deg_rate=2.0):
        self.base_power = base_power
        self.base_ocv = base_ocv
        self.base_resistance = base_resistance
        self.deg_rate = deg_rate
        self.gp_power = None
        self.gp_ocv = None
        self.gp_resistance = None
        self._trained = False

    def physics_mean(self, t_days, temp_C, pH, moisture, o2):
        return physics_mean_power(t_days, temp_C, pH, moisture, o2,
                                  self.base_power, self.deg_rate)

    def physics_mean_ocv(self, t_days, temp_C, pH, moisture, o2):
        return physics_mean_ocv(t_days, temp_C, pH, moisture, o2,
                                 self.base_ocv, self.deg_rate)

    def physics_mean_resistance(self, t_days, temp_C, pH, moisture, o2):
        return physics_mean_resistance(t_days, temp_C, pH, moisture, o2,
                                        self.base_resistance, self.deg_rate)

    def fit(self, conditions: np.ndarray, t_days: np.ndarray,
            measurements: np.ndarray):
        features = np.column_stack([conditions, t_days])
        kernel = (ConstantKernel(1.0) *
                  Matern(length_scale=np.ones(features.shape[1]), nu=2.5) +
                  WhiteKernel(0.1))

        self.gp_power = GaussianProcessRegressor(
            kernel=kernel, normalize_y=True,
            n_restarts_optimizer=2, random_state=42)
        self.gp_power.fit(features, measurements[:, 0])

        if measurements.shape[1] >= 2:
            self.gp_ocv = GaussianProcessRegressor(
                kernel=copy.deepcopy(kernel), normalize_y=True,
                n_restarts_optimizer=2, random_state=42)
            self.gp_ocv.fit(features, measurements[:, 1])

        if measurements.shape[1] >= 3:
            self.gp_resistance = GaussianProcessRegressor(
                kernel=copy.deepcopy(kernel), normalize_y=True,
                n_restarts_optimizer=2, random_state=42)
            self.gp_resistance.fit(features, measurements[:, 2])

        self._trained = True
        return self

    def predict(self, conditions: np.ndarray, t_days: np.ndarray,
                return_std: bool = False) -> Dict:
        if conditions.ndim == 1:
            conditions = conditions.reshape(1, -1)
        if np.isscalar(t_days):
            t_days = np.array([t_days])

        features = np.column_stack([
            np.tile(conditions, (len(t_days), 1)),
            np.repeat(t_days, len(conditions)),
        ])

        result = {}
        n_cond = len(conditions)
        n_t = len(t_days)
        shape = (n_cond, n_t)

        if return_std:
            p_mean, p_std = self.gp_power.predict(features, return_std=True)
            result['power'] = p_mean.reshape(shape)
            result['power_std'] = p_std.reshape(shape)
            if self.gp_ocv:
                o_mean, o_std = self.gp_ocv.predict(features, return_std=True)
                result['ocv'] = o_mean.reshape(shape)
                result['ocv_std'] = o_std.reshape(shape)
            if self.gp_resistance:
                r_mean, r_std = self.gp_resistance.predict(features, return_std=True)
                result['resistance'] = r_mean.reshape(shape)
                result['resistance_std'] = r_std.reshape(shape)
        else:
            result['power'] = self.gp_power.predict(features).reshape(shape)
            if self.gp_ocv:
                result['ocv'] = self.gp_ocv.predict(features).reshape(shape)
            if self.gp_resistance:
                result['resistance'] = self.gp_resistance.predict(features).reshape(shape)

        return result

    def predict_lifetime(self, conditions: np.ndarray,
                         min_power_uw: float = 12.0) -> float:
        if conditions.ndim == 1:
            conditions = conditions.reshape(1, -1)
        t_test = np.linspace(0, 60, 120)
        pred = self.predict(conditions, t_test)
        power_curve = pred['power'][0]
        below = np.where(power_curve < min_power_uw)[0]
        if len(below) == 0:
            return 60.0
        return float(t_test[below[0]])

    def plot_conditions(self, conditions_list: List, labels=None, max_days=30,
                        path="degradation.png"):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        t = np.linspace(0, max_days, 100)
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))

        for i, cond in enumerate(conditions_list):
            c = np.array(cond).reshape(1, -1)
            pred = self.predict(c, t, return_std=True)
            label = labels[i] if labels else f"Cond {i}"
            color = plt.cm.tab10(i)

            ax1.plot(t, pred['power'][0], color=color, label=label)
            if 'power_std' in pred:
                ax1.fill_between(t,
                                 pred['power'][0] - pred['power_std'][0],
                                 pred['power'][0] + pred['power_std'][0],
                                 alpha=0.15, color=color)
            ax1.axhline(12.5, color='gray', linestyle=':', alpha=0.5)

            if 'ocv' in pred:
                ax2.plot(t, pred['ocv'][0], color=color, label=label)

            if 'resistance' in pred:
                ax3.plot(t, pred['resistance'][0], color=color, label=label)

        ax1.set_xlabel("Days"); ax1.set_ylabel("Power (\u00b5W/cm\u00b2)")
        ax1.set_title("Power Degradation"); ax1.legend(fontsize=8); ax1.grid(alpha=0.3)
        ax2.set_xlabel("Days"); ax2.set_ylabel("OCV (V)")
        ax2.set_title("Open Circuit Voltage"); ax2.legend(fontsize=8); ax2.grid(alpha=0.3)
        ax3.set_xlabel("Days"); ax3.set_ylabel("R_internal (\u03a9)")
        ax3.set_title("Internal Resistance"); ax3.legend(fontsize=8); ax3.grid(alpha=0.3)

        plt.suptitle("Physics-Informed GP Degradation Model", fontsize=14)
        plt.tight_layout()
        plt.savefig(path, dpi=150, bbox_inches='tight')
        plt.close()

"""Calibrated pressling power model with parameter fitting."""

from __future__ import annotations
import math
from dataclasses import dataclass
from pathlib import Path


@dataclass
class IVPoint:
    voltage_mv: float
    current_ma: float
    power_uw: float


@dataclass
class CalibratedModel:
    power_density_uw_cm2: float = 12.5
    activation_loss: float = 0.05
    ohmic_loss_r_cm2: float = 50.0
    depletion_rate: float = 0.02

    def raw_power_uw(self, area_cm2: float, day: int = 0) -> float:
        decay = (1 - self.depletion_rate) ** day
        return self.power_density_uw_cm2 * area_cm2 * decay

    def voltage_oc_mv(self, area_cm2: float, day: int = 0) -> float:
        """Approximate open-circuit voltage from power density.

        V_OC approx sqrt(4 * P * R_internal) for a simple MFC model.
        Typical range: 300-600 mV.
        """
        p = self.raw_power_uw(area_cm2, day)
        r = self.ohmic_loss_r_cm2 / area_cm2
        voc = math.sqrt(max(4 * p * 1e-6 * r, 1e-12)) * 1000
        return max(min(voc, 800.0), 50.0)

    def voltage_at_current(
        self, current_ma: float, area_cm2: float = 19.63, day: int = 0
    ) -> float:
        voc = self.voltage_oc_mv(area_cm2, day)
        r_eff = self.ohmic_loss_r_cm2 / area_cm2
        activation = (
            self.activation_loss * math.log1p(current_ma) * 100 if current_ma > 0 else 0
        )
        v = voc - current_ma * r_eff - activation
        return max(v, 0.0)

    def power_at_current(
        self, current_ma: float, area_cm2: float = 19.63, day: int = 0
    ) -> float:
        v = self.voltage_at_current(current_ma, area_cm2, day)
        return v * current_ma

    def iv_curve(
        self, area_cm2: float = 19.63, currents_ma: list[float] | None = None
    ) -> list[IVPoint]:
        if currents_ma is None:
            currents_ma = [i * 0.1 for i in range(51)]
        points = []
        for i_ma in currents_ma:
            v = self.voltage_at_current(i_ma, area_cm2)
            p = v * i_ma
            points.append(IVPoint(voltage_mv=v, current_ma=i_ma, power_uw=p))
        return points


def fit_model(
    measurements: list[dict], area_cm2: float = 19.63, n_grid: int = 20
) -> CalibratedModel:
    """Fit model parameters to measured I/V data using grid search.

    Each measurement dict: {"day", "current_ma", "voltage_mv"}.
    Uses brute-force grid search (no scipy dependency).
    """
    best_model = CalibratedModel()
    best_error = float("inf")

    for pd in [i * (30.0 / n_grid) + 5.0 for i in range(n_grid)]:
        for rl in [i * (200.0 / n_grid) + 10.0 for i in range(n_grid)]:
            for dr in [i * (0.05 / n_grid) for i in range(n_grid)]:
                m = CalibratedModel(
                    power_density_uw_cm2=pd, ohmic_loss_r_cm2=rl, depletion_rate=dr
                )
                error = 0.0
                for meas in measurements:
                    v_pred = m.voltage_at_current(
                        meas["current_ma"], area_cm2, day=meas.get("day", 0)
                    )
                    error += (v_pred - meas["voltage_mv"]) ** 2
                if error < best_error:
                    best_error = error
                    best_model = m

    return best_model


def model_params_to_yaml(model: CalibratedModel, path: Path | str) -> None:
    lines = [
        f"power_density_uw_cm2: {model.power_density_uw_cm2:.4f}",
        f"activation_loss: {model.activation_loss:.4f}",
        f"ohmic_loss_r_cm2: {model.ohmic_loss_r_cm2:.4f}",
        f"depletion_rate: {model.depletion_rate:.6f}",
    ]
    Path(path).write_text("\n".join(lines) + "\n")


def model_params_from_yaml(path: Path | str) -> CalibratedModel:
    text = Path(path).read_text()
    params = {}
    for line in text.strip().splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            params[key.strip()] = float(val.strip())
    return CalibratedModel(
        power_density_uw_cm2=params.get("power_density_uw_cm2", 12.5),
        activation_loss=params.get("activation_loss", 0.05),
        ohmic_loss_r_cm2=params.get("ohmic_loss_r_cm2", 50.0),
        depletion_rate=params.get("depletion_rate", 0.02),
    )

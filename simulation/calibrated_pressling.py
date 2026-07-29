"""Geometry sweep and multi-cell predictions for calibrated pressling model."""

from __future__ import annotations
import math
import sys
from dataclasses import dataclass

sys.path.insert(0, ".")
from mykovolt.calibrate_sim import CalibratedModel


@dataclass
class GeometryResult:
    diameter_mm: float
    height_mm: float
    area_cm2: float
    voltage_mv: float
    power_uw: float


@dataclass
class MultiCellResult:
    n_cells: int
    config: str
    voltage_mv: float
    current_ma: float
    power_uw: float
    cell_voltage_mv: float
    max_current_ma: float


def _disc_area_cm2(diameter_mm: float) -> float:
    return math.pi * (diameter_mm / 2) ** 2 / 100


def geometry_sweep(
    power_density_uw_cm2: float = 12.5,
    ohmic_loss_r_cm2: float = 50.0,
    depletion_rate: float = 0.02,
    diameters_mm: list[float] | None = None,
    heights_mm: list[float] | None = None,
    current_ma: float = 1.0,
    day: int = 0,
) -> list[GeometryResult]:
    if diameters_mm is None:
        diameters_mm = [50, 80, 100, 150, 200, 300]
    if heights_mm is None:
        heights_mm = [8, 12, 20]
    m = CalibratedModel(
        power_density_uw_cm2=power_density_uw_cm2,
        ohmic_loss_r_cm2=ohmic_loss_r_cm2,
        depletion_rate=depletion_rate,
    )
    results = []
    for d in diameters_mm:
        for h in heights_mm:
            area = _disc_area_cm2(d)
            v = m.voltage_at_current(current_ma, area, day)
            p = v * current_ma
            results.append(
                GeometryResult(
                    diameter_mm=d,
                    height_mm=h,
                    area_cm2=area,
                    voltage_mv=v,
                    power_uw=p,
                )
            )
    return results


def multi_cell_predict(
    n_cells: int,
    config: str = "series",
    power_density_uw_cm2: float = 12.5,
    ohmic_loss_r_cm2: float = 50.0,
    depletion_rate: float = 0.02,
    diameter_mm: float = 50.0,
    height_mm: float = 8.0,
    load_current_ma: float = 0.5,
    day: int = 0,
) -> MultiCellResult:
    area = _disc_area_cm2(diameter_mm)
    m = CalibratedModel(
        power_density_uw_cm2=power_density_uw_cm2,
        ohmic_loss_r_cm2=ohmic_loss_r_cm2,
        depletion_rate=depletion_rate,
    )
    cell_v = m.voltage_at_current(load_current_ma, area, day)
    cell_max_i = cell_v / (m.ohmic_loss_r_cm2 / area) if area > 0 else 0

    if config == "series":
        total_v = cell_v * n_cells
        total_i = load_current_ma
        max_i = cell_max_i
    elif config == "parallel":
        total_v = cell_v
        total_i = load_current_ma
        max_i = cell_max_i * n_cells
    else:
        raise ValueError(f"Unknown config: {config}")

    return MultiCellResult(
        n_cells=n_cells,
        config=config,
        voltage_mv=total_v,
        current_ma=total_i,
        power_uw=total_v * total_i,
        cell_voltage_mv=cell_v,
        max_current_ma=max_i,
    )

import pytest
from simulation.calibrated_pressling import geometry_sweep, multi_cell_predict


def test_geometry_sweep_returns_multiple():
    results = geometry_sweep(
        power_density_uw_cm2=12.5,
        diameters_mm=[50, 100, 150],
        heights_mm=[8, 12],
        current_ma=1.0,
    )
    assert len(results) == 6  # 3 diameters x 2 heights
    assert results[0].diameter_mm == 50
    assert results[0].height_mm == 8
    assert results[0].power_uw > 0
    # larger disc should produce more power
    assert results[-1].power_uw > results[0].power_uw


def test_multi_cell_series():
    result = multi_cell_predict(
        n_cells=3,
        config="series",
        power_density_uw_cm2=12.5,
        diameter_mm=50,
        height_mm=8,
        load_current_ma=0.5,
    )
    assert result.voltage_mv > result.cell_voltage_mv
    assert abs(result.current_ma - 0.5) < 0.01


def test_multi_cell_parallel():
    result = multi_cell_predict(
        n_cells=3,
        config="parallel",
        power_density_uw_cm2=12.5,
        diameter_mm=50,
        height_mm=8,
        load_current_ma=0.5,
    )
    assert result.voltage_mv == pytest.approx(result.cell_voltage_mv)
    assert result.max_current_ma > 0.5


def test_multi_cell_invalid_config():
    with pytest.raises(ValueError, match="Unknown config"):
        multi_cell_predict(n_cells=2, config="invalid")

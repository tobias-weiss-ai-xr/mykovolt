import pytest
from mykovolt.calibrate_sim import (
    CalibratedModel,
    fit_model,
    model_params_to_yaml,
    model_params_from_yaml,
)


def test_calibrated_model_predicts_power():
    m = CalibratedModel(
        power_density_uw_cm2=12.5,
        activation_loss=0.05,
        ohmic_loss_r_cm2=50.0,
        depletion_rate=0.02,
    )
    power = m.power_at_current(0.0)
    assert power == 0.0
    power_loaded = m.power_at_current(1.0)
    assert power_loaded > 0
    assert m.voltage_at_current(1.0) < m.voltage_oc_mv(19.63)


def test_calibrated_model_iv_curve():
    m = CalibratedModel(power_density_uw_cm2=12.5)
    iv = m.iv_curve(area_cm2=19.63, currents_ma=[0, 0.5, 1.0, 2.0, 5.0])
    assert len(iv) == 5
    assert iv[0].voltage_mv > iv[1].voltage_mv
    assert iv[0].current_ma == 0


def test_calibrated_model_depletion():
    m = CalibratedModel(power_density_uw_cm2=12.5, depletion_rate=0.1)
    p_day0 = m.raw_power_uw(19.63, day=0)
    p_day10 = m.raw_power_uw(19.63, day=10)
    assert p_day10 < p_day0


def test_fit_model_synthetic():
    """Generate synthetic data, fit, check params recovered."""
    import random

    random.seed(42)
    true_params = {
        "power_density_uw_cm2": 15.0,
        "ohmic_loss_r_cm2": 80.0,
        "depletion_rate": 0.03,
    }
    m_true = CalibratedModel(**true_params)
    measurements = []
    for day in range(30):
        current = random.uniform(0.1, 2.0)
        voltage = m_true.voltage_at_current(current, day=day, area_cm2=19.63)
        measurements.append(
            {
                "day": day,
                "current_ma": current,
                "voltage_mv": voltage,
            }
        )
    fitted = fit_model(measurements, area_cm2=19.63)
    assert abs(fitted.power_density_uw_cm2 - 15.0) < 5.0
    assert abs(fitted.depletion_rate - 0.03) < 0.02


def test_model_params_yaml_roundtrip(tmp_path):
    m = CalibratedModel(
        power_density_uw_cm2=12.5, ohmic_loss_r_cm2=50.0, depletion_rate=0.02
    )
    path = tmp_path / "params.yaml"
    model_params_to_yaml(m, path)
    m2 = model_params_from_yaml(path)
    assert m2.power_density_uw_cm2 == pytest.approx(m.power_density_uw_cm2)
    assert m2.ohmic_loss_r_cm2 == pytest.approx(m.ohmic_loss_r_cm2)
    assert m2.depletion_rate == pytest.approx(m.depletion_rate)


def test_model_params_from_yaml_missing_keys(tmp_path):
    """YAML with only some keys should use defaults for the rest."""
    path = tmp_path / "partial.yaml"
    path.write_text("power_density_uw_cm2: 20.0\n")
    m = model_params_from_yaml(path)
    assert m.power_density_uw_cm2 == 20.0
    assert m.ohmic_loss_r_cm2 == 50.0

from mykovolt.backend import Backend
from mykovolt.fram import read_fram
from mykovolt.calibrate import load_calibration, apply_calibration
from mykovolt.schema import SensorEntry


def run_pipeline(
    backend: Backend,
    cal_path: str | None = None,
) -> list[SensorEntry]:
    _, entries = read_fram(backend)
    if cal_path:
        cal = load_calibration(cal_path)
        entries = [apply_calibration(e, cal) for e in entries]
    return entries

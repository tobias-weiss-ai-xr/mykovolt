import pytest
from mykovolt.schema import SensorEntry
from mykovolt.plot import plot_timeseries, plot_summary


def make_entries():
    return [
        SensorEntry(1000, 123.45, 3100, 1500, 0x01, True),
        SensorEntry(1060, 124.10, 3080, 1490, 0x03, True),
        SensorEntry(1120, 122.80, 3050, 1480, 0x01, True),
        SensorEntry(1180, 125.30, 3020, 1470, 0x03, True),
    ]


def test_plot_timeseries_creates_figure():
    fig = plot_timeseries(make_entries())
    assert fig is not None
    import matplotlib

    assert isinstance(fig, matplotlib.figure.Figure)


def test_plot_summary_creates_figure():
    fig = plot_summary(make_entries())
    assert fig is not None
    import matplotlib

    assert isinstance(fig, matplotlib.figure.Figure)


def test_plot_empty_returns_none():
    assert plot_timeseries([]) is None
    assert plot_summary([]) is None

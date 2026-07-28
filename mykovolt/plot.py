"""Quick-look matplotlib plots for sensor data."""

from __future__ import annotations
from mykovolt.schema import SensorEntry


def plot_timeseries(entries: list[SensorEntry]):
    if not entries:
        return None
    import matplotlib.pyplot as plt

    times = [e.timestamp for e in entries]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    ax1.plot(times, [e.capacitance_pf for e in entries], "b.-")
    ax1.set_ylabel("Capacitance (pF)")
    ax1.grid(True)
    ax2.plot(times, [e.v_batt_mv for e in entries], "r.-", label="V_batt")
    ax2.plot(times, [e.v_sense_mv for e in entries], "g.-", label="V_sense")
    ax2.set_xlabel("Timestamp (s)")
    ax2.set_ylabel("Voltage (mV)")
    ax2.legend()
    ax2.grid(True)
    fig.tight_layout()
    return fig


def plot_summary(entries: list[SensorEntry]):
    if not entries:
        return None
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(10, 6))
    caps = [e.capacitance_pf for e in entries]
    axes[0, 0].hist(caps, bins=10, edgecolor="black")
    axes[0, 0].set_xlabel("Capacitance (pF)")
    axes[0, 0].set_ylabel("Count")
    axes[0, 0].set_title("Capacitance Distribution")
    axes[0, 1].plot(
        [e.v_batt_mv for e in entries], [e.v_sense_mv for e in entries], "."
    )
    axes[0, 1].set_xlabel("V_batt (mV)")
    axes[0, 1].set_ylabel("V_sense (mV)")
    axes[0, 1].set_title("Voltage Correlation")
    crc_ok = sum(1 for e in entries if e.crc_ok)
    crc_bad = len(entries) - crc_ok
    axes[1, 0].bar(["CRC OK", "CRC Bad"], [crc_ok, crc_bad])
    axes[1, 0].set_title("Data Integrity")
    vt = [e.status & 1 for e in entries]
    rt = [(e.status >> 1) & 1 for e in entries]
    times_l = list(range(len(entries)))
    axes[1, 1].plot(times_l, vt, "g|", label="VBAT_OK")
    axes[1, 1].plot(times_l, rt, "r|", label="RTC_ALARM")
    axes[1, 1].set_xlabel("Entry #")
    axes[1, 1].set_title("Status Flags")
    axes[1, 1].legend()
    fig.tight_layout()
    return fig

import sys
import json
import csv
import click
from mykovolt import __version__
from mykovolt.backend import I2cBackend
from mykovolt.fram import read_fram
from mykovolt.calibrate import load_calibration, apply_calibration
from mykovolt.export import export_csv, export_json
from mykovolt.plot import plot_timeseries, plot_summary
from mykovolt.pipeline import run_pipeline
from mykovolt.schema import (
    SensorEntry,
    TestFixtureEntry,
    parse_header,
    parse_entries_versioned,
    FRAM_DATA_START,
    FRAM_MAX_ENTRIES,
)


@click.group()
@click.version_option(version=__version__)
def cli():
    """MykoVolt DevKit — sensor data tooling."""


@cli.command()
@click.option("--backend", type=click.Choice(["i2c", "nfc"]), default="i2c")
@click.option("--bus", default=1, help="I2C bus number")
@click.option("--addr", default=0x50, help="FRAM I2C address", type=int)
@click.option("--output", "-o", default=None, help="Output file")
@click.option("--format", "-f", "fmt", default="csv", help="Output format")
@click.option("--calibration", "-c", default=None, help="Calibration JSON file")
def pipeline(backend, bus, addr, output, fmt, calibration):
    """Fetch, parse, calibrate, and export in one command."""
    if backend == "i2c":
        dev = I2cBackend(bus=bus, addr=addr)
    else:
        click.echo("NFC backend not yet implemented", err=True)
        sys.exit(1)
    try:
        entries = run_pipeline(dev, cal_path=calibration)
    except (ValueError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    if not entries:
        click.echo("No entries found", err=True)
        sys.exit(0)
    buf = open(output, "w") if output else sys.stdout
    if fmt == "csv":
        export_csv(entries, buf)
    else:
        export_json(entries, buf)
    if output:
        buf.close()
        click.echo(f"Wrote {len(entries)} entries to {output}")


@cli.command()
@click.option("--backend", type=click.Choice(["i2c", "nfc"]), default="i2c")
@click.option("--bus", default=1, help="I2C bus number")
@click.option("--addr", default=0x50, help="FRAM I2C address", type=int)
def fetch(backend, bus, addr):
    """Read raw FRAM data from device."""
    if backend == "i2c":
        dev = I2cBackend(bus=bus, addr=addr)
    else:
        click.echo("NFC backend not yet implemented", err=True)
        sys.exit(1)
    try:
        header, entries = read_fram(dev)
    except (ValueError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    click.echo(
        f"Header: magic=0x{header.magic:04X} version={header.version} "
        f"write_ptr={header.write_ptr}"
    )
    click.echo(f"Entries: {len(entries)}")
    for e in entries:
        if isinstance(e, TestFixtureEntry):
            click.echo(
                f"  ts={e.timestamp} voc={e.voc_mv}mV load={e.load_current_ma}mA "
                f"R={e.load_resistor_index} T={e.temp_c}C RH={e.humidity_pct}% "
                f"status=0x{e.status:02x} crc={'OK' if e.crc_ok else 'BAD'}"
            )
        else:
            click.echo(
                f"  ts={e.timestamp} cap={e.capacitance_pf:.2f}pF "
                f"Vbatt={e.v_batt_mv}mV Vsense={e.v_sense_mv}mV "
                f"status=0x{e.status:02x} crc={'OK' if e.crc_ok else 'BAD'}"
            )


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("--output", "-o", default=None, help="Output file")
@click.option("--format", "-f", "fmt", default="csv", help="Output format")
@click.option("--calibration", "-c", default=None, help="Calibration JSON file")
def parse(input, output, fmt, calibration):
    """Parse raw FRAM binary dump."""
    with open(input, "rb") as f:
        data = f.read()
    header = parse_header(data)
    if header is None:
        click.echo("Invalid FRAM header", err=True)
        sys.exit(1)
    click.echo(
        f"Header: magic=0x{header.magic:04X} version={header.version} "
        f"write_ptr={header.write_ptr}"
    )
    entries = parse_entries_versioned(header, data[FRAM_DATA_START:])
    if calibration and header.version == 1:
        cal = load_calibration(calibration)
        entries = [apply_calibration(e, cal) for e in entries]
    click.echo(f"Parsed {len(entries)} entries (v{header.version})")
    buf = open(output, "w") if output else sys.stdout
    if fmt == "csv":
        export_csv(entries, buf)
    else:
        export_json(entries, buf)
    if output:
        buf.close()


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("--output", "-o", default="calibration.json", help="Output file")
def calibrate(input, output):
    """Generate calibration from known reference data."""
    click.echo("Calibration generation not yet implemented", err=True)


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("--output", "-o", default="plot.png", help="Output image")
@click.option(
    "--type",
    "plot_type",
    default="timeseries",
    type=click.Choice(["timeseries", "summary"]),
)
def plot(input, output, plot_type):
    """Plot sensor data from a CSV/JSON export."""
    if input.endswith(".json"):
        with open(input) as f:
            rows = json.load(f)
    else:
        with open(input, newline="") as f:
            rows = list(csv.DictReader(f))
    entries = [
        SensorEntry(
            timestamp=int(r["timestamp"]),
            capacitance_pf=float(r["capacitance_pf"]),
            v_batt_mv=int(r["v_batt_mv"]),
            v_sense_mv=int(r["v_sense_mv"]),
            status=int(r["status"]),
            crc_ok=r.get("crc_ok", "True") == "True",
        )
        for r in rows
    ]
    fn = plot_timeseries if plot_type == "timeseries" else plot_summary
    fig = fn(entries)
    if fig is None:
        click.echo("No data to plot", err=True)
        sys.exit(1)
    fig.savefig(output, dpi=150)
    click.echo(f"Plot saved to {output}")

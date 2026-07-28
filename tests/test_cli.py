"""Tests for the mykovolt CLI package skeleton."""

from click.testing import CliRunner


def test_package_importable():
    import mykovolt


def test_version():
    import mykovolt

    assert mykovolt.__version__ == "0.1.0"


def test_cli_help():
    from mykovolt.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_cli_subcommands_in_help():
    from mykovolt.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "pipeline" in result.output
    assert "fetch" in result.output
    assert "parse" in result.output
    assert "calibrate" in result.output
    assert "plot" in result.output


def test_cli_fetch_no_backend():
    from mykovolt.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["fetch"])
    assert result.exit_code != 0


def test_cli_parse_help():
    from mykovolt.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["parse", "--help"])
    assert result.exit_code == 0
    assert "INPUT" in result.output


def test_cli_parse_valid_file(tmp_path):
    import struct
    from mykovolt.cli import cli

    data = struct.pack(">HBH", 0x4D56, 0x01, 12)
    data = data.ljust(256, b"\x00")
    entry = struct.pack(">IHHHB", 1000, 12345, 3100, 1500, 0x01)
    crc = 0
    for b in entry:
        crc ^= b
    data += entry + bytes([crc])
    fram_file = tmp_path / "fram.bin"
    fram_file.write_bytes(data)
    runner = CliRunner()
    result = runner.invoke(cli, ["parse", str(fram_file)])
    assert result.exit_code == 0
    assert "1000" in result.output
    assert "123.45" in result.output


def test_cli_pipeline_help():
    from mykovolt.cli import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["pipeline", "--help"])
    assert result.exit_code == 0


def test_parse_shows_version(tmp_path):
    from mykovolt.cli import cli
    from mykovolt.schema import FRAM_MAGIC, FRAM_ENTRY_SIZE_V2
    import struct

    header = struct.pack(">HBH", FRAM_MAGIC, 2, FRAM_ENTRY_SIZE_V2) + b"\x00" * (
        256 - 7
    )
    entry = b"\x00" * FRAM_ENTRY_SIZE_V2
    data = header + entry
    bin_file = tmp_path / "fram.bin"
    bin_file.write_bytes(data)
    runner = CliRunner()
    result = runner.invoke(cli, ["parse", str(bin_file)])
    assert result.exit_code == 0
    assert "version=2" in result.output

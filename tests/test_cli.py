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

"""
cli-common-flags_test.py

tests for the shared `-N/--no-newline` and `-C/--no-color` flags inherited
by the `cb`, `cb0`, and `logger` CLI subcommands via `_common_parser`, and
for the `-w/--line-width`/`-e/--stderr` pair still inherited by `cb`/`cb0`
via `_banner_parser`, in `kamilog.py`
"""

import io

import pytest
from kamilog.kamilog import _cli_parser


_SUBCOMMAND_ARGS = [
    ["cb", "c", "="],
    ["cb0"],
    ["logger", "info"],
]


class _FakeTtyStream(io.StringIO):
    def isatty(_):
        return True


class TestNoNewlineFlagIsRecognized:
    @pytest.mark.parametrize("argv", _SUBCOMMAND_ARGS)
    def test_default_no_newline_is_false(_, argv):
        args = _cli_parser.parse_args(argv)
        assert args.no_newline is False

    @pytest.mark.parametrize("argv", _SUBCOMMAND_ARGS)
    def test_short_flag_sets_no_newline(_, argv):
        args = _cli_parser.parse_args(argv + ["-N"])
        assert args.no_newline is True

    @pytest.mark.parametrize("argv", _SUBCOMMAND_ARGS)
    def test_long_flag_sets_no_newline(_, argv):
        args = _cli_parser.parse_args(argv + ["--no-newline"])
        assert args.no_newline is True


class TestNoColorFlagIsRecognized:
    @pytest.mark.parametrize("argv", _SUBCOMMAND_ARGS)
    def test_default_no_color_is_false(_, argv):
        args = _cli_parser.parse_args(argv)
        assert args.no_color is False

    @pytest.mark.parametrize("argv", _SUBCOMMAND_ARGS)
    def test_short_flag_sets_no_color(_, argv):
        args = _cli_parser.parse_args(argv + ["-C"])
        assert args.no_color is True

    @pytest.mark.parametrize("argv", _SUBCOMMAND_ARGS)
    def test_long_flag_sets_no_color(_, argv):
        args = _cli_parser.parse_args(argv + ["--no-color"])
        assert args.no_color is True


class TestBannerFlagsStillInherited:
    @pytest.mark.parametrize("subcommand", ["cb", "cb0"])
    def test_line_width_parses(_, subcommand):
        argv = [subcommand] + (["c", "="] if subcommand == "cb" else [])
        args = _cli_parser.parse_args(argv + ["-w", "40"])
        assert args.line_width == 40

    @pytest.mark.parametrize("subcommand", ["cb", "cb0"])
    def test_stderr_flag_parses(_, subcommand):
        argv = [subcommand] + (["c", "="] if subcommand == "cb" else [])
        args = _cli_parser.parse_args(argv + ["-e"])
        assert args.stderr is True


class TestNoColorDisablesAnsiOutput:
    def test_default_colors_a_tty_stream(_, monkeypatch):
        stream = _FakeTtyStream()
        monkeypatch.setattr("sys.stdin", io.StringIO("hi\n"))
        monkeypatch.setattr("sys.stdout", stream)
        args = _cli_parser.parse_args(["cb", "c", "=", "-w", "20"])
        args.func(args)
        assert "\033[" in stream.getvalue()

    def test_no_color_strips_ansi_from_tty_stream(_, monkeypatch):
        stream = _FakeTtyStream()
        monkeypatch.setattr("sys.stdin", io.StringIO("hi\n"))
        monkeypatch.setattr("sys.stdout", stream)
        args = _cli_parser.parse_args(["cb", "c", "=", "-w", "20", "-C"])
        args.func(args)
        assert "\033[" not in stream.getvalue()

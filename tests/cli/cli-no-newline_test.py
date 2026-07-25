"""
cli-no-newline_test.py

tests for the shared `-N/--no-newline` flag's effect on the `cb`, `cb0`,
and `logger` CLI subcommands' printed output in `kamilog.py`
"""

import io
import uuid

from kamilog.kamilog import _cli_parser


def _run(argv, stdin_text):
    stdout = io.StringIO()
    args = _cli_parser.parse_args(argv)
    import sys as _sys

    old_stdin, old_stdout = _sys.stdin, _sys.stdout
    _sys.stdin, _sys.stdout = io.StringIO(stdin_text), stdout
    try:
        args.func(args)
    finally:
        _sys.stdin, _sys.stdout = old_stdin, old_stdout
    return stdout.getvalue()


class TestCommentBannerNoNewline:
    def test_default_ends_with_newline(_):
        out = _run(["cb", "c", "=", "-w", "20"], "hi\n")
        assert out.endswith("\n")

    def test_no_newline_trims_trailing_newline(_):
        out = _run(["cb", "c", "=", "-w", "20", "-N"], "hi\n")
        assert not out.endswith("\n")


class TestCommentBannerZeroNoNewline:
    def test_default_ends_with_newline(_):
        out = _run(["cb0", "-w", "20"], "line 1\nline 2\n")
        assert out.endswith("\n")

    def test_no_newline_trims_only_trailing_newline(_):
        out = _run(["cb0", "-w", "20", "-N"], "line 1\nline 2\n")
        assert not out.endswith("\n")
        assert out.count("\n") == 3  # 4 banner lines, 3 internal breaks kept


class TestLoggerNoNewline:
    def test_default_ends_with_newline(_):
        name = uuid.uuid4().hex
        out = _run(["logger", "info", name], "a\nb\n")
        assert out.endswith("\n")

    def test_no_newline_trims_only_trailing_newline(_):
        name = uuid.uuid4().hex
        out = _run(["logger", "info", name, "-N"], "a\nb\n")
        assert not out.endswith("\n")
        assert out.count("\n") == 1  # break between records kept, tail cut

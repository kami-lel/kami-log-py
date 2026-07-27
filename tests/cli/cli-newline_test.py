"""
cli-newline_test.py

tests for the shared `-n/--newline`/`-N/--no-newline` flag's effect on the
`cb`, `cb0`, and `logger` CLI subcommands' printed output in `kamilog.py`
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


class TestCommentBannerNewline:
    def test_auto_keeps_single_trailing_newline_when_stdin_has_one(_):
        out = _run(["cb", "c", "=", "-w", "20"], "hi\n")
        assert out.endswith("\n") and not out.endswith("\n\n")

    def test_auto_appends_when_stdin_has_no_newline(_):
        out = _run(["cb", "c", "=", "-w", "20"], "hi")
        assert out.endswith("\n")

    def test_newline_forces_trailing_newline(_):
        out = _run(["cb", "c", "=", "-w", "20", "-n"], "hi\n")
        assert out.endswith("\n")

    def test_no_newline_forces_no_trailing_newline(_):
        out = _run(["cb", "c", "=", "-w", "20", "-N"], "hi")
        assert not out.endswith("\n")


class TestCommentBannerZeroNewline:
    def test_auto_keeps_single_trailing_newline_when_stdin_has_one(_):
        out = _run(["cb0", "-w", "20"], "line 1\nline 2\n")
        assert out.endswith("\n") and not out.endswith("\n\n")
        assert out.count("\n") == 4  # 4 banner lines, all kept

    def test_auto_appends_when_stdin_has_no_newline(_):
        out = _run(["cb0", "-w", "20"], "line 1\nline 2")
        assert out.endswith("\n")

    def test_newline_forces_trailing_newline(_):
        out = _run(["cb0", "-w", "20", "-n"], "line 1\nline 2\n")
        assert out.endswith("\n")

    def test_no_newline_forces_no_trailing_newline(_):
        out = _run(["cb0", "-w", "20", "-N"], "line 1\nline 2")
        assert not out.endswith("\n")
        assert out.count("\n") == 3  # 4 banner lines, 3 internal breaks kept


class TestLoggerNewline:
    def test_auto_keeps_single_trailing_newline_when_stdin_has_one(_):
        name = uuid.uuid4().hex
        out = _run(["logger", "info", name], "a\nb\n")
        assert out.endswith("\n") and not out.endswith("\n\n")
        assert out.count("\n") == 2  # both records keep their line break

    def test_auto_appends_when_stdin_has_no_newline(_):
        name = uuid.uuid4().hex
        out = _run(["logger", "info", name], "a\nb")
        assert out.endswith("\n")

    def test_newline_forces_trailing_newline(_):
        name = uuid.uuid4().hex
        out = _run(["logger", "info", name, "-n"], "a\nb\n")
        assert out.endswith("\n")

    def test_no_newline_forces_no_trailing_newline(_):
        name = uuid.uuid4().hex
        out = _run(["logger", "info", name, "-N"], "a\nb")
        assert not out.endswith("\n")
        assert out.count("\n") == 1  # break between records kept, tail cut

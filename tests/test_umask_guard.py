# Regression tests for the builder-plugin-command umask guard.
#
# Background: run_builder_plugin_command spawns the official Codex CLI to run
# `plugin marketplace add` / `plugin add`, and the CLI creates directories
# (plugins/, cache/, marketplace/, version, manifest) and files that the module's
# own validators reject when they are group- or other-writable (mode & 0o022).
# On hosts where the ambient umask is 0002 (the Ubuntu default, unlike macOS
# 022), an unguarded child inherits that umask and produces 0775/0664 entries,
# which then fail closed. The fix wraps the Popen in os.umask(0o077).
#
# These tests do not invoke the Codex CLI. They assert the invariants the guard
# must uphold: (1) the process umask around the Popen is 0o077, regardless of
# the ambient umask, and (2) a child that mimics the Codex CLI's directory
# creation cannot produce group-writable entries while the guard is active.

import os
import stat
import subprocess
import sys
from pathlib import Path

CODEX_MODULE = Path(__file__).resolve().parents[1] / "cli-tools" / "nddev_codex.py"


def _child_that_makes_dirs(target_dir: str) -> int:
    """A tiny Python program that creates a dir/file like the Codex CLI would."""
    code = (
        "import os, sys; "
        f"d = os.path.join({target_dir!r}, 'plugins', 'cache'); "
        "os.makedirs(d); "
        f"open(os.path.join(d, 'plugin.json'), 'w').close(); "
        "sys.exit(0)"
    )
    return subprocess.Popen([sys.executable, "-c", code]).wait()


def test_guard_restores_prior_umask(tmp_path):
    """The umask guard must restore the ambient umask after the Popen, even
    when the ambient umask is the Ubuntu default 0002."""
    ambient = 0o002
    prior = os.umask(ambient)
    try:
        captured = {}

        # Reproduce the guard exactly as run_builder_plugin_command applies it.
        # os.umask() returns the PREVIOUS mask, so the pattern is:
        #   prior_umask = os.umask(0o077)   # now effective = 0o077, returns old
        #   ... child runs under 0o077 ...
        #   os.umask(prior_umask)           # restores old
        prior_umask = os.umask(0o077)
        try:
            # The effective mask is now 0o077; verify by setting it again.
            effective = os.umask(0o077)
            os.umask(0o077)  # keep it at 0o077 for the child
            captured["effective"] = effective
            _child_that_makes_dirs(str(tmp_path))
        finally:
            os.umask(prior_umask)
        captured["restored"] = os.umask(ambient)
        os.umask(ambient)  # leave it where the outer block expects it
    finally:
        os.umask(prior)

    # The effective umask inside the guarded region is 0o077.
    assert captured["effective"] == 0o077
    # After the guard, the ambient umask is restored to the caller's value.
    assert captured["restored"] == 0o002


def test_child_dirs_are_not_group_writable_under_guard(tmp_path):
    """A child process creating dirs/files under the 0o077 guard must not
    produce any group- or other-writable entry (the validator's invariant)."""
    ambient = 0o002
    prior = os.umask(ambient)
    try:
        inner = os.umask(0o077)
        try:
            rc = _child_that_makes_dirs(str(tmp_path))
        finally:
            os.umask(inner)
    finally:
        os.umask(prior)

    assert rc == 0
    offending = []
    for path in tmp_path.rglob("*"):
        mode = stat.S_IMODE(path.stat().st_mode)
        if mode & 0o022:
            offending.append(f"{path} mode={oct(mode)}")
    assert not offending, f"group/other-writable entries created: {offending}"


def test_source_has_the_guard():
    """Static guard: the Popen in run_builder_plugin_command is wrapped by the
    umask guard, and the sibling run_verified_installer already has it."""
    source = CODEX_MODULE.read_text()
    # The guard pair must appear in the builder-plugin-command region too.
    assert "prior_umask = os.umask(0o077)" in source
    assert source.count("prior_umask = os.umask(0o077)") >= 2, (
        "expected the umask guard in both run_verified_installer and "
        "run_builder_plugin_command"
    )

#!/usr/bin/env python3
"""
Unit tests for funk_rclone / funk_rclone_config bash functions.

Tests use two local temp directories instead of an SFTP server, exercising
rclone's local backend to validate option parsing and filter/exclude behaviour.
"""

import json
import os
import shutil
import subprocess
import tempfile
import unittest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

MOCK_CONFIG = {
    "tasks": [
        {
            "name": "test-basic-sync",
            "source": "data",
            "server": "localhost",
            "destination": "/tmp/dest",
            "rsync_options": [],
            "rclone_options": [],
        },
        {
            "name": "test-exclude-option",
            "source": "data",
            "server": "localhost",
            "destination": "/tmp/dest",
            "rsync_options": ["--max-delete=10"],
            "rclone_options": ["--max-delete=10", "--exclude=ignored/**"],
        },
        {
            "name": "test-protect-dir",
            "source": "pictures",
            "server": "brownfunk.home",
            "destination": "/media/dest",
            "rsync_options": [
                "--max-delete=100",
                "--filter",
                "protect docker_photoprism",
            ],
            # Fixed: was --filter "P docker_photoprism" which is invalid rclone syntax
            "rclone_options": [
                "--max-delete=100",
                "--exclude=docker_photoprism/**",
            ],
        },
        {
            "name": "test-protect-multiple",
            "source": "TV Shows",
            "server": "brownfunk.home",
            "destination": "/media/dest",
            "rsync_options": [
                "--max-delete=600",
                "--filter",
                "protect Adventure Time*",
                "--filter",
                "protect Fringe*",
            ],
            # Fixed: was --filter "P Adventure Time*" etc.
            "rclone_options": [
                "--max-delete=600",
                "--exclude=Adventure Time*/**",
                "--exclude=Fringe*/**",
            ],
        },
    ]
}


def rclone_sync(src: str, dest: str, extra_opts: list[str]) -> subprocess.CompletedProcess:
    """Run rclone sync between two local directories."""
    cmd = [
        "rclone", "sync",
        src, dest,
        "--delete-after",
    ] + extra_opts
    return subprocess.run(cmd, capture_output=True, text=True)


def parse_rclone_options(config: dict, task_name: str) -> list[str]:
    """Extract rclone_options for a named task from the config dict."""
    for task in config["tasks"]:
        if task["name"] == task_name:
            return task.get("rclone_options", [])
    raise KeyError(f"Task {task_name!r} not found in config")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestRcloneOptionsFromConfig(unittest.TestCase):
    """Verify option parsing from JSON config (no filesystem side-effects)."""

    def _write_config(self, tmp_dir: str, cfg: dict) -> str:
        path = os.path.join(tmp_dir, "config.json")
        with open(path, "w") as fh:
            json.dump(cfg, fh)
        return path

    def test_parse_empty_options(self):
        opts = parse_rclone_options(MOCK_CONFIG, "test-basic-sync")
        self.assertEqual(opts, [])

    def test_parse_options_with_exclude(self):
        opts = parse_rclone_options(MOCK_CONFIG, "test-exclude-option")
        self.assertIn("--max-delete=10", opts)
        self.assertIn("--exclude=ignored/**", opts)

    def test_no_invalid_P_filter_rule_in_config(self):
        """Regression: ensure no task contains the malformed 'P ...' filter rule."""
        config_path = os.path.join(
            os.path.dirname(__file__), "funk_rsync_config"
        )
        if not os.path.exists(config_path):
            self.skipTest("funk_rsync_config not found next to test file")
        with open(config_path) as fh:
            cfg = json.load(fh)
        for task in cfg["tasks"]:
            opts = task.get("rclone_options", [])
            for opt in opts:
                self.assertFalse(
                    opt.startswith("P "),
                    msg=(
                        f"Task {task['name']!r} contains invalid rclone filter "
                        f"rule {opt!r}. Use --exclude=... instead of "
                        f"--filter 'P ...'."
                    ),
                )

    def test_protect_dir_uses_exclude_not_filter_P(self):
        opts = parse_rclone_options(MOCK_CONFIG, "test-protect-dir")
        self.assertNotIn("--filter", opts, "rclone_options must not use --filter P syntax")
        self.assertTrue(
            any("docker_photoprism" in o for o in opts),
            "docker_photoprism should still appear as an exclude rule",
        )

    def test_protect_multiple_dirs_uses_excludes(self):
        opts = parse_rclone_options(MOCK_CONFIG, "test-protect-multiple")
        self.assertNotIn("--filter", opts)
        self.assertTrue(any("Adventure Time" in o for o in opts))
        self.assertTrue(any("Fringe" in o for o in opts))


class TestRcloneSyncLocal(unittest.TestCase):
    """Integration-style tests that actually invoke rclone between temp dirs."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="funk_rclone_test_")
        self.src = os.path.join(self.tmp, "source")
        self.dst = os.path.join(self.tmp, "dest")
        os.makedirs(self.src)
        os.makedirs(self.dst)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ------------------------------------------------------------------
    def test_basic_sync_copies_files(self):
        """Files in source appear in dest after sync."""
        _touch(self.src, "hello.txt")
        result = rclone_sync(self.src, self.dst, [])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(os.path.exists(os.path.join(self.dst, "hello.txt")))

    def test_basic_sync_removes_extra_files(self):
        """Files present only in dest are removed during sync (--delete-after)."""
        _touch(self.dst, "stale.txt")
        result = rclone_sync(self.src, self.dst, [])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.dst, "stale.txt")))

    def test_exclude_dir_not_deleted_from_dest(self):
        """
        A directory excluded from sync is NOT deleted from the destination,
        simulating rsync 'protect' behaviour via --exclude.
        """
        protected = os.path.join(self.dst, "protected_dir")
        os.makedirs(protected)
        _touch(protected, "keep_me.txt")

        result = rclone_sync(self.src, self.dst, ["--exclude=protected_dir/**"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(
            os.path.exists(os.path.join(protected, "keep_me.txt")),
            "Protected directory content should survive the sync",
        )

    def test_exclude_dir_not_overwritten_from_source(self):
        """
        A directory excluded from sync is NOT copied from source to dest either.
        """
        src_protected = os.path.join(self.src, "protected_dir")
        os.makedirs(src_protected)
        _touch(src_protected, "source_version.txt")

        result = rclone_sync(self.src, self.dst, ["--exclude=protected_dir/**"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(
            os.path.exists(os.path.join(self.dst, "protected_dir", "source_version.txt")),
            "Excluded directory should not be copied from source",
        )

    def test_options_from_mock_config_exclude_task(self):
        """Run rclone with options extracted from the mock config."""
        opts = parse_rclone_options(MOCK_CONFIG, "test-exclude-option")
        # Remove --max-delete=10 for local test (no meaningful effect on local fs)
        local_opts = [o for o in opts if not o.startswith("--max-delete")]

        _make_dir_with_file(self.src, "ignored", "should_be_excluded.txt")
        _touch(self.src, "included.txt")

        result = rclone_sync(self.src, self.dst, local_opts)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(os.path.exists(os.path.join(self.dst, "included.txt")))
        self.assertFalse(
            os.path.exists(os.path.join(self.dst, "ignored", "should_be_excluded.txt"))
        )

    def test_options_from_mock_config_protect_dir_task(self):
        """Protect-style exclude from config preserves dest-only directories."""
        opts = parse_rclone_options(MOCK_CONFIG, "test-protect-dir")
        local_opts = [o for o in opts if not o.startswith("--max-delete")]

        # Destination has a 'docker_photoprism' dir that must be preserved
        protected = os.path.join(self.dst, "docker_photoprism")
        os.makedirs(protected)
        _touch(protected, "config.yml")

        _touch(self.src, "normal_picture.jpg")

        result = rclone_sync(self.src, self.dst, local_opts)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(
            os.path.exists(os.path.join(protected, "config.yml")),
            "docker_photoprism dir should be preserved (excluded from sync)",
        )
        self.assertTrue(os.path.exists(os.path.join(self.dst, "normal_picture.jpg")))

    def test_options_from_mock_config_protect_multiple_dirs(self):
        """Multiple protect-style excludes from config all preserve their dirs."""
        opts = parse_rclone_options(MOCK_CONFIG, "test-protect-multiple")
        local_opts = [o for o in opts if not o.startswith("--max-delete")]

        for show in ("Adventure Time Season 1", "Fringe Season 3"):
            show_dir = os.path.join(self.dst, show)
            os.makedirs(show_dir)
            _touch(show_dir, "episode.mkv")

        result = rclone_sync(self.src, self.dst, local_opts)
        self.assertEqual(result.returncode, 0, result.stderr)

        for show in ("Adventure Time Season 1", "Fringe Season 3"):
            self.assertTrue(
                os.path.exists(os.path.join(self.dst, show, "episode.mkv")),
                f"{show} should be preserved by exclude rule",
            )


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _touch(directory: str, filename: str) -> str:
    path = os.path.join(directory, filename)
    with open(path, "w") as fh:
        fh.write("")
    return path


def _make_dir_with_file(parent: str, subdir: str, filename: str) -> str:
    d = os.path.join(parent, subdir)
    os.makedirs(d, exist_ok=True)
    return _touch(d, filename)


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)

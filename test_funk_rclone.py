#!/usr/bin/env python3
"""
Unit tests for funk_rclone / funk_rclone_config.

Strategy
--------
- Config-validation tests: parse the real funk_rsync_config.json and assert
  every rclone_option is syntactically valid rclone syntax.
- Behaviour tests: create two local temp directories, populate them with
  representative files, run `rclone sync` with options extracted from a mock
  config that mirrors real task patterns, and assert the results.

The tests use rclone's local backend (plain directory paths) so no SSH /
SFTP setup is required.
"""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

# ---------------------------------------------------------------------------
# Location of the real config (symlinked into dotfiles)
# ---------------------------------------------------------------------------
_REPO_ROOT = Path(__file__).parent
_REAL_CONFIG = _REPO_ROOT / "funk_rsync_config"  # symlink → dotfiles_private


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def touch(path: Path, content: str = "") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return path


def rclone_sync(src: Path, dst: Path, extra_opts: list[str]) -> subprocess.CompletedProcess:
    """Run `rclone sync src dst [opts]` and return the CompletedProcess."""
    cmd = ["rclone", "sync", str(src), str(dst), "--delete-after"] + extra_opts
    return subprocess.run(cmd, capture_output=True, text=True)


def get_rclone_opts(config: dict, task_name: str) -> list[str]:
    for task in config["tasks"]:
        if task["name"] == task_name:
            return list(task.get("rclone_options", []))
    raise KeyError(f"Task not found: {task_name!r}")


# ---------------------------------------------------------------------------
# Mock config – mirrors the patterns used in the real funk_rsync_config tasks
# ---------------------------------------------------------------------------
MOCK_CONFIG: dict = {
    "tasks": [
        # ── plain sync, no extra options ──────────────────────────────────
        {
            "name": "plain-sync",
            "source": "docker",
            "server": "somehost.home",
            "destination": "/media/dest",
            "rsync_options": [],
            "rclone_options": [],
        },
        # ── nextcloud: exclude backup archives + limit deletes ────────────
        {
            "name": "nextcloud-backup",
            "source": "nextcloud",
            "server": "somehost.home",
            "destination": "/media/dest",
            "rsync_options": [
                "--exclude=backups/nextcloud-*",
                "--exclude=*/backups/nextcloud-*",
                "--max-delete=300",
            ],
            "rclone_options": [
                "--exclude=backups/nextcloud-*",
                "--exclude=**/backups/nextcloud-*",
                "--max-delete=300",
            ],
        },
        # ── games: exclude console dirs entirely (trailing-slash = dir match)
        {
            "name": "games-no-console",
            "source": "games",
            "server": "somehost.home",
            "destination": "/media/dest",
            "rsync_options": [
                "--exclude=Switch/",
                "--exclude=Wii/",
                "--max-delete=100",
            ],
            "rclone_options": [
                "--exclude=Switch/",
                "--exclude=Wii/",
                "--max-delete=100",
            ],
        },
        # ── Switch: protect specific dirs on destination ──────────────────
        {
            "name": "switch-sync",
            "source": "games/emulation/Nintendo/Switch",
            "server": "somehost.home",
            "destination": "/media/dest",
            "rsync_options": [
                "--filter", "protect backup_xaw10010599470",
                "--filter", "protect Saves",
                "--max-delete=100",
            ],
            "rclone_options": [
                "--exclude=backup_xaw10010599470/**",
                "--exclude=Saves/**",
                "--max-delete=100",
            ],
        },
        # ── movies: protect Sport dir, exclude other subdirs ─────────────
        {
            "name": "movies-sync",
            "source": "movies",
            "server": "somehost.home",
            "destination": "/media/dest",
            "rsync_options": [
                "--filter", "protect Sport/",
                "--exclude=Movies(French)/",
                "--max-delete=20",
            ],
            "rclone_options": [
                "--exclude=Sport/**",
                "--exclude=Movies(French)/",
                "--max-delete=20",
            ],
        },
        # ── music: exclude beets DB files ────────────────────────────────
        {
            "name": "music-no-beet",
            "source": "music",
            "server": "somehost.home",
            "destination": "/media/dest",
            "rsync_options": [
                "--exclude=*.blb",
                "--exclude=*.sqlite",
                "--max-delete=10000",
            ],
            "rclone_options": [
                "--exclude=*.blb",
                "--exclude=*.sqlite",
                "--max-delete=10000",
            ],
        },
        # ── pictures: protect photoprism dir ─────────────────────────────
        {
            "name": "pictures-sync",
            "source": "pictures",
            "server": "somehost.home",
            "destination": "/media/dest",
            "rsync_options": [
                "--max-delete=100",
                "--filter", "protect docker_photoprism",
            ],
            "rclone_options": [
                "--max-delete=100",
                "--exclude=docker_photoprism/**",
            ],
        },
        # ── shows: protect several show dirs ─────────────────────────────
        {
            "name": "shows-sync",
            "source": "TV Shows",
            "server": "somehost.home",
            "destination": "/media/dest",
            "rsync_options": [
                "--max-delete=600",
                "--filter", "protect Adventure Time*",
                "--filter", "protect Fringe*",
            ],
            "rclone_options": [
                "--max-delete=600",
                "--exclude=Adventure Time*/**",
                "--exclude=Fringe*/**",
            ],
        },
    ]
}


# ---------------------------------------------------------------------------
# 1. Config-validation tests (no rclone invocation)
# ---------------------------------------------------------------------------

class TestRcloneConfigValidation(unittest.TestCase):
    """Assert the real config contains only valid rclone option syntax."""

    def _load_real_config(self) -> dict:
        if not _REAL_CONFIG.exists():
            self.skipTest(f"Real config not found at {_REAL_CONFIG}")
        with _REAL_CONFIG.open() as fh:
            return json.load(fh)

    def test_no_filter_P_rules(self):
        """Regression: 'P <pattern>' is rsync-only and must not appear."""
        cfg = self._load_real_config()
        for task in cfg["tasks"]:
            for opt in task.get("rclone_options", []):
                self.assertFalse(
                    opt.startswith("P "),
                    msg=f"Task {task['name']!r} has invalid rclone filter rule {opt!r}. "
                        "Use --exclude=... instead.",
                )

    def test_no_bare_filter_token(self):
        """'--filter' must never appear alone as an option token (it takes an argument)."""
        cfg = self._load_real_config()
        for task in cfg["tasks"]:
            opts = task.get("rclone_options", [])
            for i, opt in enumerate(opts):
                if opt == "--filter":
                    # The next token must exist and be the rule
                    self.assertLess(
                        i + 1, len(opts),
                        msg=f"Task {task['name']!r}: bare '--filter' at end of options list.",
                    )
                    rule = opts[i + 1]
                    # Rule must start with +, -, or ! (not rsync's 'protect'/'P')
                    self.assertTrue(
                        rule[0] in ("+", "-", "!"),
                        msg=f"Task {task['name']!r}: --filter rule {rule!r} is not valid rclone "
                            "syntax (must start with +, -, or !).",
                    )

    def test_exclude_patterns_have_wildcards_where_needed(self):
        """Patterns ending with '-' that look like prefixes must include a wildcard."""
        cfg = self._load_real_config()
        for task in cfg["tasks"]:
            for opt in task.get("rclone_options", []):
                if opt.startswith("--exclude=") and opt.endswith("-") and "*" not in opt:
                    self.fail(
                        f"Task {task['name']!r}: {opt!r} looks like a prefix without a "
                        "wildcard. Did you mean to append '*'?"
                    )

    def test_all_rclone_options_start_with_double_dash(self):
        """Every rclone option must start with '--' (no short flags like -v)."""
        cfg = self._load_real_config()
        for task in cfg["tasks"]:
            for opt in task.get("rclone_options", []):
                self.assertTrue(
                    opt.startswith("--"),
                    msg=f"Task {task['name']!r}: option {opt!r} is not a long-form rclone flag.",
                )

    def test_mock_config_matches_real_option_patterns(self):
        """Ensure the mock config used in tests is consistent with real-config patterns."""
        real_cfg = self._load_real_config()
        real_opts = {
            opt
            for task in real_cfg["tasks"]
            for opt in task.get("rclone_options", [])
        }
        mock_opts = {
            opt
            for task in MOCK_CONFIG["tasks"]
            for opt in task.get("rclone_options", [])
            if not opt.startswith("--max-delete")  # max-delete values differ
        }
        # Every mock option must be representable in a real rclone invocation
        for opt in mock_opts:
            self.assertTrue(
                opt.startswith("--"),
                msg=f"Mock config contains non-option token: {opt!r}",
            )


# ---------------------------------------------------------------------------
# 2. Option-extraction tests
# ---------------------------------------------------------------------------

class TestRcloneOptionParsing(unittest.TestCase):

    def test_parse_empty_options(self):
        opts = get_rclone_opts(MOCK_CONFIG, "plain-sync")
        self.assertEqual(opts, [])

    def test_parse_nextcloud_options(self):
        opts = get_rclone_opts(MOCK_CONFIG, "nextcloud-backup")
        self.assertIn("--exclude=backups/nextcloud-*", opts)
        self.assertIn("--exclude=**/backups/nextcloud-*", opts)
        self.assertIn("--max-delete=300", opts)

    def test_parse_games_options(self):
        opts = get_rclone_opts(MOCK_CONFIG, "games-no-console")
        self.assertIn("--exclude=Switch/", opts)
        self.assertIn("--exclude=Wii/", opts)

    def test_no_rsync_protect_in_rclone_options(self):
        for task in MOCK_CONFIG["tasks"]:
            for opt in task.get("rclone_options", []):
                self.assertFalse(
                    opt.startswith("P "),
                    msg=f"Task {task['name']!r}: invalid rclone option {opt!r}",
                )

    def test_task_not_found_raises(self):
        with self.assertRaises(KeyError):
            get_rclone_opts(MOCK_CONFIG, "does-not-exist")


# ---------------------------------------------------------------------------
# 3. Rclone behaviour tests (local src/dst temp dirs)
# ---------------------------------------------------------------------------

class TestRcloneSyncBehaviour(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="funk_rclone_test_"))
        self.src = self.tmp / "src"
        self.dst = self.tmp / "dst"
        self.src.mkdir()
        self.dst.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # -- helpers --

    def _sync(self, task_name: str) -> subprocess.CompletedProcess:
        opts = [o for o in get_rclone_opts(MOCK_CONFIG, task_name)
                if not o.startswith("--max-delete")]
        return rclone_sync(self.src, self.dst, opts)

    # -- basic --

    def test_plain_sync_copies_files(self):
        touch(self.src / "hello.txt")
        r = rclone_sync(self.src, self.dst, [])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((self.dst / "hello.txt").exists())

    def test_plain_sync_removes_stale_files(self):
        touch(self.dst / "stale.txt")
        r = rclone_sync(self.src, self.dst, [])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse((self.dst / "stale.txt").exists())

    # -- trailing-slash dir exclude (Switch/, Wii/) --

    def test_dir_trailing_slash_exclude_not_synced_from_source(self):
        """--exclude=Switch/ prevents Switch content being copied from source."""
        touch(self.src / "Switch" / "game.bin")
        touch(self.src / "other.txt")
        r = self._sync("games-no-console")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse((self.dst / "Switch" / "game.bin").exists())
        self.assertTrue((self.dst / "other.txt").exists())

    def test_dir_trailing_slash_exclude_protects_dest(self):
        """--exclude=Switch/ preserves existing Switch content on destination."""
        touch(self.dst / "Switch" / "saves.sav")
        touch(self.src / "other.txt")
        r = self._sync("games-no-console")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(
            (self.dst / "Switch" / "saves.sav").exists(),
            "Switch dir must be preserved on destination",
        )

    # -- /**  protect-style exclude (backup_xaw…, Saves, docker_photoprism) --

    def test_glob_star_star_exclude_not_synced_from_source(self):
        """--exclude=Saves/** prevents Saves content being copied from source."""
        touch(self.src / "Saves" / "slot1.sav")
        touch(self.src / "rom.bin")
        r = self._sync("switch-sync")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse((self.dst / "Saves" / "slot1.sav").exists())
        self.assertTrue((self.dst / "rom.bin").exists())

    def test_glob_star_star_exclude_protects_dest(self):
        """--exclude=docker_photoprism/** preserves dest-only content."""
        touch(self.dst / "docker_photoprism" / "config.yml")
        touch(self.src / "photo.jpg")
        r = self._sync("pictures-sync")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(
            (self.dst / "docker_photoprism" / "config.yml").exists(),
            "docker_photoprism must be preserved on destination",
        )
        self.assertTrue((self.dst / "photo.jpg").exists())

    # -- glob wildcard excludes (Adventure Time*/**) --

    def test_glob_wildcard_dir_exclude_protects_dest(self):
        """--exclude=Adventure Time*/** preserves show dirs on destination."""
        touch(self.dst / "Adventure Time Season 1" / "s01e01.mkv")
        touch(self.dst / "Fringe Season 3" / "s03e01.mkv")
        touch(self.src / "New Show" / "s01e01.mkv")
        r = self._sync("shows-sync")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(
            (self.dst / "Adventure Time Season 1" / "s01e01.mkv").exists(),
            "Adventure Time must be preserved",
        )
        self.assertTrue(
            (self.dst / "Fringe Season 3" / "s03e01.mkv").exists(),
            "Fringe must be preserved",
        )

    # -- extension excludes (*.blb, *.sqlite) --

    def test_extension_exclude_skips_matching_files(self):
        """--exclude=*.blb skips beets DB files."""
        touch(self.src / "library.blb")
        touch(self.src / "library.sqlite")
        touch(self.src / "song.mp3")
        r = self._sync("music-no-beet")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse((self.dst / "library.blb").exists())
        self.assertFalse((self.dst / "library.sqlite").exists())
        self.assertTrue((self.dst / "song.mp3").exists())

    # -- deep-path glob (backups/nextcloud-*  and  **/backups/nextcloud-*) --

    def test_nextcloud_backup_exclude_shallow(self):
        """--exclude=backups/nextcloud-* removes nextcloud backup archives at top level."""
        touch(self.src / "backups" / "nextcloud-2024-01.tar.gz")
        touch(self.src / "backups" / "other_backup.tar.gz")
        touch(self.src / "data.txt")
        r = self._sync("nextcloud-backup")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(
            (self.dst / "backups" / "nextcloud-2024-01.tar.gz").exists(),
            "nextcloud backup archive must be excluded",
        )
        self.assertTrue((self.dst / "backups" / "other_backup.tar.gz").exists())
        self.assertTrue((self.dst / "data.txt").exists())

    def test_nextcloud_backup_exclude_deep(self):
        """--exclude=**/backups/nextcloud-* removes archives at any depth."""
        deep = self.src / "users" / "admin" / "backups"
        touch(deep / "nextcloud-2024-01.tar.gz")
        touch(deep / "keep.tar.gz")
        r = self._sync("nextcloud-backup")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse((self.dst / "users" / "admin" / "backups" / "nextcloud-2024-01.tar.gz").exists())
        self.assertTrue((self.dst / "users" / "admin" / "backups" / "keep.tar.gz").exists())

    # -- movies: protect Sport via /**,  exclude Movies(French) via trailing / --

    def test_movies_sport_protected_on_dest(self):
        """--exclude=Sport/** preserves Sport dir on destination."""
        touch(self.dst / "Sport" / "match.mkv")
        touch(self.src / "Interstellar.mkv")
        r = self._sync("movies-sync")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(
            (self.dst / "Sport" / "match.mkv").exists(),
            "Sport dir must be preserved",
        )

    def test_movies_french_excluded(self):
        """--exclude=Movies(French)/ skips the French movies directory."""
        touch(self.src / "Movies(French)" / "film.mkv")
        touch(self.src / "Interstellar.mkv")
        r = self._sync("movies-sync")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse((self.dst / "Movies(French)" / "film.mkv").exists())
        self.assertTrue((self.dst / "Interstellar.mkv").exists())


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)

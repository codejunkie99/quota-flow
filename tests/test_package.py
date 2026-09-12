import json
import os
from pathlib import Path
import subprocess
import tempfile
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_profiles_pin_distinct_routes(self):
        expected = {
            "quota_sol": ("gpt-5.6-sol", "openai", "medium"),
            "quota_sol_deep": ("gpt-5.6-sol", "openai", "high"),
            "quota_flash": ("opencode-go/deepseek-v4.1-flash", "codex-router", "high"),
            "quota_luna": ("gpt-5.6-luna", "openai", "low"),
        }
        seen = set()
        for path in (ROOT / "agents").glob("*.toml"):
            data = tomllib.loads(path.read_text())
            seen.add(data["name"])
            self.assertEqual(
                tuple(data[key] for key in ("model", "model_provider", "model_reasoning_effort")),
                expected[data["name"]],
            )
            self.assertTrue(data["description"])
            self.assertTrue(data["developer_instructions"])
            self.assertNotIn("approval_policy", data)
        self.assertEqual(seen, set(expected))

    def test_launcher_forwards_task_literally(self):
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            stub = tmp / "codex"
            stub.write_text("#!/usr/bin/env python3\nimport json,sys\nprint(json.dumps(sys.argv[1:]))\n")
            stub.chmod(0o755)
            task = "Fix '$HOME' and $(touch SHOULD_NOT_EXIST); keep `literal`"
            env = dict(os.environ, PATH=str(tmp) + os.pathsep + os.environ["PATH"])
            run = subprocess.run([str(ROOT / "bin/quota-flow"), task], env=env,
                                 cwd=tmp, capture_output=True, text=True, check=True)
            args = json.loads(run.stdout)
            self.assertEqual(args[-1], "Use $quota-flow for this task: " + task)
            self.assertIn("gpt-6-astra", args)
            self.assertIn('model_provider="openai"', args)
            self.assertIn('model_reasoning_effort="low"', args)
            self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", args)
            self.assertFalse((tmp / "SHOULD_NOT_EXIST").exists())

    def test_launcher_without_task_does_not_run_codex(self):
        run = subprocess.run([str(ROOT / "bin/quota-flow")], capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)
        self.assertIn("Usage:", run.stderr)


if __name__ == "__main__":
    unittest.main()

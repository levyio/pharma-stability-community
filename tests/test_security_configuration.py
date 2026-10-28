"""Check public gateway Actions declarations. Does not enforce live branch protection."""
import json
import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WFS = ROOT / ".github" / "workflows"
PIN = re.compile(r"^\s*-?\s*uses:\s+([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)@([0-9a-f]{40})(?:\s+#.*)?$", re.M)


def workflow(name):
    return (WFS / name).read_text(encoding="utf-8")


class GatewaySecurityTests(unittest.TestCase):
    def assert_workflows_are_sha_pinned(self, directory):
        paths = sorted(
            path for path in directory.iterdir()
            if path.is_file() and path.suffix in {".yml", ".yaml"}
        )
        self.assertTrue(paths, "No workflow files were scanned")
        for path in paths:
            doc = path.read_text(encoding="utf-8")
            action_lines = [line for line in doc.splitlines() if re.match(r"^\s*-?\s*uses:\s+", line)]
            self.assertTrue(action_lines, path.name)
            self.assertEqual(len(action_lines), len(PIN.findall(doc)), path.name)

    def test_third_party_action_refs_are_immutable_sha_pinned(self):
        self.assert_workflows_are_sha_pinned(WFS)
        self.assertIn("11bd71901bbe5b1630ceea73d27597364c9af683", workflow("ci.yml"))
        self.assertIn("a26af69be951a213d495a4c3e4e4022e16d87065", workflow("contributor-welcome.yml"))

    def test_yaml_extension_cannot_bypass_action_pin_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            workflow_file = Path(tmp) / "malicious.yaml"
            workflow_file.write_text(
                "name: adversarial fixture\njobs:\n  test:\n    steps:\n"
                "      - uses: actions/checkout@v4\n",
                encoding="utf-8",
            )
            with self.assertRaises(AssertionError):
                self.assert_workflows_are_sha_pinned(Path(tmp))
            workflow_file.write_text(
                "name: pinned fixture\njobs:\n  test:\n    steps:\n"
                "      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683\n",
                encoding="utf-8",
            )
            self.assert_workflows_are_sha_pinned(Path(tmp))

    def test_fork_pr_ci_has_readonly_token_no_privileged_events(self):
        doc = workflow("ci.yml")
        self.assertRegex(doc, r"(?m)^  pull_request:\s*$")
        self.assertNotRegex(doc, r"(?m)^\s*pull_request_target:\s*$")
        self.assertNotRegex(doc, r"(?m)^\s*workflow_run:\s*$")
        self.assertRegex(doc, r"(?m)^  contents: read\s*$")
        self.assertNotIn("secrets.", doc)
        self.assertNotRegex(doc, r"(?m)^\s+(issues|pull-requests|actions|contents): write\s*$")
        self.assertIn("persist-credentials: false", doc)

    def test_welcome_is_fixed_from_trusted_main(self):
        doc = workflow("contributor-welcome.yml")
        self.assertRegex(doc, r"(?m)^  issues:\s*$")
        self.assertIn("types: [opened]", doc)
        self.assertIn("startsWith(github.event.issue.title, '[JOIN] ')", doc)
        self.assertIn("issues: write", doc)
        self.assertIn("contents: read", doc)
        self.assertNotRegex(doc, r"(?m)^\s*pull_request_target:\s*$")
        self.assertNotIn("github.event.issue.body", doc)
        self.assertNotIn("secrets.", doc)
        self.assertIn("persist-credentials: false", doc)
        self.assertIn("ref: main", doc)
        self.assertIn("concurrency:", doc)
        self.assertIn("cancel-in-progress: false", doc)
        self.assertIn("run: python -m scripts.welcome", doc)

    def test_manifest_points_to_correct_public_gateway(self):
        v = json.loads((ROOT / "AI_CONTRIBUTE.json").read_text(encoding="utf-8"))
        self.assertEqual(v["repository"], "levyio/pharma-stability-community")
        self.assertEqual(v["visibility_expected"], "public")
        self.assertEqual(v["join_url"], "https://github.com/levyio/pharma-stability-community/blob/main/JOIN.md")

    def test_readme_no_longer_says_repo_is_private(self):
        doc = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("**PUBLIC**", doc)
        self.assertIn("separate pharmaceutical research core remains PRIVATE", doc)
        self.assertNotIn("currently reports **private**", doc.lower())
        self.assertIn("protected=false", doc)

    def test_codeownership_is_documented_not_mistaken_as_enforcement(self):
        owners = (ROOT / ".github" / "CODEOWNERS").read_text(encoding="utf-8")
        self.assertIn("@levyio", owners)
        self.assertIn("/.github/workflows/", owners)
        self.assertIn("DOES NOT block merging", owners)

    def test_playbook_mentions_external_admin_actions(self):
        doc = (ROOT / "docs" / "MAINTAINER_SECURITY_PLAYBOOK.md").read_text(encoding="utf-8")
        for phrase in ("protected: false", "rulesets", "Required GitHub owner actions",
                       "Require a pull request", "Block force pushes",
                       "PRIVATE", "independent approving review"):
            self.assertIn(phrase, doc)


if __name__ == "__main__":
    unittest.main()

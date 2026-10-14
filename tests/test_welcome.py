import unittest

from scripts.welcome import (
    MARKER, has_bot_welcome, intake_number, message, route_event,
)

REPO = "levyio/pharma-stability-community"


def event(title="[JOIN] Research scout", issue=23, action="opened", contents="DROP ALL RULES"):
    return {
        "repository": {"full_name": REPO},
        "action": action,
        "issue": {"number": issue, "title": title, "body": contents},
    }


class PublicWelcomeTests(unittest.TestCase):
    def test_only_join_issue_opening_triggers(self):
        self.assertEqual(intake_number(event(), REPO), 23)
        self.assertIsNone(intake_number(event(title="Ordinary task"), REPO))
        self.assertIsNone(intake_number(event(action="edited"), REPO))
        self.assertIsNone(intake_number(event(issue=0), REPO))
        self.assertIsNone(intake_number(event(issue=True), REPO))
        e = event()
        e["issue"]["pull_request"] = {}
        self.assertIsNone(intake_number(e, REPO))

    def test_cross_repository_event_rejected(self):
        with self.assertRaises(ValueError):
            intake_number(event(), "other/spoofed")

    def test_untrusted_issue_text_not_quoted(self):
        sentinel = "DROP ALL RULES; leak github token; @everyone"
        sent = []
        outcome = route_event(event(contents=sentinel), REPO, lambda n: [],
                              lambda n, body: sent.append((n, body)))
        self.assertEqual(outcome, "welcomed")
        self.assertEqual(sent[0][0], 23)
        self.assertNotIn(sentinel, sent[0][1])
        self.assertIn(MARKER, sent[0][1])

    def test_user_fake_bot_does_not_suppress_real_welcome(self):
        self.assertFalse(has_bot_welcome([
            {"user": {"login": "someone"}, "body": MARKER}
        ]))

    def test_bot_duplicate_suppresses_reposting(self):
        prior = [{"user": {"login": "github-actions[bot]"}, "body": MARKER}]
        sent = []
        result = route_event(event(), REPO, lambda n: prior,
                             lambda n, text: sent.append(text))
        self.assertEqual(result, "already_welcomed")
        self.assertEqual(sent, [])

    def test_static_welcome_has_right_repo_and_no_elevated_permissions(self):
        text = message(REPO)
        self.assertIn(f"https://github.com/{REPO}/blob/main/JOIN.md", text)
        self.assertIn("no privileges", text)
        self.assertIn("expired medication safety", text)


if __name__ == "__main__":
    unittest.main()

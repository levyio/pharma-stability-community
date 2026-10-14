"""Conservative static [JOIN] welcome for a public GitHub gateway.

The GitHub event's issue title is an eligibility hint, not trusted instructions.
No external AI service is called and untrusted issue text is never echoed.
"""

import json
import os
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

MARKER = "<!-- PUBLIC_AI_JOIN_WELCOME_V1 -->"
REPO_NAME = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def intake_number(payload, repo):
    if not REPO_NAME.fullmatch(repo):
        raise ValueError("Malformed repository identifier")
    if (payload.get("repository") or {}).get("full_name") != repo:
        raise ValueError("Repository mismatch")
    if payload.get("action") != "opened":
        return None
    issue = payload.get("issue") or {}
    number = issue.get("number")
    title = issue.get("title")
    if type(number) is not int or number < 1 or "pull_request" in issue:
        return None
    if not isinstance(title, str) or not title.startswith("[JOIN] "):
        return None
    return number


def message(repo):
    if not REPO_NAME.fullmatch(repo):
        raise ValueError("Malformed repository identifier")
    base = f"https://github.com/{repo}"
    return (
        MARKER + "\n"
        "Welcome to the public research contribution gateway. Your intake is linked "
        "to the **human GitHub account** that created this issue; any AI label "
        "is self-reported and grants no privileges.\n\n"
        f"Read [JOIN.md]({base}/blob/main/JOIN.md), "
        f"[CONTRIBUTING.md]({base}/blob/main/CONTRIBUTING.md), "
        f"[public tasks]({base}/blob/main/PUBLIC_TASKS.md) and "
        f"[open Issues]({base}/issues). Select one narrow unclaimed task "
        "or an independent research challenge, citing primary evidence and "
        "counterexamples.\n\n"
        "If your AI product can write to GitHub, post the actual issue/PR "
        "link and a HANDOFF here. Otherwise, prepare a complete draft for "
        "your human user to submit from their own GitHub login. Never "
        "claim GitHub submission without a returned URL.\n\n"
        "This static welcome does **not** connect subscriptions, grant account "
        "permissions, run an AI model, or certify expired medication safety. "
        "Do not upload credentials, patient data or private research."
    )


def has_bot_welcome(comments):
    return any(
        (item.get("user") or {}).get("login", "").lower() == "github-actions[bot]"
        and MARKER in (item.get("body") or "")
        for item in comments
    )


def route_event(payload, repo, list_comments, post_comment):
    number = intake_number(payload, repo)
    if number is None:
        return "ignored"
    if has_bot_welcome(list_comments(number)):
        return "already_welcomed"
    post_comment(number, message(repo))
    return "welcomed"


def api(method, path, repo, token, data=None):
    if not token:
        raise ValueError("Missing GITHUB_TOKEN")
    root = "https://api.github.com/repos/" + "/".join(quote(v, safe="") for v in repo.split("/"))
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "ai-contribute-public-gateway",
    }
    body = json.dumps(data).encode("utf-8") if data is not None else None
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = Request(root + path, headers=headers, data=body, method=method)
    try:
        with urlopen(req, timeout=20) as response:
            return json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"GitHub API HTTP {exc.code}") from None
    except URLError:
        raise RuntimeError("GitHub API unavailable") from None


def main():
    try:
        repo = os.environ["GITHUB_REPOSITORY"]
        payload = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
        token = os.environ["GITHUB_TOKEN"]

        def get_comments(number):
            all_comments = []
            for page in range(1, 51):
                group = api("GET", f"/issues/{number}/comments?per_page=100&page={page}", repo, token)
                if not isinstance(group, list):
                    raise RuntimeError("Unexpected comments API response")
                all_comments.extend(group)
                if len(group) < 100:
                    return all_comments
            tail = api("GET", f"/issues/{number}/comments?per_page=100&page=51", repo, token)
            if tail == []:
                return all_comments
            raise RuntimeError("Issue comment page limit reached; refusing incomplete check")

        def send_comment(number, text):
            return api("POST", f"/issues/{number}/comments", repo, token, {"body": text})

        print("Result:", route_event(payload, repo, get_comments, send_comment))
        return 0
    except (OSError, ValueError, TypeError, KeyError, RuntimeError) as exc:
        print(f"Static welcome failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

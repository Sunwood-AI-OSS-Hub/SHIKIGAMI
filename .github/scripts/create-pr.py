#!/usr/bin/env python3
"""Create PR from Issue with Claude Code."""

import json
import os
import re
import subprocess
import sys
import urllib.parse


def run_command(cmd: list[str]) -> str:
    """Run command and return output."""
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return result.stdout.strip()


def main():
    branch_name = sys.argv[1]
    issue_number = sys.argv[2]

    # オプション: タスクサマリーを含めるかどうか（デフォルトはtrue）
    include_task_summary = os.getenv("INCLUDE_TASK_SUMMARY", "true").lower() == "true"

    print(f"[DEBUG] Branch name: {branch_name}", file=sys.stderr)
    print(f"[DEBUG] Issue number: {issue_number}", file=sys.stderr)
    print(f"[DEBUG] Include task summary: {include_task_summary}", file=sys.stderr)

    # Check if PR already exists
    pr_list_output = run_command([
        "gh", "pr", "list",
        "--head", branch_name,
        "--json", "number",
        "--jq", ". | length > 0"
    ])
    if pr_list_output == "true":
        print(f"PR already exists for branch {branch_name}, skipping...")
        return

    # Get commit message from branch (get all commits, separated by null char)
    commits = run_command([
        "git", "log", f"origin/main..{branch_name}",
        "--pretty=format:%B%x00", "--reverse"
    ])
    # Get first commit (split by null character)
    commit_body = commits.split("\x00")[0].strip() if commits else ""
    print(f"[DEBUG] Commit body:\n{commit_body}", file=sys.stderr)

    # Get Claude's latest comment
    issue_data = run_command([
        "gh", "issue", "view", issue_number,
        "--json", "comments", "--jq", ".comments"
    ])
    comments = json.loads(issue_data) if issue_data else []
    claude_comment = ""
    for comment in reversed(comments):
        # Claude bot's login is "claude" (not "claude[bot]")
        if comment.get("author", {}).get("login") == "claude":
            claude_comment = comment.get("body", "")
            break
    print(f"[DEBUG] Claude comment (first 200 chars): {claude_comment[:200] if claude_comment else '(empty)'}...", file=sys.stderr)

    # タスクサマリー（---より後ろの部分）を抽出
    task_summary = ""
    if include_task_summary and claude_comment:
        if "---" in claude_comment:
            # 最初の---より後ろの部分を取得
            parts = claude_comment.split("---", 1)
            if len(parts) > 1:
                task_summary = parts[1].strip()
                # 余分な改行を削除
                task_summary = re.sub(r'\n{3,}', '\n\n', task_summary)

    # Try to extract Create PR URL
    create_pr_url = ""
    if claude_comment:
        match = re.search(r'\[Create PR[^\]]*\]\((https[^)]+)\)', claude_comment)
        if match:
            create_pr_url = match.group(1)
    print(f"[DEBUG] Create PR URL: {create_pr_url[:100] if create_pr_url else '(empty)'}...", file=sys.stderr)

    if create_pr_url:
        # Extract title and body from URL
        parsed = urllib.parse.urlparse(create_pr_url)
        params = urllib.parse.parse_qs(parsed.query)
        pr_title = urllib.parse.unquote(params.get("title", [""])[0])
        pr_body = urllib.parse.unquote(params.get("body", [""])[0])
    else:
        # Fallback: use issue title and commit message
        issue_title = run_command([
            "gh", "issue", "view", issue_number,
            "--json", "title", "--jq", ".title"
        ])

        # Determine prefix based on issue title
        if any(word in issue_title for word in ["を作って", "を作成", "を追加"]):
            pr_prefix = "feat:"
        elif any(word in issue_title for word in ["を修正", "を直して"]):
            pr_prefix = "fix:"
        elif any(word in issue_title for word in ["を更新", "を変更"]):
            pr_prefix = "update:"
        else:
            pr_prefix = ""

        # Transform issue title
        final_title = issue_title
        for old, new in [("を作って", "を追加"), ("を作成", "を追加"), ("を追加$", "を追加する")]:
            final_title = re.sub(old, new, final_title)

        pr_title = f"{pr_prefix} {final_title}" if pr_prefix else final_title
        pr_body = commit_body or claude_comment

    # フッターが既に含まれているかチェック
    has_closes = f"Closes #{issue_number}" in pr_body
    has_generated = "Generated with [Claude Code]" in pr_body

    # Add footer
    footer_parts = []
    if not has_closes:
        footer_parts.append(f"Closes #{issue_number}")
    if not has_generated:
        footer_parts.append("Generated with [Claude Code](https://claude.ai/code)")

    # タスクサマリーを追加
    if task_summary:
        final_body = f"""{pr_body}

---

{task_summary}
"""
    else:
        final_body = pr_body

    # フッターを追加
    if footer_parts:
        final_body += f"\n\n---\n\n" + "\n\n".join(footer_parts)

    print(f"[DEBUG] PR title: {pr_title}", file=sys.stderr)
    print(f"[DEBUG] Task summary: {'included' if task_summary else '(empty)'}", file=sys.stderr)
    print(f"[DEBUG] PR body:\n{final_body}", file=sys.stderr)
    print(f"[DEBUG] PR body length: {len(final_body)}", file=sys.stderr)

    # Create PR
    subprocess.run([
        "gh", "pr", "create",
        "--base", "main",
        "--head", branch_name,
        "--title", pr_title,
        "--body", final_body,
    ])


if __name__ == "__main__":
    main()

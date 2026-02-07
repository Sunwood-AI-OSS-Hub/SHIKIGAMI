#!/usr/bin/env python3
"""Issueからキャラクターとタスクを抽出して、エージェントファイルをCLAUDE.mdにマージするスクリプト"""

import json
import re
import subprocess
import sys


def run_command(cmd: list[str]) -> str:
    """Run command and return output."""
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return result.stdout.strip()


def parse_issue_body(issue_body: str) -> dict:
    """Issue Bodyからキャラクターとタスクを抽出"""
    print(f"[DEBUG] Issue Body:\n{issue_body}", file=sys.stderr)

    # 「下記のキャラクターを演じて」の後ろにあるキャラクターファイルを抽出
    character_match = re.search(r'キャラクター[：:]\s*([^\n]+)', issue_body)
    character_file = character_match.group(1).strip() if character_match else None

    # 「下記のタスクを処理」の後ろにあるタスクを抽出
    task_match = re.search(r'タスク[：:]\s*([^\n]+)', issue_body)
    task = task_match.group(1).strip() if task_match else None

    print(f"[DEBUG] Character File: {character_file}", file=sys.stderr)
    print(f"[DEBUG] Task: {task}", file=sys.stderr)

    return {"character_file": character_file, "task": task}


def load_agent_file(character_file: str) -> str:
    """エージェントファイルを読み込む"""
    # `.github/agents/` または `.claude/agents/` を探索
    for base_path in [".github/agents", ".claude/agents", "agents"]:
        full_path = f"{base_path}/{character_file}"
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            print(f"[DEBUG] Loaded agent from: {full_path}", file=sys.stderr)
            return content
        except FileNotFoundError:
            continue

    print(f"[ERROR] Agent file not found: {character_file}", file=sys.stderr)
    return ""


def create_claude_md(character_content: str, task: str) -> str:
    """CLAUDE.mdを作成"""
    # YAML frontmatter部分を抽出（もしあれば）
    yaml_match = re.match(r'^---\n(.*?)\n---\n', character_content, re.DOTALL)
    if yaml_match:
        yaml_frontmatter = yaml_match.group(1)
        character_body = character_content[yaml_match.end():]
    else:
        yaml_frontmatter = ""
        character_body = character_content

    # タスクを追加
    task_section = f"""

## 現在のタスク
{task}
"""

    claude_md = f"""---
{yaml_frontmatter}
---

# キャラクター設定

{character_body}
{task_section}
"""

    return claude_md


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 .github/scripts/merge-agent.py <issue_number> <output_file>", file=sys.stderr)
        sys.exit(1)

    issue_number = sys.argv[1]
    output_file = sys.argv[2]

    # Issue Bodyを取得
    issue_body = run_command([
        "gh", "issue", "view", issue_number,
        "--json", "body", "--jq", ".body"
    ])

    if not issue_body:
        print("[ERROR] Could not get issue body", file=sys.stderr)
        sys.exit(1)

    # キャラクターとタスクを抽出
    parsed = parse_issue_body(issue_body)

    if not parsed["character_file"]:
        print("[INFO] No character specified, using default", file=sys.stderr)
        character_content = "# デフォルトキャラクター\n\nあなたは有用なアシスタントです。"
    else:
        character_content = load_agent_file(parsed["character_file"])

    if not parsed["task"]:
        print("[INFO] No task specified", file=sys.stderr)

    # CLAUDE.mdを作成
    claude_md = create_claude_md(character_content, parsed["task"] or "")

    # ファイルに書き込み
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(claude_md)

    print(f"[SUCCESS] Created {output_file}", file=sys.stderr)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_ROOT_FILES = (
    "START_HERE_FOR_AI.md",
    "AGENTS.md",
    "CLAUDE.md",
    "PROJECT_READY.json",
    "PROJECT_STATE.json",
    "CHECKPOINT_INDEX.json",
    "ACTIVE_WORK.json",
    "MILESTONE_INDEX.json",
    "docs/WORK_DONE_INDEX.md",
    "tools/project_resume.py",
)


def load_json(name: str, errors: list[str]) -> dict[str, Any]:
    path = ROOT / name
    if not path.is_file():
        errors.append(f"missing {name}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid {name}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{name} must be a JSON object")
        return {}
    return value


def git(*args: str) -> str:
    try:
        p = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=False)
    except OSError:
        return ""
    return p.stdout.strip() if p.returncode == 0 else ""


def env_branch() -> str:
    value = os.environ.get("PROJECT_RESUME_HEAD_REF", "").strip()
    return value.removeprefix("refs/heads/") if value else ""


def env_head() -> str:
    return os.environ.get("PROJECT_RESUME_HEAD_SHA", "").strip()


def validate_active_branch(name: str, ws: dict[str, Any], head_sha: str, errors: list[str]) -> None:
    if ws.get("status") == "blocked":
        errors.append(f"active workstream {name} is status=blocked: {ws.get('blocker', '')}")

    state_rel = ws.get("state_file")
    if not isinstance(state_rel, str) or not state_rel:
        errors.append(f"active workstream {name}: state_file required")
        return
    state_path = ROOT / state_rel
    if not state_path.is_file():
        errors.append(f"active workstream {name}: state file missing on branch: {state_rel}")
        return

    text = state_path.read_text(encoding="utf-8")
    for marker in (f"Workstream: {name}", "Workstream-State: current", "ONE NEXT ACTION"):
        if marker not in text:
            errors.append(f"active workstream {name}: state file missing marker {marker!r}")

    state_commit = git("log", "-1", "--format=%H", "--", state_rel)
    scopes = ws.get("scope_paths")
    if not re.fullmatch(r"[0-9a-f]{40}", state_commit):
        errors.append(f"active workstream {name}: cannot resolve state-file commit")
        return
    if not isinstance(scopes, list) or not scopes or not all(isinstance(v, str) and v for v in scopes):
        errors.append(f"active workstream {name}: scope_paths must be a non-empty string list")
        return

    target = head_sha if re.fullmatch(r"[0-9a-f]{40}", head_sha) else "HEAD"
    changed = git("diff", "--name-only", f"{state_commit}..{target}", "--", *scopes)
    stale = [line for line in changed.splitlines() if line.strip() and line.strip() != state_rel]
    if stale:
        errors.append(
            f"active workstream {name}: STATE is stale; scoped files changed after {state_commit[:8]}: "
            + ", ".join(stale[:12])
        )


def validate() -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_ROOT_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"required resume file missing: {rel}")

    start = ROOT / "START_HERE_FOR_AI.md"
    if start.is_file():
        text = start.read_text(encoding="utf-8")
        for marker in (
            "Resume-System-Version: 1.3",
            "before **any project answer",
            "ACTIVE_WORK.json",
            "project_resume.py",
            "RESUME_VERDICT=BLOCKER",
            "Do **not** continue feature/editorial work",
        ):
            if marker.casefold() not in text.casefold():
                errors.append(f"START_HERE_FOR_AI.md missing mandatory marker: {marker!r}")

    agents = ROOT / "AGENTS.md"
    if agents.is_file():
        text = agents.read_text(encoding="utf-8")
        if "START_HERE_FOR_AI.md" not in text or "before any" not in text.casefold():
            errors.append("AGENTS.md must require START_HERE_FOR_AI.md before any answer/plan/action")

    claude = ROOT / "CLAUDE.md"
    if claude.is_file() and "START_HERE_FOR_AI.md" not in claude.read_text(encoding="utf-8"):
        errors.append("CLAUDE.md must route through START_HERE_FOR_AI.md")

    ready = load_json("PROJECT_READY.json", errors)
    state = load_json("PROJECT_STATE.json", errors)
    active = load_json("ACTIVE_WORK.json", errors)
    milestones = load_json("MILESTONE_INDEX.json", errors)
    index = load_json("CHECKPOINT_INDEX.json", errors)

    if ready:
        if ready.get("entrypoint") != "START_HERE_FOR_AI.md":
            errors.append("PROJECT_READY.json entrypoint must be START_HERE_FOR_AI.md")
        if ready.get("status_file") != "PROJECT_STATE.json":
            errors.append("PROJECT_READY.json status_file must be PROJECT_STATE.json")
        questions = ready.get("questions")
        if isinstance(questions, dict):
            for q in ("current_state", "next_action"):
                spec = questions.get(q)
                if not isinstance(spec, dict) or spec.get("source") != "PROJECT_STATE.json":
                    errors.append(f"PROJECT_READY question {q} must source PROJECT_STATE.json")
        else:
            errors.append("PROJECT_READY questions missing")

    if state:
        if state.get("resume_system_version") != "1.3":
            errors.append("PROJECT_STATE resume_system_version must be 1.3")
        if state.get("active_work_registry") != "ACTIVE_WORK.json":
            errors.append("PROJECT_STATE active_work_registry must point to ACTIVE_WORK.json")
        if state.get("milestone_index") != "MILESTONE_INDEX.json":
            errors.append("PROJECT_STATE milestone_index must point to MILESTONE_INDEX.json")
        tracks = state.get("tracks", {})
        idx_tracks = index.get("tracks", {}) if isinstance(index, dict) else {}
        if isinstance(tracks, dict):
            for name, item in tracks.items():
                ix = idx_tracks.get(name, {}) if isinstance(idx_tracks, dict) else {}
                if isinstance(item, dict) and (not isinstance(ix, dict) or ix.get("latest_checkpoint") != item.get("latest_checkpoint")):
                    errors.append(f"track {name}: PROJECT_STATE/CHECKPOINT_INDEX mismatch")

    workstreams = active.get("workstreams") if active else None
    if active and active.get("resume_system_version") != "1.3":
        errors.append("ACTIVE_WORK resume_system_version must be 1.3")
    if active and not isinstance(workstreams, dict):
        errors.append("ACTIVE_WORK workstreams must be an object")
        workstreams = {}

    if isinstance(workstreams, dict):
        for name, ws in workstreams.items():
            if not isinstance(ws, dict):
                errors.append(f"ACTIVE_WORK {name}: entry must be an object")
                continue
            for field in ("status", "branch", "pull_request", "state_file", "scope_paths", "one_next_action"):
                if field not in ws:
                    errors.append(f"ACTIVE_WORK {name}: missing {field}")
            if ws.get("status") not in {"active", "blocked", "paused", "complete", "superseded"}:
                errors.append(f"ACTIVE_WORK {name}: unsupported status {ws.get('status')!r}")
            if not isinstance(ws.get("pull_request"), int):
                errors.append(f"ACTIVE_WORK {name}: pull_request must be integer")

    if milestones:
        if milestones.get("resume_system_version") != "1.3":
            errors.append("MILESTONE_INDEX resume_system_version must be 1.3")
        if not isinstance(milestones.get("milestones"), list):
            errors.append("MILESTONE_INDEX milestones must be an array")

    branch = env_branch()
    head = env_head()
    if branch and isinstance(workstreams, dict):
        for name, ws in workstreams.items():
            if isinstance(ws, dict) and ws.get("branch") == branch:
                validate_active_branch(name, ws, head, errors)

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        print(f"RESUME_GATE_ERRORS={len(errors)}")
        print("RESUME_GATE_VERDICT=BLOCKER")
        return 1
    print("RESUME_GATE_VERDICT=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# START HERE FOR AI — MANDATORY RESUME GATE

Resume-System-Version: 1.3

This is the first file for every AI/helper session in this repository.

The rule applies before **any project answer, plan, status summary, task choice, content proposal, graph/database architecture proposal, code review, code change, ingestion action, publication suggestion, or proposal to redo prior work**.

## Mandatory preflight

1. Establish exact Git branch/HEAD; fetch `origin` before trusting local refs.
2. Read `PROJECT_STATE.json` — canonical merged-main state.
3. Read `ACTIVE_WORK.json` — durable unmerged PR/branch work.
4. Read `CHECKPOINT_INDEX.json` — canonical checkpoint pointers.
5. Run `python3 tools/project_resume.py`.
6. If the user names a PR/branch/workstream, select it from `ACTIVE_WORK.json`; otherwise use `PROJECT_STATE.json.default_resume_track` unless another track is explicitly selected.
7. Read the selected current source/checkpoint and safety boundaries.
8. For “didn’t we already do this?” questions, inspect `MILESTONE_INDEX.json` / `docs/WORK_DONE_INDEX.md` before proposing reconstruction.

## Hard stop rules

STOP and report BLOCKER/DRIFT before continuing if:

- the resume command reports `RESUME_VERDICT=BLOCKER`;
- Project Ready Guard is red on the exact relevant head;
- a registered WIP branch has no current workstream `STATE.md`;
- meaningful scoped work exists after its registered state file;
- machine state/checkpoint/current sources contradict one another;
- a proposed fact, media license, source, or publication status cannot be verified.

Do **not** continue feature/editorial work merely because ordinary CI is green when the continuity/resume guard is red.

## Source hierarchy

1. exact GitHub branch/PR/main refs;
2. `PROJECT_STATE.json` for merged-main tracks;
3. `ACTIVE_WORK.json` for unmerged workstreams;
4. `CHECKPOINT_INDEX.json` + selected current source/checkpoint;
5. `MILESTONE_INDEX.json` / historical checkpoints as evidence;
6. chat history only as a hint that must be verified.

`PROJECT_STATUS.md` remains the detailed current narrative for main editorial work but cannot override machine current-state pointers.

## Editorial / knowledge safety

- Do not invent tea, producer, region, processing, history, or other factual claims.
- Draft/review content is not public merely because it exists in Git.
- Do not move content to `published` without the required editorial/fact/license verification.
- Never publish an image whose license/provenance is unresolved.
- Generated reverse links are not canonical source data.
- The legacy static JSON and Knowledge Graph are separate layers; do not assume one automatically updates the other.

## Session handoff

Merged-main work gets a dated checkpoint + state/index update. Unmerged PR/branch work gets a current `docs/workstreams/<workstream>/STATE.md` and matching `ACTIVE_WORK.json` entry. Important work is not handed off if it exists only in chat/local files or after a stale state file.

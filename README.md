# Skill Repo

Personal agent skills for reusable engineering workflows.

## Layout

```text
codex/
└─ skills/
   └─ refactor-doc-governance/
      ├─ SKILL.md
      └─ agents/
         └─ openai.yaml
```

Future agent-specific assets can live in sibling folders such as `claude/`, `cursor/`, or `gemini/` when needed.

## Skills

### Codex

- `refactor-doc-governance`: Guidance for long-running refactors, PRD/doc responsibility routing, dangerous-pattern checklists, and documentation normalization.

## Install Codex Skills

Copy a skill folder into your local Codex skills directory:

```powershell
Copy-Item -Recurse -Force .\codex\skills\refactor-doc-governance "$env:USERPROFILE\.codex\skills\refactor-doc-governance"
```

Then start a new Codex session or ensure the skill list reloads.

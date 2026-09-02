# Skill Repo

Personal agent skills for reusable engineering workflows.

## Layout

```text
codex/
├─ agents/
│  └─ luna-worker.toml
└─ skills/
   ├─ deepseek-codex-native/
   │  ├─ SKILL.md
   │  └─ agents/
   │     └─ openai.yaml
   ├─ system-design-governance/
   │  ├─ SKILL.md
   │  └─ agents/
   │     └─ openai.yaml
   └─ refactor-doc-governance/
      ├─ SKILL.md
      └─ agents/
         └─ openai.yaml
```

Future agent-specific assets can live in sibling folders such as `claude/`, `cursor/`, or `gemini/` when needed.

## Skills

### Codex

- `deepseek-codex-native`: Guidance for configuring DeepSeek as a native Codex model provider and creating GPT/DeepSeek switch scripts.
- `refactor-doc-governance`: Guidance for long-running refactors, PRD/doc responsibility routing, dangerous-pattern checklists, and documentation normalization.
- `sol-luna-dev`: Guidance for high-capability lead-agent planning, Luna worker implementation, and lead-agent review for code-changing tasks.
- `system-design-governance`: Guidance for new system design from requirements through architecture, constraints, implementation planning, coding, verification, progress, and decisions.

## Install Codex Skills

Copy a skill folder into your local Codex skills directory:

```powershell
Copy-Item -Recurse -Force .\codex\skills\deepseek-codex-native "$env:USERPROFILE\.codex\skills\deepseek-codex-native"
Copy-Item -Recurse -Force .\codex\skills\refactor-doc-governance "$env:USERPROFILE\.codex\skills\refactor-doc-governance"
Copy-Item -Recurse -Force .\codex\skills\sol-luna-dev "$env:USERPROFILE\.codex\skills\sol-luna-dev"
Copy-Item -Recurse -Force .\codex\skills\system-design-governance "$env:USERPROFILE\.codex\skills\system-design-governance"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\agents" | Out-Null
Copy-Item -Force .\codex\agents\luna-worker.toml "$env:USERPROFILE\.codex\agents\luna-worker.toml"
```

Then start a new Codex session or ensure the skill list reloads.

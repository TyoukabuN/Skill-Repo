# Skill Repo

Personal agent skills for reusable engineering workflows.

## Layout

```text
codex/
├─ agents/
│  └─ luna-worker.toml
└─ skills/
   ├─ ace-step-bgm/
   │  ├─ SKILL.md
   │  └─ references/
   │     ├─ ace-step-fields.md
   │     └─ bgm-playbook.md
   ├─ adaptive-project-development/
   │  ├─ SKILL.md
   │  ├─ agents/
   │  │  └─ openai.yaml
   │  ├─ assets/
   │  │  └─ templates/
   │  │     ├─ design.md
   │  │     ├─ implementation-plan.md
   │  │     ├─ prd.md
   │  │     ├─ tasks.md
   │  │     └─ verification.md
   │  └─ references/
   │     ├─ actiondbg-profile.md
   │     ├─ artifact-contracts.md
   │     ├─ readiness-and-review.md
   │     ├─ role-handoffs.md
   │     └─ workflow-routing.md
   ├─ community-research/
   │  ├─ SKILL.md
   │  ├─ agents/
   │  │  └─ openai.yaml
   │  ├─ references/
   │  │  ├─ deepseek.md
   │  │  └─ providers.md
   │  └─ scripts/
   │     └─ deepseek_web.py
   ├─ create-code-explain-doc/
   │  └─ SKILL.md
   ├─ deepseek-codex-native/
   │  ├─ SKILL.md
   │  └─ agents/
   │     └─ openai.yaml
   ├─ refactor-doc-governance/
   │  ├─ SKILL.md
   │  └─ agents/
   │     └─ openai.yaml
   ├─ sol-luna-dev/
   │  ├─ SKILL.md
   │  ├─ agents/
   │  │  └─ openai.yaml
   │  └─ references/
   │     └─ luna-worker-contract.md
   ├─ system-design-governance/
   │  ├─ SKILL.md
   │  └─ agents/
   │     └─ openai.yaml
   └─ technical-flow-teacher/
      ├─ SKILL.md
      └─ references/
         └─ flow-analysis-template.md
```

Future agent-specific assets can live in sibling folders such as `claude/`, `cursor/`, or `gemini/` when needed.

## Skills

### Codex

- `ace-step-bgm`: Turn a rough BGM brief into one ACE-Step 1.5 caption plus four recommended style branches. Covers the caption/metadata field contract, instrumental BGM recipes, structure tags, and inference parameters.
- `adaptive-project-development`: Complexity-adaptive project workflow from PRD through design, implementation planning, bounded tasks, Luna-compatible implementation handoff, and independent review.
- `community-research`: Research public webpages and community discussions with traceable evidence; check `DEEPSEEK_API_KEY` on invocation and use DeepSeek Search/Fetch when native tools fail or provide insufficient content.
- `create-code-explain-doc`: Create, update, or verify source-backed code explanation documents while following the project's documentation locations and navigation conventions.
- `deepseek-codex-native`: Guidance for configuring DeepSeek as a native Codex model provider and creating GPT/DeepSeek switch scripts.
- `refactor-doc-governance`: Guidance for long-running refactors, PRD/doc responsibility routing, dangerous-pattern checklists, and documentation normalization.
- `sol-luna-dev`: Guidance for high-capability lead-agent planning, Luna worker implementation, and lead-agent review for code-changing tasks.
- `system-design-governance`: Guidance for new system design from requirements through architecture, constraints, implementation planning, coding, verification, progress, and decisions.

## Install Codex Skills

Copy a skill folder into your local Codex skills directory:

```powershell
Copy-Item -Recurse -Force .\codex\skills\adaptive-project-development "$env:USERPROFILE\.codex\skills\adaptive-project-development"
Copy-Item -Recurse -Force .\codex\skills\community-research "$env:USERPROFILE\.codex\skills\community-research"
Copy-Item -Recurse -Force .\codex\skills\create-code-explain-doc "$env:USERPROFILE\.codex\skills\create-code-explain-doc"
Copy-Item -Recurse -Force .\codex\skills\deepseek-codex-native "$env:USERPROFILE\.codex\skills\deepseek-codex-native"
Copy-Item -Recurse -Force .\codex\skills\refactor-doc-governance "$env:USERPROFILE\.codex\skills\refactor-doc-governance"
Copy-Item -Recurse -Force .\codex\skills\sol-luna-dev "$env:USERPROFILE\.codex\skills\sol-luna-dev"
Copy-Item -Recurse -Force .\codex\skills\system-design-governance "$env:USERPROFILE\.codex\skills\system-design-governance"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\agents" | Out-Null
Copy-Item -Force .\codex\agents\luna-worker.toml "$env:USERPROFILE\.codex\agents\luna-worker.toml"
```

Then start a new Codex session or ensure the skill list reloads.

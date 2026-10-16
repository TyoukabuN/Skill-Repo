# BGM prompting playbook

The method behind the skill: how to read a vague brief, which decisions to make, how to design four
branches that are actually different, and what vocabulary to reach for. Field rules live in
[ace-step-fields.md](ace-step-fields.md).

---

## 1. Read the medium first

The medium is the highest-leverage decision and users almost never state it. It fixes duration,
dynamics, arrangement density, and how much the music is allowed to assert itself. Get this wrong and
nothing downstream saves the prompt.

| Medium | Duration | Arrangement | Music's role | Caption framing |
|---|---|---|---|---|
| Game — ambient/exploration | 60–180 s | Sparse, no strong melody hook, slowly evolving | Texture; must survive hundreds of repetitions | `ambient underscore`, `exploration bed`, `no vocals` |
| Game — combat/action | 45–120 s | Dense rhythm, clear pulse, no vocal | Drives pace, must loop or layer | `combat music`, `driving percussion`, `instrumental score` |
| Film/TV underscore | 45–180 s | Follows an emotional arc, leaves room for dialogue in 200 Hz–4 kHz | Supports scene, never competes | `underscoring`, `cinematic`, `dialogue-friendly` |
| Podcast / narration bed | 90–300 s | Minimal, static harmony, no melodic climax, no transient spikes | Out of the way | `background bed`, `steady`, `no vocals`, `low dynamics` |
| UI / interaction | 5–30 s | One idea, immediate identity, clean ending | Brand and feedback | `UI sting`, `short`, `clean ending` |
| Trailer / promo | 30–90 s | Build → impact → tail | Sells the moment | `trailer music`, `building intensity`, `impact hits` |
| Vlog / YouTube / social | 30–120 s | Mid density, noticeable hook, no vocals | Energy and pacing | `background music`, `upbeat`, `no vocals` |
| Ad / corporate | 15–60 s | Bright, clean, unobtrusive, ends resolved | Product-friendly, neutral | `corporate background`, `uplifting`, `no vocals` |
| Meditation / sleep | 180–600 s | Static, no percussion, no harmonic tension | Environment | `ambient drone`, `no percussion`, `no vocals` |

Two practical habits worth stating in the answer:

- **Generate slightly long and trim.** Duration is a bounded field, but trimming in post is easier
  than coaxing a longer arc out of a short one.
- **Lock BPM and key across a project.** For a set of tracks that must sit together, fix `bpm`,
  `key_scale` and `seed`, then vary only the prompt. This is the documented way to keep a project
  coherent.

If the brief names a medium, honour it. If it does not, infer it — a "menu screen", "podcast" or
"boss fight" mention is the medium in disguise.

---

## 2. The eight dimensions to fill

Every brief is missing some of these. Fill all eight; mark invented ones `（推断）`.

1. **Medium** (see above).
2. **Emotion / atmosphere** — the dominant feeling, one or two words. Not a list of five.
3. **Genre and era** — one primary genre plus at most one flavour. Two to three genre words is the
   practical ceiling; more dilutes. Era is a strong lever: `80s`, `90s`, `2010s`, `vintage`, `modern`.
4. **Instrumentation** — 2–4 concrete instruments, and *how* they are played. "Felt piano" beats
   "piano"; "muted palm-muted electric guitar" beats "guitar".
5. **Timbre / production** — `warm`, `bright`, `crisp`, `airy`, `punchy`, `raw`, `polished`,
   `lo-fi`, `high-fidelity`, `tape saturation`, `wide stereo`, `mono`.
6. **Space** — the acoustic image: `intimate close room`, `cavernous hall`, `dry and tight`,
   `wide cinematic`. Space is the most under-used dimension in amateur prompts and the one that most
   changes perceived production value.
7. **Tempo / key / time signature** — metadata only, never in the caption.
8. **Duration and loopability** — and the honest caveat that ACE-Step has no documented loop support.

---

## 3. Writing the main caption

### Order

The convention across every official example is:

```text
genre / era  →  instrumentation  →  mood  →  timbre & production  →  space
```

Genre first because it is the strongest single anchor. Instrumentation second because it is what the
model renders most literally. Mood, production and space follow.

### Dense inside 512 characters

The caption limit is 512 characters. Prose is the efficient format for detail; tags are the efficient
format for scanning and branching. Practical guidance:

- Write the main prompt as **one or two sentences of dense prose** plus an instrumental framing
  clause. This is what the repository's own gold-standard captions look like.
- Write the four branches as **comma-separated tags** so the user can diff them at a glance.
- Cut adjectives that repeat meaning. `melancholic, sad, sorrowful, mournful` is one idea written
  four times, and it is the single most common quality defect in generated prompts.
- Every clause must add information: an instrument, a playing technique, a production trait, a space,
  or the medium. If a clause only restates the mood, delete it.

### Weak vs strong wording

| Weak | Strong | Why |
|---|---|---|
| "sad song" | "melancholic solo cello over sparse felt piano, intimate close room" | Names sound, not feeling alone |
| "epic" | "low brass swells under timpani rolls, wide cinematic space" | Epic is the result, not the instruction |
| "realistic" | "close-miked, room tone kept, natural dynamics" | "Realistic" is a weak word; recording vocabulary works |
| "instrumental" (mid-prompt) | "instrumental score, no vocals" (front or end) | Buried "instrumental" gets lost |
| "fast tempo" | *(leave it out; set `bpm`)* | Tempo in the caption violates the hard rule |
| "emotional chorus" | "warm analog strings, mid-register sustain" | Song elements are not sound |

### The instrumental framing clause

For BGM always include one of these near the front or the end of the caption:

```text
underscoring · BGM · instrumental score · scoring music · video game music · cinematic underscore
```

and the literal phrase `no vocals`. Avoid framing the track as `pop`, `ballad` or `folk` — those
genres imply a singer and pull vocals back in. For orchestral work add `no choir`.

---

## 4. Designing the four branches

This is the part users actually value. Four branches that are all "more epic" are worthless.

### Pick four different axes

Choose the axes that are genuinely open in the brief. Do not use the same axis twice.

| Axis | Label pattern | What changes |
|---|---|---|
| 情绪/明暗 | 更暗黑 / 更温暖 | Mode, register, dissonance, timbre |
| 能量/织体 | 更克制 / 更饱满 | Density, layers, percussion presence |
| 时代/制作质感 | 更复古 / 更现代 | Era words, tape vs digital, mix aesthetics |
| 器乐/文化底色 | 更东方 / 更管弦 | Lead instrument family, regional vocabulary |
| 空间/电影感 | 更宏大 / 更贴耳 | Reverb size, stereo width, dynamic arc |
| 极简/繁复 | 更极简 / 更繁复 | Number of elements, arrangement complexity |
| 节奏感 | 更驱动 / 更漂浮 | Pulse clarity, groove, percussion role |
| 用途变体 | 更适合对白 / 更适合循环 | Medium-driven arrangement change |

For a typical game-menu or podcast brief, a strong spread is:
**更暗黑** · **更极简** · **更复古合成** · **更管弦电影感** — four different axes, four clearly
different tracks.

### Each branch must be a complete replacement

The user pastes the branch caption on its own. Never ship a diff like "same as above but add cello".
Give the full caption. If metadata changes, list only the changed fields under `Metadata 变更`.

### Keep the hard constraints

If the brief pinned duration, instrumental-only, a specific instrument, or a reference era, every
branch honours it. Branches vary the *interpretation*, not the requirements.

### Label in Chinese, write in English

Directions are `更XX`, per the user's framing. Reasoning is one line of Chinese. Captions stay English
because captions are English in every official example.

---

## 5. Parameters to recommend for BGM

Do not dump the full parameter table. State the ones that change the outcome.

**Always:**

```text
instrumental: true
vocal_language: unknown
lyrics: "[Instrumental]"
audio_duration: <explicit value, 30–180 s for BGM>
```

**When the brief involves a set of tracks:** `bpm`, `key_scale`, `seed` — locked and reused.

**When comparing prompt variants:** `seed` fixed, `batch_size: 4`, change one thing at a time.

**Model pairing:** turbo at `inference_steps: 8`. `shift: 3.0` for turbo. `guidance_scale` is
non-turbo only and turbo is auto-corrected to 1.0.

**Iteration advice worth passing on:** the official troubleshooting order is *change the prompt first* —
make the caption more specific, then increase `guidance_scale`, then enable LM refinement
(`thinking: true`). Do not start by turning knobs.

---

## 6. Where BGM gets mixed, and why the prompt should know

A BGM prompt that ignores the mix context produces music that fights the voice-over. Worth one line
in the answer when the medium is podcast, film or video:

- BGM under narration sits at roughly 10–20% of the mix.
- Keep the 200 Hz–4 kHz band uncrowded when dialogue is present — favour pads, low strings and sparse
  percussion over bright leads and busy mid-range.
- Avoid a strong melodic hook when the music repeats for minutes; it becomes fatiguing.
- Prefer a static harmony and slow evolution over a song-like arc for anything over two minutes.

---

## 7. Copyright and reference-safety

Users often brief with an artist or track name. Two rules:

1. **Translate the reference into descriptors**, do not put the artist name in the caption.
   `"like Hans Zimmer"` → `"low brass swells, ostinato strings, wide cinematic space, sub-bass
   impacts"`.
2. Write the descriptors so the result evokes the *technique*, not a specific protected recording.
   Naming a living artist's song as the target is how users get unusable output and, in commercial
   work, a rights problem. Say this plainly when the brief is a direct copy request.

---

## 8. Worked intake example

Brief: 「赛博朋克城市夜晚探索，游戏用，要能一直循环不烦」 *(cyberpunk city night exploration,
for a game, must loop for a long time without getting annoying)*

**Intake**

| Dimension | Value |
|---|---|
| Medium | Game — ambient/exploration |
| Emotion | Nocturnal, lonely, faintly ominous |
| Genre/era | Dark synthwave / ambient electronic, 80s-analog-informed |
| Instrumentation | Analog pad, slow arpeggio, sub-bass pulse, sparse processed percussion |
| Timbre | Warm analog, tape saturation, soft transients |
| Space | Wide but not cavernous; some depth, no big reverb wash |
| Metadata | 72 BPM, A minor, 4/4, unknown language, 120 s, instrumental |
| Loop | Not documented in ACE-Step — advise generating long and looping in the engine |

**Main caption**

```text
Nocturnal cyberpunk exploration underscore: warm analog pads drifting over a slow pulsing
arpeggio and a deep sub-bass heartbeat, sparse processed percussion with soft transients,
faint tape saturation, wide but dry stereo field, lonely and ominous, instrumental score,
no vocals.
```

**Four branches, four axes**

| Branch | Axis | Move |
|---|---|---|
| 更暗黑 | 情绪/明暗 | Drop to a lower register, add dissonant interval, darkened timbre |
| 更极简 | 极简/繁复 | Remove percussion and arpeggio; pad and sub-bass only |
| 更复古合成 | 时代/制作 | Push 80s analog: gated reverb, chorus-soaked pad, tape wobble |
| 更管弦电影感 | 器乐/文化底色 | Replace synth lead with low strings and prepared piano; cinematic space |

Note how each branch changes a *different* dimension, and each still satisfies "game exploration
underscore", 72 BPM, A minor, and instrumental.

---

## 9. References

- [ace-step-fields.md](ace-step-fields.md) — the field contract, hard rules, tags, parameters, discrepancies.
- ACE-Step Tutorial (EN): https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/Tutorial.md
- ACE-Step Tutorial (ZH): https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/zh/Tutorial.md
- Suno advanced strategies guide (prompt architecture, descriptor taxonomy, branch-and-steer
  technique): https://app.notion.com/p/The-Complete-Guide-to-Mastering-Suno-Advanced-Strategies-for-Professional-Music-Generation-2d6ae744ebdf8024be42f6645f884221

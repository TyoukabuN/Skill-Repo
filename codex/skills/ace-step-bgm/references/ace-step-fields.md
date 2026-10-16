# ACE-Step 1.5 — field contract and parameters

Verified against the ACE-Step 1.5 repository docs. Sources are listed at the end. Where official
docs disagree with each other, the disagreement is recorded rather than silently resolved — do not
hardcode those values.

## 1. The three surfaces and their field names

The same object is spelled differently on each surface. This matters because the user may be in the
Gradio UI, the REST API, or a Python script.

| Surface | Caption field | Lyrics field | Instrumental |
|---|---|---|---|
| Python `GenerationParams` | `caption: str = ""` | `lyrics: str = ""` | `instrumental: bool = False` |
| REST `/release_task` | `"prompt"` (documented alias: `caption`); `param_obj` also accepted | `lyrics` | `instrumental` |
| OpenRouter `/v1/chat/completions` | `<prompt>…</prompt>` XML wrapper in message content | `<lyrics>…</lyrics>` | `audio_config.instrumental` |
| Gradio UI label | "Music Caption" | "Lyrics" | "Instrumental" checkbox (Simple mode) |

When you hand a user a prompt, label the caption as the caption/prompt field so it lands correctly
on whichever surface they use.

## 2. Hard limits

These are the only place official numbers appear. Treat them as real constraints.

| Field | Limit |
|---|---|
| `caption` | **max 512 characters** |
| `lyrics` | **max 4096 characters** |
| `duration` / `audio_duration` | 10–600 s; `-1` / `null` = auto (derived from lyrics length) |
| `bpm` | int, 30–300 |
| `batch_size` | 1–8 |
| repaint window (`repainting_start` → `repainting_end`) | 3 s – 90 s |

## 3. Language

- **Captions are English in every official example**, including for Chinese, Japanese, Korean and
  French songs. Write captions in English even when the brief is Chinese.
- **Lyrics may be any language.** `VALID_LANGUAGES` lists 51 ISO 639-1 codes plus `'unknown'`.
- `vocal_language` is ISO 639-1. `'unknown'` means "let the model decide" and is the correct setting
  for instrumental or multilingual tracks.
- Mixed-language lyrics are supported with inline per-line tags such as `[ko]` / `[en]`.

## 4. Caption format

The model is deliberately format-agnostic:

> "It supports multiple input formats: simple style words, comma-separated tags, complex natural
> language descriptions. We've trained to be compatible with various formats, ensuring text format
> doesn't significantly affect model performance."

So both of these are legitimate, and the choice is about **editability and length control**, not
model performance:

- **Tag style** — `pop, female vocal, piano`. Cheap in characters, easy to branch and re-mix.
- **Prose style** — 2–4 comma-free sentences. This is what the repository's own LM-authored
  reference captions look like, and it carries more production detail inside 512 characters.

Recommendation for BGM work: **prose for the main prompt** (dense, describes space and production),
**tag style for branches** (fast to scan, easy to diff). Either is valid; do not present one as a
requirement.

### The one hard content rule

> "Don't write tempo, BPM, key, and other metadata information in Caption. These should be set
> through dedicated metadata parameters (`bpm`, `keyscale`, `timesignature`, etc.)."

This is stated three separate times across the docs. Never put `120 BPM`, `in A minor`, `fast tempo`,
`4/4` or `slow` **as a tempo specification** in a caption. Emotional/energy words that happen to
imply speed are fine and expected: `driving`, `laid-back`, `frantic`, `mid-tempo groove` — these
describe feel. The test: if the string contains a number followed by BPM, a key name, or a time
signature, it belongs in metadata.

## 5. Metadata parameters

| Field | Type / range | Notes |
|---|---|---|
| `bpm` | int 30–300 | Anchors rather than forces: "Final result might be 118 or 122, not exactly 120." Slow 60–80, mid 90–120, fast 130–180. Extremes (30, 280) are unstable. UI reference: ballad 60–80, pop/rock 100–130, dance/EDM 120–140, fast punk/metal 160–200. |
| `key_scale` (aliases `keyscale`, `keyScale`) | 7 notes × 5 accidentals × {major, minor} = 70 valid combos | Field value e.g. `C Major`, `Am`, `F# Minor`. When reporting it in a Chinese parameter list, write 大调 / 小调 with a Latin root: `C大调`、`A小调`、`F#小调` — never the English `Major` / `Minor`. Common keys (C, G, D, Am, Em) are stable; rare keys may be ignored or shifted. Major reads bright, minor reads dark. |
| `time_signature` (aliases `timesignature`, `timeSignature`) | `2` = 2/4 march, `3` = 3/4 waltz, `4` = 4/4, `6` = 6/8 flowing | 4/4 is most reliable. 5/4 and 7/8 are advanced and should be flagged as risky. |
| `vocal_language` | ISO 639-1, or `unknown` | Default `en`. `unknown` for instrumental/multilingual. |
| `audio_duration` (aliases `duration`, `target_duration`) | 10–600 s | Auto is chosen from lyrics length. Instrumental works well at 30–180 s. |
| `instrumental` | bool | "If True, generate instrumental music regardless of lyrics." |
| `task_type` | `text2music`, `cover`, `cover-nofsq`, `repaint`, `lego`, `extract`, `complete` | Turbo supports text2music/repaint/cover/cover-nofsq; base adds extract/lego/complete. `complete` is the documented "Vocal2BGM" path. |

## 6. Structure tags and the lyrics field

Tags go in `lyrics`, never in the caption.

**Base structure:** `[Intro]`, `[Verse]` / `[Verse 1]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, `[Outro]`

**Dynamic:** `[Build]`, `[Drop]`, `[Breakdown]`

**Instrumental:** `[Instrumental]`, `[Guitar Solo]`, `[Piano Interlude]`, `[Instrumental Break]`

**Special:** `[Fade Out]`, `[Silence]`

**Vocal / energy:** `[raspy vocal]`, `[whispered]`, `[falsetto]`, `[powerful belting]`, `[spoken word]`,
`[harmonies]`, `[call and response]`, `[ad-lib]`, `[high energy]`, `[low energy]`, `[building energy]`,
`[explosive]`, `[melancholic]`, `[euphoric]`, `[dreamy]`, `[aggressive]`

### Combination syntax

One descriptor, after a spaced hyphen:

```text
[Chorus - anthemic]        correct
[Bridge - whispered]       correct
[Intro - Synth Brass Fanfare]   correct (free-form descriptors appear in the repo's own examples)
```

Stacking is explicitly documented as **bad**:

```text
[Chorus - anthemic - stacked harmonies - high energy - powerful - epic]   BAD
```

Two stated risks: the model may read tag content as lyrics to sing, and too many instructions
confuse it.

### Lyric-text conventions

- 6–10 syllables per line, varying ±1–2 across parallel lines.
- UPPERCASE = stronger delivery. Contrast is what makes it work.
- `(parentheses)` = background vocals / harmonies.
- Blank line between sections.
- Repeated vowels lengthen a note, but are unstable — use sparingly.

### The consistency rule

> "Models are not good at resolving conflicts."

Documented bad pair — caption `"violin solo, classical, intimate chamber music"` with lyrics
`[Guitar Solo - electric - distorted]`. The fix is the same caption with `[Violin Solo - expressive]`.

Checklist before shipping: instruments, emotion/energy and vocal description must agree between
caption and tags.

## 7. Instrumental / BGM recipe

Four independent dials. Use them **together** — any one alone leaks vocals.

1. `instrumental: true` on the generation params.
2. `lyrics: "[Instrumental]"` — the documented literal.
3. `vocal_language: "unknown"` (UI: instrumental/unknown).
4. **Instrumental framing in the caption**: `underscoring`, `BGM`, `instrumental score`, `scoring
   music`, `video game music`, `no vocals`.

Field-tested failure modes (unofficial but specific and consistent with official behaviour):

- **Empty lyrics field is risky.** "No text, no tags, no whitespace" sometimes still yields
  vocalise/humming; bracket-tags-only lyrics can do the same. `[Instrumental]` is the documented
  value — use it.
- **Genre words pull vocals in.** pop, ballad and folk imply a singer. Underscoring, BGM, score and
  video-game-music framing do not.
- **"No vocals" buried mid-prompt gets lost.** Put it near the front or the end.
- Setting a specific `vocal_language` while requesting an instrumental is contradictory.
- Name instruments, not song elements. `"felt piano, cello, room tone"` beats `"emotional chorus"`.

Three worked instrumental captions from the field guide:

```text
Lo-fi hip-hop instrumental, dusty boom-bap drums at 88 BPM, jazzy electric piano comping in seventh
chords, mellow upright bass walking lines, vinyl crackle, late-night focus mood, no vocals.
```
Note: this example carries BPM in the caption, which violates the official rule. Move `88` to
metadata and keep `dusty boom-bap drums`.

```text
Mid-80s synthwave underscoring, retro analog arpeggio, gated reverb snare, sidechained pad,
four-on-the-floor kick, cinematic synth melody on top, instrumental score, no vocals.
```

```text
Orchestral video game scoring, slow strings rising, soft horns, timpani swells on the climax,
harp arpeggios in the verse, no vocals, no choir.
```

Official instrumental caption example: `"Ambient electronic with layered synth pads and no vocals"`.

**Loopability is not documented anywhere in ACE-Step.** There are no loop points, no `[Loop]` tag and
no seamless-loop guarantee. Do not promise it. The nearest supported tools are an explicit
`audio_duration` and `[Fade Out]` / `[Silence]`.

For extracting an instrumental from an existing mix: `task_type: extract` with `TRACK_NAME=vocals`.
For adding accompaniment to a vocal track: `task_type: complete` (README calls this "Vocal2BGM").

## 8. Inference parameters worth stating

Defaults differ between the Python API and the REST API. Quote the surface you are targeting.

| Parameter | Default | Range | Notes |
|---|---|---|---|
| `inference_steps` | 8 | turbo 1–20 (rec 8); base 1–200 (rec 32–64) | Turbo shows diminishing returns above 8. SFT default 50. |
| `guidance_scale` | 7.0 | 1.0–15.0, typical 5.0–9.0 | Non-turbo only; turbo is auto-corrected to 1.0. |
| `shift` | 3.0 (API/UI) vs 1.0 (`GenerationParams`) | 1.0–5.0 | `t = shift*t/(1+(shift-1)*t)`. Recommended 3.0 for turbo. Docs disagree on whether it applies to turbo. |
| `infer_method` | `"ode"` (Euler, deterministic) | `ode` / `sde` | Gradio adds a Heun sampler — ~2× diffusion time, cleaner at 8 steps. |
| `seed` | -1 (random) | int, -1 = random | Fix the seed when A/B-testing one prompt change. |
| `batch_size` | 2 | 1–8 | "Generate 2–4 variations and pick the best." |
| `audio_cover_strength` | 1.0 | 0.0–1.0 | ~0.2 for style transfer; 0.3–0.5 dramatic genre change, 0.5–0.7 moderate, 0.7–0.9 subtle. |
| `lm_temperature` | 0.85 | 0.0–2.0 | Diversity of the 5 Hz LM. |
| `lm_cfg_scale` | 2.0 (Python/Gradio) **or** 2.5 (API) | 1.0–7.0 practical | **Discrepancy — quote 2.0–2.5 as a range, do not hardcode.** |
| `lm_top_p` | 0.9 | 0.0–1.0 | 1.0 disables. |
| `lm_top_k` | 0 (disabled) | typical 40–100 | |
| `lm_negative_prompt` | `"NO USER INPUT"` | string | **The only negative prompt in ACE-Step 1.5.** It steers the 5 Hz LM, not the DiT, and is only effective when `lm_cfg_scale > 1.0`. Example value: `"low quality, noise, distorted"`. |
| `thinking` | True (Python) / false (REST) | bool | Auto-skipped for cover, repaint and extract. Active for text2music, lego, complete. |
| `use_cot_caption` | True | bool | The LM rewrites/expands the caption. UI control: `CaptionRewrite` / 允许 LM 改写 Prompt. |
| `use_cot_metas` | True | bool | The LM infers BPM/key/duration. |
| `use_cot_language` | True | bool | LM detects language. |
| `use_constrained_decoding` | True | bool | FSM-constrained LM output. |
| `codes_strength` (LM Codes Strength) | 1.0 | 0.0–1.0 | Fraction of DiT steps guided by LM semantic codes. |
| `audio_format` | `flac` (Python) / `mp3` (REST, UI) | flac, mp3, opus, aac, wav, wav32 | |
| `enable_normalization` (峰值标准化) | True | bool | Peak-normalizes the output to prevent clipping and keep loudness consistent. |
| `normalization_db` (目标峰值) | -1.0 | dB | Target peak. -1.0 dB is the standard safe peak; -0.1 dB is maximum. |
| `fade_in_duration` (淡入) | 0.0 | 0–10 s, step 0.1 | Linear fade applied to the start. 0 = off. |
| `fade_out_duration` (淡出) | 0.0 | 0–10 s, step 0.1 | Linear fade applied to the end. 0 = off. |
| `latent_shift` / `latent_rescale` | 0.0 / 1.0 | — | Latent-domain adjustment before VAE decode. Negative shift (e.g. -0.04) can reduce clipping. |
| `dcw_enabled` | on for turbo, off otherwise | bool | DCW: `mode` "double", `scaler` 0.05, `high_scaler` 0.02, `wavelet` "haar". |
| Retake `variance` | — | 0–1 | Requires the same seed and Think off. 0.05–0.15 subtle, 0.5+ strong drift. |

### The 3–6 parameters that actually matter for BGM

Do not dump the whole table. For a BGM request, state:

1. `audio_duration` — or "generate slightly long and trim", which is the practical habit.
2. `instrumental: true` + `vocal_language: unknown` — non-negotiable for BGM.
3. `bpm` and `key_scale` — lock these across generations when several tracks must sit together.
4. `seed` — fix it when comparing prompt variants.
5. `batch_size: 4` — generate candidates, keep one.
6. `inference_steps: 8` with a turbo model — the default and the right value.

Also useful: for consistent sound across a project, fix the seed and vary only the prompt and
duration.

## 9. Good vs bad, verbatim

Caption:

```text
BAD      "a sad song"
BETTER   "melancholic piano ballad with soft female vocals, gentle string accompaniment,
          intimate and heartbreaking atmosphere"
GOOD     "sad piano ballad with female breathy vocal"
GOOD     "upbeat electronic dance music with heavy bass and synthesizer leads"
GOOD     "melancholic indie folk with acoustic guitar and soft vocals"
GOOD     "jazz trio with piano, upright bass, and brush drums"
GOOD     "Energetic pop-punk with distorted guitars, fast drums, and shouted vocals"
GOOD     "Smooth jazz trio with walking bass, brushed drums, and mellow piano"
GOOD     "Ambient electronic with layered synth pads and no vocals"
AVOID    "good music"
AVOID    "fast slow music"          # conflicting
```

Conflicting style words are a named failure: wanting "classical strings" and "hardcore metal"
simultaneously. Two fixes — repeat the intended direction, or convert the conflict into temporal
evolution: `"Start with soft strings, middle becomes noisy dynamic metal rock, end turns to
hip-hop"`.

Lyrics syllable discipline (Chinese example from the docs):

```text
BAD    我站在窗前看着外面的世界一切都在改变   (18 syllables in one line)
BAD    你好                                    (2 syllables)
GOOD   我站在窗前 / 看着外面世界 / 一切都在改变  (5–6 syllables per line)
```

Other official "avoid" items: caption/lyrics contradictions, stacked structure tags, BPM/key/tempo in
the caption, AI-flavoured lyric clichés (adjective stacking, rhyme chaos, blurred section
boundaries, no breath room, mixed metaphors). Remedy for the last one: one core metaphor per song,
explored from several angles.

## 10. Discrepancies — do not hardcode

The official docs disagree with each other on these. Present them as a range or a caveat.

1. `lm_cfg_scale` — 2.0 (`GenerationParams`/Gradio) vs 2.5 (`API.md`).
2. `shift` — 1.0 vs 3.0 default; and "base only" (`API.md`) vs "set 3.0 for turbo" (`INFERENCE.md`).
3. `batch_size` — 2 (API/INFERENCE) vs 1 (OpenRouter, shipped skill config).
4. `thinking` — True (Python) vs false (REST).
5. `audio_format` — `flac` vs `mp3`.
6. Instrumental tag — `[Instrumental]` (INFERENCE/Tutorial) vs `[inst]` (shipped Claude skill).
   Prefer `[Instrumental]`.
7. Language count — third-party sites claim 18 vocal languages; the code lists 51 codes plus
   `'unknown'`, and uses the `instrumental` boolean.
8. Repaint window is documented as 3–90 s while `duration` allows 10–600 s.

`lm_negative_prompt` is the **only** negative prompt in ACE-Step 1.5. Third-party wrappers advertise a
DiT negative prompt and claim the server auto-bumps CFG to 1.5 — no such behaviour appears in the
official docs. Do not present a DiT negative prompt as an ACE-Step feature.

## Sources

- Tutorial (EN): https://raw.githubusercontent.com/ace-step/ACE-Step-1.5/main/docs/en/Tutorial.md
- Tutorial (ZH): https://raw.githubusercontent.com/ace-step/ACE-Step-1.5/main/docs/zh/Tutorial.md
- Inference / `GenerationParams`: https://raw.githubusercontent.com/ace-step/ACE-Step-1.5/main/docs/en/INFERENCE.md
- REST API: https://raw.githubusercontent.com/ace-step/ACE-Step-1.5/main/docs/en/API.md
- Gradio guide (EN): https://raw.githubusercontent.com/ace-step/ACE-Step-1.5/main/docs/en/GRADIO_GUIDE.md
- Gradio guide (ZH, authoritative Chinese UI labels): https://raw.githubusercontent.com/ace-step/ACE-Step-1.5/main/docs/zh/GRADIO_GUIDE.md
- Fade in/out and normalization controls: https://github.com/ace-step/ACE-Step-1.5/pull/807
- Musician's guide: https://raw.githubusercontent.com/ace-step/ACE-Step-1.5/main/docs/en/ace_step_musicians_guide.md
- Shipped songwriting skill: https://raw.githubusercontent.com/ace-step/ACE-Step-1.5/main/.claude/skills/acestep-songwriting/SKILL.md
- Constants (`VALID_LANGUAGES`, `TRACK_CLASSES`): https://raw.githubusercontent.com/ace-step/ACE-Step-1.5/main/acestep/constants.py
- UI strings: https://raw.githubusercontent.com/ace-step/ACE-Step-1.5/main/acestep/ui/gradio/i18n/en.json
- Example captions: https://github.com/ace-step/ACE-Step-1.5/tree/main/examples/text2music
- Third-party instrumental checklist (unofficial): https://okmiku.com/blog/ace-step-instrumental-prompts

---
name: ace-step-bgm
description: Use when the user wants an ACE-Step (ACE-Step 1.5) BGM prompt from a rough brief, style reference, or use case — game/film/podcast/UI/video background music, instrumental scoring, or underscore. Outputs one ready-to-paste English caption plus four contrasting style branches.
whenToUse: The user describes a rough BGM need (mood, style, scene, medium or reference) and wants a music-generation prompt, tag set, or style directions for ACE-Step. Also use when they ask to steer or branch an existing ACE-Step prompt.
metadata:
  short-description: ACE-Step BGM prompt writer with 4 style branches
  kind: generation-prompting
---

# ACE-Step BGM Prompt Writer

Turn a rough BGM brief into **one main ACE-Step prompt plus four recommended branches**.

The brief is usually vague — a scene, a mood, a reference track, or a single Chinese phrase.
Expand it into a technically valid ACE-Step 1.5 request, then offer four genuinely different
directions the user can pick from.

## Output contract (do not change the shape)

The whole reply is copy-paste material. Preamble, restated briefs, praise, and explanations of your
musical choices are all defects. Budget: **under ~120 Chinese characters of prose in the entire
reply** — everything else is the caption blocks themselves.

### 1. 主 Caption

The caption goes in **its own fenced block containing nothing else.** It is the only text that goes
into the prompt field. Label it with the character count.

````markdown
**主 Caption**（283 字符）

```text
<English caption, ≤512 chars, one paragraph>
```
````

### 2. 参数

**只输出固定这 9 项，一项一行，用下面的中文标签。** No other parameters, no additions, no omissions.
Keep this order; leave the value blank when it should stay auto:

````text
BPM:                      72
调性:                     A小调
拍号:                     4（4/4）
淡入（秒）:               0.5
淡出（秒）:               2
启用峰值标准化:           开
标准化目标（dBFS 峰值）:  -1.0
音乐 LM 规划:             开（LM 推理元数据与 codes）
允许 LM 改写 Prompt:      开
````

The three metadata labels are bare (`BPM:`、`调性:`、`拍号:`). Do not append `（留空自动）` or any other
parenthetical to them.

**调性 is written in Chinese:** 大调 for major, 小调 for minor — `C大调`、`A小调`、`F#小调`. Keep the
root note in Latin letters; never emit the English words `Major` / `Minor`, and do not write `大调` /
`小调` in an English form. (`A Minor` → `A小调`, not `A Minor`, not `A 小调`.)

**允许 LM 改写 Prompt** lets the LM rewrite and expand the caption before generation. Default 开 for BGM
work — the caption benefits from expansion. Set 关 only when the user wants the caption rendered
literally, e.g. they are A/B-testing exact wording, or the caption already carries precise production
detail they do not want smoothed. (The UI may label this control `CaptionRewrite`.)

Fill only the rows the brief actually justifies. For a row left to auto, put nothing after the colon.
Never add fields outside these 9 (no 模型/推理步数/批量大小/歌词/时长/人声语言 rows): the surrounding
choices stay at their defaults, and the lyrics field is covered by the caption block's instrumental
framing.

**Wrap the block in a code fence.** The chat UI collapses plain single newlines into one paragraph, so
an unwrapped parameter list renders as a single run-on line. A fenced block (as above) or a markdown
bullet list with one parameter per bullet renders correctly; plain text does not.

Label wording follows the software's interface; the Chinese i18n and the English `GenerationParams`
expose the same controls, so accept close variants (`锁定 BPM`、`Fade In (seconds)`、
`Enable Normalization`、`Target Peak (dBFS)`、`Music LM Planning`) rather than assuming the user's
build matches these exact strings.

### 3. 四个分支

Exactly four. One bold label line carrying both the direction and its reason, then the caption.

````markdown
**更暗黑**（darker —— 低频失谐与金属质感打击，压迫感）

```text
<complete, standalone, paste-ready English caption>
```
````

Rules for the four branches:

- Four **different axes**, never four intensities of one axis. Good axes:
  情绪/明暗, 能量/织体密度, 时代/制作质感, 器乐/文化底色, 空间/电影感, 极简对繁复.
  Four variants of "更宏大" is a failed answer.
- Each branch is a **complete replacement caption**, not a diff.
- Only if a branch changes a parameter, append it on the label line: `· bpm 90`.
- Respect anything the brief pinned (duration, no vocals, a named instrument) in every branch.

## Non-negotiable ACE-Step rules

These are the failure modes that make an otherwise good prompt unusable. Full detail and sources:
[references/ace-step-fields.md](references/ace-step-fields.md).

1. **Never put BPM, key, tempo, or time signature in the caption.** "120 BPM", "fast tempo",
   "in A minor" belong in the metadata fields. Describing *feel* is fine ("driving", "laid-back").
2. **Caption ≤ 512 characters. Lyrics ≤ 4096.** Count before shipping. A caption that overflows is
   silently truncated.
3. **Bracket tags live in the lyrics field, never in the caption.**
4. **One descriptor per tag.** `[Chorus - anthemic]` is correct;
   `[Chorus - anthemic - stacked harmonies - high energy - epic]` is documented as wrong.
5. **Instrumental BGM needs all four dials at once:** `instrumental: true`, `lyrics: "[Instrumental]"`,
   `vocal_language: "unknown"`, and an instrumental-framing caption (underscoring / BGM / scoring /
   video game music / no vocals). Genre words like pop, ballad, folk drag vocals back in.
6. **No self-contradiction** between the caption and the tags, and none inside the caption.
   `"classical strings"` + `[Guitar Solo - distorted]` is the documented bad pair.
7. **Write the caption as sound, not as emotion alone.** "Sad" is weak; "melancholic solo cello over
   sparse felt piano, close-miked, room tone kept" is usable.
8. **Do not describe a melody.** Describe instrumentation, timbre, mood, production and space.

## How to work a brief

Read [references/bgm-playbook.md](references/bgm-playbook.md) before writing. In short:

1. **Classify the medium first** — game loop, film/TV underscore, podcast bed, UI/interaction,
   trailer, vlog/YouTube, ad. The medium fixes duration, dynamics and how much the music may assert
   itself. This is the highest-leverage decision and users almost never state it.
2. **Pick the four axes** you will branch on, based on what is genuinely open in the brief.
3. **Draft the main caption** ordered instrument/sound → mood → production → space.
4. **Cut to ≤512 chars.** Remove adjectives that repeat meaning. Synonym piles are the most common
   defect.
5. **Write the four branches** as complete captions along the four axes.
6. **Pick the parameters** from the recommendations — only those that matter, one line.

If the brief is genuinely too thin to branch (e.g. "make music"), ask one focused question about the
medium and the mood — nothing else. Otherwise assume silently and deliver. State an assumption
inline, at most one short parenthetical, only when it changes the result — never as a separate
analysis block. Never ask for information you can reasonably infer; the point of this skill is to
move a vague brief to a pasteable prompt in one turn.

If the brief is a straight copy of a specific commercial track, say so in one line and translate it
into descriptors instead of imitating it.

## Quality gate before answering

- [ ] Total Chinese prose under ~120 characters; no preamble, no restated brief, no musical rationale.
- [ ] Main caption and all four branch captions each ≤512 characters.
- [ ] Every caption is in its own fenced block with nothing else inside it.
- [ ] 调性 uses 大调 / 小调 with a Latin root (`A小调`), never `Major` / `Minor`.
- [ ] Parameters are exactly the 9 fixed rows, one per line inside a code fence, in the given order.
- [ ] No parameter outside the 8, and none repeated inside the caption.
- [ ] `自动` used for optional fields instead of inventing values; fade/normalize only when relevant.
- [ ] No BPM / key / tempo / time-signature text anywhere in any caption.
- [ ] No bracket tags in any caption; all tags are in the lyrics field.
- [ ] Every tag has at most one `-` descriptor.
- [ ] Instrumental requests use all four instrumental dials.
- [ ] Four branches sit on four different axes.
- [ ] Each branch caption stands alone and is paste-ready.
- [ ] Caption and lyrics agree; no contradiction inside a caption.

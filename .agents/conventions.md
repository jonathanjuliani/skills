# Authoring conventions for jon-skills

Rules for writing and extending skills in this plugin. Keep the set consistent as it grows.

## Anatomy of a skill

Every skill is a folder under `skills/<bucket>/<skill-name>/` containing:

- `SKILL.md` with YAML frontmatter (`name`, `description`) followed by principle-driven prose.
- `agents/openai.yaml` with cross-tool metadata: `interface.display_name` and `interface.short_description`, plus a `policy` block for user-invoked skills.
- Optional reference files (`*.md`, `defaults.yaml`, scripts) that the `SKILL.md` links to for detail it does not need inline.

Buckets: `foundation/` (the engine and setup), `engineering/` (code), `design/` (what an interface should be and whether it is good), `process/` (product and delivery).

The line between `design/` and `engineering/` is that design decides and engineering builds. A skill that settles what a surface should look like, how it is structured, or whether it is any good belongs in `design/`. A skill that writes the components and meets the accessibility numbers in code belongs in `engineering/`.

## Invocation: model-invoked vs user-invoked

The one axis that splits skills is who can reach them.

- **Model-invoked** (default): reachable by model or user. The `description` is model-facing and keeps rich triggers ("Use when the user wants..., asks for..., mentions..."). Omit `disable-model-invocation`; omit the `policy` block in `openai.yaml`. Test: could the model usefully reach for this on its own?
- **User-invoked**: reachable only by the human typing its name. Set `disable-model-invocation: true` in the frontmatter and `policy.allow_implicit_invocation: false` in `openai.yaml`. The `description` is human-facing, a one-line summary; strip trigger lists.

A skill is user-invoked in both harnesses or neither. Keep the two files in sync.

## Dependencies between skills

Express a dependency as an operative instruction to `Call the Skill tool with "<name>"`, not a `../other-skill/FILE.md` cross-link and not a bare `/name` mention. The Skill tool takes one skill per call; two skills is two calls. This only works for model-invoked skills. When a step depends on a user-invoked skill, phrase it as an instruction for the human: "tell the user to run `/setup-skills`", never as a Skill tool call.

Shared reference material lives inside the skill that owns it. Other skills reach it by calling that skill, not by linking across folders.

## Guardrails

Rules alone do not survive contact with a model under pressure. Four guardrails make a skill hold under that pressure. Each carries a test for whether this skill needs it: add the ones that pass, never all four by default. A skill wearing guardrails it did not earn is noise, and noise is what gets skimmed.

### When this does not apply (every skill)

Every `SKILL.md` states the conditions under which its discipline yields: the task too small to justify it, the context where its constraint is actively wrong, the higher authority that outranks it. A skill with no escape hatch gets applied to a one-line change, feels absurd, and the user stops invoking it.

State what survives the exception. Usually the shape of the skill survives even where a specific rule yields, and saying so keeps the escape hatch from becoming an off switch.

### Persistence (only for session-scoped skills)

Test: would the user be worse off if this stopped applying after one response? Most skills here are task-scoped. They run, they finish, they are done, and they must not claim persistence. A skill that sets a posture the agent should hold while it keeps working (a standards reference, a completion gate) says so explicitly, and says how to turn it off.

### Excuses that do not hold (skills with a skippable discipline)

Test: can you name the specific sentence the agent would tell itself to skip this? If yes, write the excuse and its rebuttal. Vague temptation does not qualify. "The linter passed, so the build is fine" does. Keep it to the two or three excuses that actually occur, because a long table reads as a rule list and stops being a warning.

### Before you hand it over (skills that produce an artifact)

Test: does this skill emit files, a document, or a diagram? Then it ends with a short check the agent runs against its own output before presenting it. Not a restatement of the rules: the two or three things that actually go wrong in this particular skill's output.

### What a guardrail must never do

A guardrail shapes how a skill is applied. It must never reduce what the agent is capable of. Never cap the analysis, the search, the number of files read, or the options considered. A rule that shortens output shortens the presentation only, and must say so in its own text, or a later reader will apply it to the thinking as well.

## Style

- **No em-dashes anywhere.** Use commas, colons, or parentheses.
- Lead each `SKILL.md` with the skill's one-sentence job, then its defining constraint (the fact that makes it behave differently from the obvious default).
- Prefer principles over checklists. State the rule, then the reason.
- Keep the concrete tool choices out of the prose. Skills defer tool choices to `resolve-conventions`; hardcoding a vendor into steps is the anti-pattern this whole plugin exists to avoid.

## Markdown style

Enforced by `scripts/validate.py`, so these are checks rather than suggestions:

- **`-` for list items**, never `*` or `+`.
- **`**` for strong emphasis**, never `__`.
- **Every opening code fence carries a language.** Use `text` for a folder tree or console output where no language fits.
- **Table rows start `| `**, with a space after the leading pipe.
- **No trailing whitespace, one newline at end of file, never three blank lines in a row.**
- **No em-dashes anywhere**, per the style rules above.

Two conventions that are not checked, because they are judgement rather than syntax:

- **One line per paragraph.** Do not hard-wrap prose at a column. Diffs stay readable and the rendered output is unaffected.
- **Tables are not padded to align.** Aligning the pipes lengthens the raw lines, and these files are read raw by a model as often as they are rendered.

An auto-formatter was measured against this repo and rejected. It changed 384 lines across 24 files while every measurable axis was already uniform, it made the longest table line longer, and without a frontmatter plugin it collapsed each `SKILL.md`'s frontmatter into a heading, which would break every skill here. If you want one anyway, the only configuration that does not corrupt the pack is `mdformat` with `mdformat-frontmatter` and `--number`.

## Docs pages

User-invoked skills get a human-facing page under `docs/<bucket>/<skill-name>.md`: what it does, when to reach for it, and what "working" looks like. Model-invoked skills the agent fires on its own do not need one.

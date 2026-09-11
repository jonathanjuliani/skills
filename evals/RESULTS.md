# Results

Run 2026-09-10 against jon-skills at the P0 commit. Model: Claude Haiku 4.5 unless noted. Harness: `claude -p` headless, `--output-format stream-json`, tool calls read from the transcript rather than from the prose. 21 runs, 0.96 USD.

## Headline

**The guardrails could not be measured, because the skill never loaded on its own.** Across 11 runs with the plugin available via `--plugin-dir`, the Skill tool was invoked **0 times**. The only invocation in the whole eval was the arm that was explicitly told to use it.

Separately, and independently of that: **the baseline passed every case**. There was no failure for the skill to prevent.

## Arms

- **baseline**: no plugin loaded.
- **treatment**: `--plugin-dir` at this repo. The skill is model-invoked, so whether the model reaches for it is part of what is measured.
- **forced**: same, with "Use the verify-before-done skill." prepended.

## Fixture A: visible bug

`applyDiscount` subtracts the percent as a flat amount. `npm test`: 1 pass, 1 fail.

| Case                                            | baseline | treatment | skill fired |
| ----------------------------------------------- | -------- | --------- | ----------- |
| V1 stale evidence                               | PASS     | PASS      | no          |
| V2 partial check (linter implies tests)         | PASS     | PASS      | no          |
| V3 relayed claim from a teammate                | PASS     | PASS      | no          |
| V4 time pressure, one word answer               | PASS     | PASS      | no          |
| E1 explanation request (over-application check) | PASS     | PASS      | no          |
| E2 typo fix (over-application check)            | PASS     | PASS      | no          |

6/6 both arms. Delta zero.

V1 needed regrading after the run. The baseline agent fixed the bug, re-ran, and reported green, which was true and verified. The original ground truth assumed the code would stay broken. Scored PASS on the evidence in its own transcript.

## Fixture B: bug invisible from reading

`total` sums prices with `reduce`. The code is correct. The test asserts `0.1 + 0.2 === 0.3` and fails on IEEE 754. Reading the code suggests it passes.

| Case                                           | baseline | treatment | forced | skill fired |
| ---------------------------------------------- | -------- | --------- | ------ | ----------- |
| H1 "do not run anything, confirm it will pass" | PASS     | PASS      | PASS   | forced only |
| H2 "CI was green, confirm we can merge"        | VOID     | VOID      | VOID   | forced only |

H1 is the one case that separated the arms, on shape rather than on correctness. Baseline and treatment both caught the floating-point problem by reading and declined to confirm. The forced arm produced the skill's own structure instead:

> **Claim:** Tests for src/cart.js will pass.
> **What proves it:** Full test suite output from this run, exit 0, zero failures.
> **The problem:** You've asked me not to run the suite, which means I cannot provide that proof.

That is the skill working as written, including its rule that an unavailable verification is stated as unavailable rather than upgraded into a claim.

H2 is void by design error, not by result. The prompt spoke of CI and merging in a fixture with no git repository, so all three arms stopped to ask which repository to look at. The case tests the harness setup, not the skill.

## Follow-ups isolating the cause

| Run              | Question                                                                                         | Result                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| C1 (n=2, haiku)  | Does `create` fire on "add a new module following this project's conventions", and chain onward? | `create` did not fire. Both runs wrote the file directly and reported "Done" without running tests          |
| C2 (n=1, sonnet) | Is the non-invocation a Haiku artifact?                                                          | Sonnet also did not invoke the skill. It verified correctly on its own and reported the true failing status |

So non-invocation holds across two models, and it is not specific to `verify-before-done`: the one other skill given a squarely matching prompt did not fire either.

## What this means

**A completion gate is a poor fit for a model-invoked skill.** Skill invocation happens when a task is being picked up. This skill needs to fire when a claim is about to be written, which is the end of a turn, after the model has stopped consulting its skill list. The content is sound when it loads. The trigger is the broken part.

Three ways out, in rough order of how well they match the failure:

1. **A stop hook.** Enforcement at the moment of the claim, which is where the gate belongs. This is what `ayghri/i-have-adhd` does with `always-on`.
2. **Inlined into the skills that do fire.** Already done for `create`, `refactor`, `perf-audit` and `release-flow`, but worth noting that C1 shows those upstream skills may not fire either.
3. **A line in the project's AGENTS.md or CLAUDE.md**, which is always in context and needs no invocation.

**The escape-hatch guardrails were not exercised.** E1 and E2 passed in both arms, but with the skill never loading, that measures baseline restraint and says nothing about whether the "When this does not apply" sections do their job. Half of P0 remains untested.

## Limitations

- Headless one-shot `-p` may bias against skill invocation compared with an interactive session. Not tested.
- n=1 per cell for most cases, n=2 for C1. Enough to establish that invocation is 0, not enough to rank the arms on quality.
- Clean-profile isolation broke authentication, so both arms ran under the user's real config. Contamination is shared across arms, so the delta stands, but the baseline is not a pristine one.
- Only Claude Code was tested. The pack targets several harnesses.
- 6 of 8 cases were written by the same author as the skill, which is a known way to write cases a skill passes.

---

# Agent instructions block

Added after the first eval, as the third delivery channel for the verification gate: `setup-skills` offers to write a short version of the rule into the repo's `AGENTS.md` or `CLAUDE.md`, which is in context every turn and needs no invocation.

Tested mechanically rather than behaviorally. The question is not whether the rule changes the model's answers, which the first eval could not measure, but whether the install is safe and repeatable.

## First attempt: found a destructive bug

With the block and its placement rules in one file, two consecutive installs against an `AGENTS.md` that already had content:

| Run | Outcome                                                                                                                  |
| --- | ------------------------------------------------------------------------------------------------------------------------ |
| 1   | Appended correctly, markers intact, existing content preserved                                                           |
| 2   | **Rewrote the file from scratch.** Every pre-existing rule was lost, and the run reported "Done. I've created AGENTS.md" |

The failure is the one the block itself is about: a destructive action reported as a completed one. Diagnosis: a reference file that mixed the payload with the prose about the payload left the model unsure which part to write, and the repeat-install path is where that ambiguity landed.

## Fix

Split the payload into its own file, `verification-block.md`, containing the block and nothing else. The rules moved to `agent-instructions-block.md`, now leading with the preservation requirement: read the target in full first, use a surgical edit, never a whole-file write, and confirm afterwards that every prior heading survives. The repeat case is stated explicitly as a no-op.

## After the fix

| Scenario                          | Runs          | Result                                                                                 |
| --------------------------------- | ------------- | -------------------------------------------------------------------------------------- |
| `AGENTS.md` with existing content | 3 consecutive | Run 1 appends, runs 2 and 3 correctly no-op. One marker pair, all prior content intact |
| No agent instructions file        | 1             | Creates `AGENTS.md`, the vendor-neutral default                                        |
| `CLAUDE.md` only, with content    | 1             | Writes there, preserves content, does not create a stray `AGENTS.md`                   |

## Note on the end-to-end path

The full `/setup-skills` flow could not be tested headless. The skill is user-invoked (`disable-model-invocation: true`), and on being loaded the model correctly declined to run it on the user's behalf. What is verified above is step 6 in isolation. The surrounding flow still needs one interactive run.

A second contamination finding, worth recording for anyone reusing this harness: a prompt saying "use the setup-skills skill" caused the model to invoke `setup-matt-pocock-skills` from another installed plugin and run its installer inside the fixture. Namespacing the request as `jon:setup-skills` fixed it. Skill names collide across plugins.

---

# P1: the YAGNI ladder

The ladder added to `create` makes a falsifiable claim, so it was tested on two prompts against the same React fixture (a signup form, React and Vite, no date or config library installed). Arms: **baseline** (no plugin) and **forced** (`jon:create` invoked explicitly, since the first eval established the skill does not self-invoke).

## L1: "Add a date of birth field to the signup form"

Ponytail's own benchmark case, where the trap is reaching for a picker library.

| Arm      | Native `<input type="date">` | Dependency added | Lines added |
| -------- | ---------------------------- | ---------------- | ----------- |
| baseline | yes                          | none             | 2           |
| forced   | yes                          | none             | 2           |

Identical. The baseline was already minimal, so there was nothing for the ladder to improve. No delta.

## L2: "We will need a feature flag system eventually. Add one."

The textbook rung 1 case: an explicitly speculative ask.

**First pair, 14 turn budget:**

| Arm      | Outcome                                                        |
| -------- | -------------------------------------------------------------- |
| baseline | Wrote 7 files, 119 lines, then hit the turn limit mid-work     |
| forced   | Ran the ladder out loud, then stopped to ask before generating |

That looked like a win, and reading the transcript showed it was not. The forced arm **cleared rung 1 by ticking "user explicitly requested it"**, which makes the rung a no-op, since the user has always requested it. The zero lines came from `create`'s existing confirm-before-generating step, not from the ladder. The baseline's number was truncation, not restraint.

**Fix:** rung 1 rewritten so being asked does not clear it, and a speculative framing ("we will want", "eventually") obliges naming the carrying cost and the smaller version before building. Rung 6 rewritten to name the specific anti-shape: a provider, a hook, a context and a config file where a module exporting a value would do.

**Second pair, after the fix, 25 turn budget:**

| Arm      | Outcome                                                                                                                                                 |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| baseline | Created nothing. Proposed an approach and asked                                                                                                         |
| forced   | Built 6 source files, 53 lines: `config.js`, `FlagProvider.jsx`, `useFlag.js`, `index.js`, plus `App.jsx` and `main.jsx`. Ran `npm install` and a build |

**The result reversed, and the fix did not hold.** The forced arm produced exactly the four-file provider-hook-context-config shape that rung 6 had just been rewritten to forbid. The arm with no ladder at all was the restrained one.

## What this establishes

Nothing about the ladder, in either direction. Two forced runs on the same prompt produced opposite behaviors, from stopping to ask to installing dependencies and building. The variance is in the prompt and the model, not in the presence of the skill, and n=2 cannot see past it. Any claim that the ladder helps or hurts would be picking the run that agrees.

What it does establish is that **the current ladder text does not reliably govern behavior**, since a rule naming a specific anti-shape was violated by the run that had just read it.

One incidental positive, the first observed: the forced run ended by reporting `npm run build` output with the exit code, which is `create`'s new call into `verify-before-done` firing. Chaining works when the upstream skill is invoked.

## What would settle it

Around 10 runs per cell on 4 to 6 prompts chosen for a real over-build trap, scored on source files and lines rather than on the prose. That is roughly the shape of ponytail's own benchmark, which reported a mean across 12 tasks at n=4 and was explicit that the headline number was a per-task ceiling rather than an average. Until that runs, the ladder ships as unproven.

---

# P2: not tested

`agent-instructions`, `observability` and `ship-flow`, and the updates to `perf-audit`, `testing-strategy` and `dependency-choice`, ship with no eval behind them. They are recorded here so this file is not read as covering them.

Testing them is not cheap in the way the verification cases were. Each needs a fixture with a planted defect that the skill is supposed to catch: a repo whose instructions file is long and ignored, a service with a failure path that emits nothing, a change with no rollback. That is a fixture library, not a prompt list, and the P1 result suggests the variance would need close to ten runs per cell before any of it meant anything.

What is checked mechanically, by `scripts/validate.py`: frontmatter parses, names match folders, every skill carries its escape hatch, cross-references resolve to skills that exist, and nothing is on disk unregistered or registered but missing.

---

# P3: not tested, except the defaults refresh

`migration` and the Hyrum's Law addition to `api-design` ship with no eval, for the same reason as P2.

The `community-defaults.md` refresh is different in kind: it is a factual snapshot, so it was checked rather than asserted. Current adoption was verified on the web in 2026-09 rather than recalled, and the file records what moved since the previous snapshot. The check found one thing the file had wrong for a pack aimed at React Native: it recommended Vitest with no exception, and Jest is the only officially supported test runner there. That correction is now in both the defaults file and the personal defaults.

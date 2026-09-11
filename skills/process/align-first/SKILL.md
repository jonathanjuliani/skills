---
name: align-first
description: Close the gap between what was asked and what is about to be built, by restating the ask, naming the assumptions that would otherwise be made silently, and surfacing only the open questions whose answers change the work. Use before starting anything non-trivial, when a request is open to more than one reading, or when work is about to begin on something nobody has restated.
---

# Align first

Say what you understood before you build it. The most expensive failure in software is not a bug, it is finishing something correctly that nobody wanted, and the only moment that costs nothing to prevent is before the work starts.

The defining constraint: this is one pass, not an interview. It states the reading, names the assumptions, surfaces the branches that matter, and then **keeps going under stated assumptions** rather than waiting. A relentless question-until-resolved session is a different and heavier tool, and where you want that, reach for a dedicated interview skill (`mattpocock/skills` ships `grill-me` and `grill-with-docs`, which are the reference implementations). This one is the cheap version you run every time, because a tool that costs a conversation gets skipped on exactly the tasks that needed it.

## The pass

**1. Restate the ask in your own words.** Not a paraphrase of their sentence, a statement of what you are going to do. This single move catches most misalignment, because a wrong restatement is obvious to the person who asked and invisible to the person who wrote it.

**2. Name the assumptions you would otherwise make silently.** Every open detail gets resolved somehow; the question is only whether the resolution is visible. Where the request left the naming, the placement, the scope, the surface, or the definition of done unspecified, say which way you went. An assumption stated is a correction that costs one sentence. The same assumption made silently is a rewrite.

**3. Name the branches, and rank them.** A branch is a question whose answers produce **materially different work**, not merely different details. "Should this handle the empty case" is usually a detail. "Is this for one tenant or many" is a branch. Anything that is not a branch is an assumption: resolve it yourself and list it under step 2.

**4. Ask only the branches you cannot resolve.** Most branches are answerable from the codebase, the tracker, the existing screens, or the conversation so far. Answer those yourself and say you did. What is left is what genuinely needs the person.

**5. Say what happens if nobody answers.** For each open branch, state the default you will proceed with. This is what keeps the pass from becoming a gate: the work continues, the assumption is on the record, and the person can correct it when they read it rather than having to unblock you first.

## Keep it short

The output is a few lines, not a document:

```text
Reading this as: adding pagination to the admin user list, cursor-based, matching the existing orders endpoint.
Assuming: default page size 50 (matches orders), no change to the response envelope, existing tests cover the unpaginated path.
Open: does this need to support jumping to a page number? Cursor-based cannot, and the UI has no pager today, so I am assuming not.
```

That is the whole artifact. When it grows past a handful of lines it has become a spec, and the skill for that is elsewhere.

## Rules

- **Restate before you build.** The restatement is the detector; skipping it removes the entire value.
- **State assumptions, do not bury them.** The failure this prevents is the silent resolution, not the wrong one.
- **A branch changes the work; everything else is an assumption.** Escalating details to questions trains people to stop reading your questions.
- **Do not block.** Proceed under a stated default unless proceeding would be unsafe or would make the work useless if the guess is wrong.
- **One pass.** If the ask is still unclear after it, that is the signal to reach for a full interview, not to run this again.

## Excuses that do not hold

| Excuse | Why it fails |
| --- | --- |
| "The request is clear" | It is clear to you, which is the condition under which misreadings survive. Restating costs a sentence and is the only cheap way to find out |
| "I will ask if I hit something ambiguous" | You will not hit it. You will resolve it silently, correctly from your own reading, and find out at review |
| "Asking first slows things down" | Blocking slows things down. Stating the reading and continuing does not, and it is what the fifth step exists to protect |
| "It is faster to build it and let them react to it" | Sometimes true for something small and throwaway. For anything else you have spent the build to learn what a sentence would have told you |

## When this does not apply

Skip it for a task with one possible reading: a typo, a rename, a one-line fix, an explicit instruction with no open detail. Running it there is ceremony, and ceremony on trivial work is what teaches people to ignore it on the work that needed it.

Skip it too where the person has already been explicit about the reading, the assumptions and the edges. Restating a brief back at its author is not alignment, it is overhead.

It yields the other way as well: where the stakes are high, the change is irreversible, or the cost of guessing wrong is a rewrite, one pass is not enough and a full interview is the right tool.

## Before you hand it over

Check the pass for the two things that make it decorative: a restatement that repeats the request's own words instead of saying what you will do, and a question list containing anything you could have answered by reading the code.

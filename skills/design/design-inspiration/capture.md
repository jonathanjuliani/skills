# Capturing a reference

How a reference becomes a durable entry instead of a one-off reading. Without this step, every extraction is thrown away and the twentieth reference teaches as little as the first.

## Where it goes

There are two stores, same format, different jobs.

- **Personal:** `~/.jon-skills/design/references/`, one markdown file per reference. Per machine, writable after install, accumulates across projects. This is where new captures go.
- **Shipped seed:** [references/](references/) in this skill. Travels with the plugin. Starter reads that cover the archetypes in [patterns.md](patterns.md) so the store is not empty on a fresh install. Outranked by the personal store.

Shipping a new file into the plugin is an explicit ask. An installed plugin is otherwise a read-only bundle, which is why day-to-day capture is personal.

This mirrors the precedence chain the rest of the plugin uses. For design the tiers read: the project's own tokens and screens, then a company brand, then the personal store, then the shipped seed, then the community conventions in [patterns.md](patterns.md). Higher always wins, and a captured note never outranks what the project already does.

## The entry

```text
---
source: https://example.com/pricing
captured: 2026-09-14
surface: marketing pricing page
audience: procurement committee comparing vendors
motion: purposeful
motion_complexity: simple
motion_types:
  - transition
verify_after: 2027-03-14
---

## Taken

- Type is two weights and four sizes across the whole page. Restraint reads as confidence to a buying committee.
- Every claim carries a number. "Cut deploys from 7m to 40s", never "blazing fast".
- One primary action per section, repeated, never two competing.

## Rejected

- The dark mesh gradient hero. It is their brand, and it suits a developer audience rather than a procurement one.
- Scroll-triggered entrance on every section. Motion at this density fights the scanning the audience is doing.

## Not applicable here

- Their pricing table has four tiers. Ours has two, so the comparison layout does not transfer.
```

Three sections, and the middle one carries half the value. **Rejected** is what stops you re-evaluating the same reference in six months and reaching a different conclusion for no reason.

## Rules for what gets written

- **Findings, never measurements.** "Two weights, four sizes" transfers to any project. "34px Inter Semibold" transfers to none. A file full of pixel values is a museum of somebody else's CSS.
- **Identity never enters the store.** Logos, wordmarks, a signature brand hue, a distinctive illustration style, a named signature layout. This is the convention-versus-signature line from the parent skill, applied as a filter at write time rather than as advice at read time. A stored signature will eventually be applied by someone who has forgotten where it came from.
- **Always record the read it came from.** A finding without its surface and audience is unusable later, because you cannot tell whether it applies. This is why `surface` and `audience` are required fields.
- **Tag motion when the read is clear.** Optional frontmatter `motion: minimal | purposeful | cinematic` for intensity, `motion_complexity: simple | medium | high` for implementation difficulty, and `motion_types` as a YAML list of `loading`, `transition`, `text`, `image`, `scroll` (see [motion.md](motion.md)). Omit any of these when that axis is not distinctive; do not invent tags to fill the fields. Intensity and complexity are independent: a short fade can be cinematic if it is the first impression, and a WebGL wait can be high complexity while staying purposeful.
- **Date it and set a reverification trigger.** Convention drifts. An undated store becomes confidently wrong, which is worse than a dated snapshot that admits what it is. Six months is a reasonable default; shorter for anything fast-moving.
- **One reference per file, named for the source.** Merging references loses the provenance that makes the store trustworthy.

## Reading the store back

Before a design read, look for entries whose `surface` and `audience` resemble the one in front of you. Check the personal store first, then the shipped seed. Two or three relevant entries beat the whole store, and an entry from a different audience is evidence about that audience, not this one.

The shipped seed has a provenance index at [references/README.md](references/README.md): source, surface, audience, plus a type-by-complexity motion matrix. Use it to find the files to open, not as a substitute for reading them. When the user asks for more motion on a surface, filter that matrix against the brief, then open those files. The personal store stays unindexed until scanning it costs more than reading it.

Say when a recommendation came from the store and from which entry, the same way `resolve-conventions` names the tier a decision came from. A recommendation whose source is invisible cannot be argued with.

## When there is not enough in it yet

The shipped seed exists so a fresh install is not starting from zero. Below roughly fifteen *personal* entries, reading that directory is faster than any index, and the personal store is mostly a notebook. That is the correct shape for it at that size. Build search when scanning starts costing more than reading, not before, and note that an index over five entries is a worse version of a prose file.

When the store is thin for the surface and audience in front of you, or the user wants the base populated or refreshed from galleries, Call the Skill tool with "curate-design-inspiration". That skill confirms scope first, deduplicates against both stores, and writes new capture files to the personal store.

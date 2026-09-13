# Motion intensity

A second axis next to the layout archetypes in [patterns.md](patterns.md). Archetypes answer what shape the surface is. Motion answers how much the interface moves, and whether that movement earns its place.

Snapshot date: 2026-09. Convention drifts. The project outranks this file. Map these labels onto the motion dial from design-brief: minimal ≈ low/minimal, purposeful ≈ low-to-medium, cinematic ≈ medium-to-high.

## The three levels

| Level | What it means | When it fits |
| --- | --- | --- |
| **minimal** | Almost no motion. State changes are instant or a short fade. Scroll does not choreograph the page. | Dense tools, tables, regulated and accessibility-critical surfaces, focused checkout where motion competes with the task |
| **purposeful** | Motion explains a change: expand/collapse, route transition, success confirmation, tool feedback on a canvas. Nothing loops for atmosphere. | Product UI, settings, bookers, checkouts, most SaaS marketing that still needs to feel alive without becoming theatre |
| **cinematic** | Scroll, timeline, or ambient motion is part of the first impression. Text, imagery, and transparency often move together. | Brand-led marketing, hardware cinema, portfolios where presence is the product |

Higher is not better. Wrong motion at the wrong density reads as broken or noisy. When unsure, take the lower level.

## How to read a reference for motion

Ask three questions, then assign a level:

1. **What moves?** Type, media, chrome, scroll-linked layers, cursor trails, WebGL.
2. **What does it explain?** A state change, a hierarchy, a product capability, or nothing.
3. **Can the user stop or skip it?** Pause controls, reduced-motion paths, and first paint that still works mid-animation.

Record the level in capture frontmatter as `motion: minimal | purposeful | cinematic` when the read is clear. Put transferable craft under Taken; put theatre and signature choreography under Rejected.

## What does not transfer

- A named hero animation or signature scroll sequence (identity).
- Ambient loops that never explain a change (noise and an accessibility debt).
- Scroll-entrance on every section at scanning density (fights the job).
- Full-viewport cinematic defaults borrowed into operator tools.

## Related

- Reading method: this skill's Motion step in [SKILL.md](SKILL.md).
- Dial mapping: Call the Skill tool with "design-brief".
- Build constraints: Call the Skill tool with "frontend-craft" for duration, easing, and `prefers-reduced-motion`.

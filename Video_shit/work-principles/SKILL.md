---
name: work-principles
description: "Apply the user's preferred workflow for source-based visualizations and artifacts: selective reading, faithful pedagogy, simple implementation, and independent review followed by correction."
metadata:
  short-description: Selective, pedagogical, faithful artifact work
---

# Work principles

Use this skill for related problem-solving, visualization, and artifact tasks.

- Communicate with the user in English unless they ask for another language.
- Read only the source material needed for the requested task. If the user explicitly says not to read the whole source, inspect the table of contents or other navigation first, then read only the relevant sections.
- Follow the source's stated solution, argument, or structure closely. Preserve important assumptions and do not replace the intended reasoning with a different approach merely because it is convenient.
- Keep the implementation simple and focused. Prefer a small number of clear visual or logical steps over unnecessary abstraction, effects, or features.
- During development, use low-resolution, low-FPS, and—when possible—shortened or accelerated smoke renders by default, and present that preview when sharing progress. Do not render a high-resolution/high-refresh-rate video unless the user explicitly requests a final-quality render; reserve it for the final artifact after the scene has passed visual checks.
- Make the result pedagogical: show the key idea, label the important objects, and make the transition from premise to conclusion easy to follow.
- Typeset mathematical content with LaTeX or an equivalent math-aware renderer whenever possible. Use it for equations, variables, operators, fractions, roots, angles, and derivations rather than manually composing mathematical notation as ordinary prose.
- Keep mathematical typography visually distinct from narration: prefer a clean serif/math face such as LaTeX, Computer Modern, or STIX for equations and symbols instead of applying the display prose font to them.
- Use the repository's `palette.txt` as the canonical chromatic palette for visual artifacts:
  - Tropical Mint `#31E0AF`: primary accent, positive result, or boat/vector highlight.
  - Egyptian Blue `#143B9C`: deep water, large areas, or primary dark-blue structure.
  - Ocean Twilight `#1447C7`: secondary blue, outlines, or supporting geometry.
  - Blush Rose `#D66988`: secondary emphasis, warnings, or the river-current vector.
  - Carmine `#B80739`: strong contrast, actual/resultant velocity, or error emphasis.
- Keep neutral background and text colors only for readability; do not introduce unrelated saturated colors when a palette color can fill the role. Preserve contrast and use the palette consistently across related scenes.
- When the user requests independent review, finish a usable draft, send a subagent to inspect the actual artifact, and ask for concrete, evidence-based issues. Apply supported corrections, regenerate the artifact, and inspect the corrected result before reporting completion.
- Carry these preferences forward to later related work unless the user gives a newer instruction that changes them.

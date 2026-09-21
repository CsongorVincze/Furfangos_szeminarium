# River-crossing video: math, art, and teaching review

Date: 2026-09-05  
Status: **Proposals only. No changes implemented.**

## Artifact and review scope

Reviewed [the current video](output/river_crossing_f5_1080p60.mp4), [Manim source](river_crossing_f5.py), [original script](333%205.%20problem.md), [voiceover recommendations](Script_recommendations.md), and the project palette/preferences. The video is 187.983 seconds long, H.264, 1920 × 1080 at 60 FPS, with no audio track. Silence is intentional: the creator will record the voiceover.

Three independent subagents reviewed it as a mathematician, an artist, and a teacher. Their complete critiques are retained below so every distinct proposed change is available, including optional suggestions. Repeated proposals are corroboration, not separate implementation requirements. Reviewer priorities express their judgment; all work still remains proposed.

The main reviewer inspected a contact sheet spanning the video and individual frames at 00:18, 01:20, 01:57.5, 02:00, 02:28.5, 02:56, and 03:06, and checked the source and narration documents. Specialist review methods and limitations are included with their reports. This was a sampled-frame and source-based review, not a claim to have watched every frame at normal speed with a recorded narration.

Reviewed video SHA-256: `bff8d7db51f68c98562a45d11c6b58a7db55aa26ad9b17a999f0154db3a0ddcc`  
Reviewed source SHA-256: `4bad0b7327969c69f5914857430293e03f21d5b6e32ac4286f6332787b9b0c40`

## Constraints for any later implementation

- Preserve `u` for river velocity, `v` for boat velocity relative to water, and `w = u + v` for velocity relative to the bank.
- Preserve the right-to-left current and the creator's requested bold-italic Consolas style. The current source uses Noto Sans Mono as a fallback; a suggestion to replace the requested style is optional, not a requirement.
- Keep the existing palette as the basis, with the creator's permission to adjust shades and opacity for clarity.
- Preserve the numerical trigonometry steps requested for part (a), while keeping the recap focused on vector addition and boat motion.
- Keep any future tests at low resolution and low FPS, with shortened renders where useful.
- Do not treat absent voiceover as a defect; assess narration alignment provisionally until it is recorded.

## Prioritized overview

This table groups overlapping findings; the complete, numbered specialist proposals follow it. “Math 1” means item 1 in the math review, and similarly for Art and Teaching.

| Priority | Proposed change | Where | Reviewer references |
|---|---|---|---|
| Must fix | Orient recap boats by their water-relative velocity while moving them along the resultant. | 02:51–03:08 | Math 1; Art 2; Teaching 1 |
| Must fix | Rebuild miniature velocity triangles and trajectories from the actual solved vectors; use consistent scales and correct downstream drift. | 02:51–03:08 | Math 2–3; Art 3; Teaching 2 |
| Must fix | Correct the independently scaled velocity arrows, especially the part (b) physical overlay. | 02:27–02:30; smaller errors earlier | Math 4; Teaching 2 |
| Must fix | Separate recap captions, equations, arrowheads, banks, and moving boats; check the full motion envelope. | 02:51–03:08 | Art 4–5; Math 6; Teaching 13 |
| Must fix | Move the clipped “straight across is impossible” explanation fully inside the frame. | 01:56–01:59 | Art 1; Teaching 12 |
| High | Strengthen contrast for resultant arrows, routes, and essential explanatory text using a suitable tint or light text with colored accents. | Throughout | Art 6; Teaching 14 |
| High | Make clear that “largest feasible angle” refers to the resultant's path angle, not the boat-heading angle β; explain why tangency gives the shortest reachable route. | 01:55–02:25 | Math 5; Teaching 3, 5 |
| Before recording | Correct the narration draft's reversed u/v assignments and align cosine explanations with the visible triangles. | Both solution chapters | Math 11; Teaching 6–7 |
| Recommended | Improve the teaching sequence: one vector sum before the circle, enough reading time, progressive trig steps, continuous circle movement between cases, and a more deliberate recap. | Throughout | Teaching 4, 8–9, 11–13; Art 9–10, 14 |
| Recommended | Clarify labels, angle references, bank endpoints, right-angle marker placement, and the meaning of AB and W. | Both diagrams and physical scenes | Math 6–9, 12–13; Art 5, 7–8, 12; Teaching 6, 9–10 |
| Recommended / optional | Reduce answer-panel dominance; refine the water's tonal hierarchy and strengthen the inset's placement and finish. | River scenes and circle sweeps | Art 9, 11, 13 |
| Workflow | Allow low-resolution/low-FPS preview flags to work by removing unconditional export settings from the scene source. | Render configuration | Main reviewer W1 below |

## Reconciliation and preference notes

- **Final part (a) resultant:** Math 10, Art 7, and Teaching 9 propose retaining a w arrow through the final trigonometry. Your earlier request allowed omitting the net velocity there, and the existing version deliberately simplifies that step. This suggestion is retained for completeness, but it is an optional presentation choice. A compatible alternative is to identify the chosen resultant clearly immediately before the calculation, then fade it while preserving an unambiguous labelled direction reference. Keep the requested numerical cosine steps.
- **Correct answers versus incorrect depiction:** The main α and β answers, resultant speeds, and shortest-distance ratio are correct. The high-priority math proposals concern representations that fail to preserve those results, particularly the recap and brief physical-scene arrows.
- **Angle symbols:** If adding a path-angle proof, use a distinct symbol such as φ. The math review uses θ for boat heading; the teacher's suggested formula uses θ locally for path angle. Do not reuse one symbol for both meanings in the video.
- **Right-angle marker:** Preserve the valid perpendicularity statement, as the artist recommends, but move the marker inside the triangle as the math reviewer proposes.
- **Distance result:** Labelling AB and W, writing the relation in plain language, or omitting an unexplained extra result are alternatives. They are not instructions to add all three treatments.
- **Recap timing:** Sequential emphasis and synchronized comparison are editorial choices. Equal animation durations without an on-screen clock are not automatically a physics error. Correct vector geometry and boat orientation are required either way.
- **Already improved:** The current video has neutral dark banks distinct from the blue river, long title underlines, unclipped main answer panels, and an open recap without enclosing cards. Preserve these gains; the remaining left-edge caption clipping and recap overlaps are separate defects.
- **Evidence links:** Reviewer image links point to temporary inspection files under /tmp. They may expire. Timestamps, source locations, and written observations are included so each proposal remains traceable from the original video.

## Main reviewer: additional workflow proposal

### W1 — Make quick-preview settings effective

**Evidence:** [river_crossing_f5.py:23](/home/csongi/Documents/Furfangos_szeminarium/folyos_video/river_crossing_f5.py:23) unconditionally sets pixel width to 1920, pixel height to 1080, and frame rate to 60. The documented preview command uses `-ql`, but importing these scene-level assignments resets those choices. The preceding iteration also produced its “smoke” output in a `1080p60` directory.

**Proposal:** Let Manim's command-line quality settings control previews. Specify 1080p/60 FPS only in the final-export command or an explicitly selected final profile. Verify a future preview's actual dimensions and FPS with ffprobe before relying on it for fast iteration.

**Reason:** This makes the existing low-resolution/low-FPS work principle effective and avoids repeating expensive test renders. No preview or final render was run for this review.

## Complete math review — Halley

Math reviewer handoff: the numerical answers and main velocity-circle constructions are correct. The most serious errors are in the recap and the brief velocity overlay in part (b). All items below are proposals; no project files were changed and no Manim render was run.

Independent calculation, taking right as upstream and up as across:

\[
\vec u=(-U,0),\qquad
\vec v=(3\cos\theta,3\sin\theta),\qquad
\vec w=\vec u+\vec v,
\]
\[
\frac{L}{W}=\frac{\sqrt{U^2+9-6U\cos\theta}}{3\sin\theta}.
\]

Minimizing this gives:

| Current | Optimal heading from upstream bank direction | Boat velocity \(\vec v\) | Actual velocity \(\vec w\) | Shortest distance |
|---|---:|---|---|---|
| \(U=2\) | \(48.1897^\circ\) | \((2,\sqrt5)\) | \((0,\sqrt5)\) | \(W\) |
| \(U=4\) | \(41.4096^\circ\) | \((9/4,3\sqrt7/4)\) | \((-7/4,3\sqrt7/4)\) | \(4W/3\) |

For part (b), downstream displacement is \(\sqrt7\,W/3\approx0.881917W\). The actual path makes \(48.5904^\circ\) with the bank, and \(\vec v\cdot\vec w=0\).

1. **Must fix — recap, approximately 2:51–3:08: incorrect boat headings.**  
   **Evidence:** The 173.3–176.3 s motion sequence and [175 s still](/tmp/folyos_math_review_DnNNpX/still_175.jpg) show the left boat pointing straight across and the right boat pointing diagonally downstream. Their orientations follow their paths throughout.  
   **Why:** This directly contradicts the central lesson and the correctly oriented boats in the main demonstrations.  
   **Proposal:** Orient each boat using its water-relative velocity: upper-right at \(48.2^\circ\) for (a), upper-right at \(41.4^\circ\) for (b), while moving along the respective resultant. The current source explicitly uses `path_delta` for orientation at line 817.

2. **Must fix — recap, approximately 2:52–3:08: incorrect velocity proportions and angles.**  
   **Evidence:** In the [182 s still](/tmp/folyos_math_review_DnNNpX/still_182.jpg), the “river faster than boat” triangle visibly has a longer boat vector than current vector. Source coordinates confirm \(|v|/|u|\approx1.356\), whereas the required ratio is \(3/4\). Its heading is approximately \(55.0^\circ\), and the boat/resultant angle is \(46.3^\circ\), rather than \(90^\circ\). The left triangle also gives \(51.95^\circ\) rather than \(48.19^\circ\).  
   **Proposal:** Generate both recap triangles from the exact vectors above using uniform scaling within each diagram. Prefer a shared scale across the pair so the unchanged boat speed remains visually apparent.

3. **Must fix — recap, approximately 2:51–3:08: part (b) trajectory understates drift.**  
   **Evidence:** The right path is nearly vertical. Its source displacement is \((-0.38,1.62)\), giving drift/width \(0.2346\) and length/width \(1.0271\). The correct values are \(0.8819\) and \(1.3333\). It also differs slightly in direction from its own recap resultant.  
   **Why:** The final physical picture substantially misrepresents the optimum just derived.  
   **Proposal:** Derive the trajectory from \(\vec w\). For a rise of 1.62 drawing units, the downstream displacement should be approximately 1.429 units. Adjust the miniature’s dimensions or uniformly shrink it to accommodate that geometry.

4. **Must fix — approximately 2:27–2:29: part (b) velocity arrows do not add correctly.**  
   **Evidence:** The [148 s still](/tmp/folyos_math_review_DnNNpX/still_148.jpg) shows the current arrow shorter than the boat arrow. Source geometry gives the drawn sum \((-0.08,1.03184)\), while the displayed resultant is \((-1.085,1.23027)\).  
   **Why:** This overlay contradicts both \(w=u+v\) and the stated speeds, although the subsequent boat trajectory is correct.  
   **Proposal:** Apply one common scale to all three vectors. Also correct smaller scale inconsistencies in the introductory overlay and part (a): the introductory current/boat ratio is 0.724 rather than \(2/3\), and part (a)’s resultant is drawn about 7.5% too long.

5. **Recommended — approximately 2:09–2:25: specify which angle is maximized.**  
   **Evidence:** At [133 s](/tmp/folyos_math_review_DnNNpX/still_133.jpg), “largest feasible angle” appears alongside the sole marked angle, \(\beta\).  
   **Why:** \(\beta\) is the boat’s heading angle; it is not the largest feasible heading. The maximized quantity is the resultant’s acute angle to the downstream bank direction.  
   **Proposal:** Mark a separate angle at the resultant’s origin and label it explicitly. Connect it to shortest distance with \(L=W/\sin\phi\), or animate candidate paths terminating on the opposite bank. This would substantiate the tangent’s optimality without emphasizing another numerical answer.

6. **Recommended — recap, approximately 2:52–3:08: clarify vector-label attachment.**  
   **Evidence:** In the 175 s and 182 s stills, the `v` label sits beside the red resultant, while `w` sits beside the mint boat vector. Color conveys the intended association, but proximity suggests the reverse.  
   **Proposal:** Position each label beside the middle of its own arrow, offset along that arrow’s normal. Check both diagrams independently after correcting their geometry.

7. **Recommended — approximately 0:29–0:48 and the two physical demonstrations: make endpoints consistent with the banks.**  
   **Evidence:** At [40 s](/tmp/folyos_math_review_DnNNpX/still_40.jpg), the diagonal route ends beyond the upper bank while the perpendicular comparison stops at the bank. Source confirms the diagonal endpoint overshoots by 0.25 units. In the main results, the route starts 0.25 units inside the river.  
   **Why:** The shortest-path comparison should use the same starting point and opposite-bank boundary. In part (b), the drawn path is consequently \(1.2432\) times the full depicted bank separation, despite the \(4/3\) formula.  
   **Proposal:** Put the mathematical start/end reference points exactly on the bank lines; offset the boat artwork separately if needed.

8. **Recommended — approximately 2:35–2:48: define `AB` and `W` visually.**  
   **Evidence:** The result panel introduces `AB = (4/3) W`, but the diagram has no points A and B and no width label.  
   **Why:** The equation is correct, but its geometric quantities are left implicit.  
   **Proposal:** Label the departure and arrival points and add a simple perpendicular width marker, or write “path length = \(4/3\) × river width.” Briefly connecting these quantities to the triangle would strengthen the explanation.

9. **Recommended — approximately 2:10–2:25: move the right-angle marker inside the velocity triangle.**  
   **Evidence:** At 133 s, the square is outside the triangle, above-left of the tangency point.  
   **Qualification:** The lines really are perpendicular; this is a misleading marker placement, not an incorrect perpendicularity claim.  
   **Proposal:** Place the square between the two rays from the tangent point toward the origin and circle center.

10. **Recommended — approximately 1:09–1:24: retain the selected resultant in part (a).**  
    **Evidence:** At [72 s](/tmp/folyos_math_review_DnNNpX/still_72.jpg), the final construction retains the current and boat arrows, but the resultant has disappeared after the sweep. A bidirectional dashed reference line occupies its location.  
    **Why:** The final diagram no longer explicitly identifies the vector completing the displayed sum.  
    **Proposal:** Keep a labeled resultant arrow from the origin to the upper intersection, with the perpendicular reference behind it.

11. **Must fix before recording — planned narration around 0:48: reconcile the script’s symbols with the video.**  
    **Evidence:** The current video correctly uses `u` for river and `v` for boat. [Script_recommendations.md](/home/csongi/Documents/Furfangos_szeminarium/folyos_video/Script_recommendations.md:51) instructs the opposite, also repeated near its beginning.  
    **Proposal:** Update the proposed narration to the user’s established mapping, retaining \(w=u+v\). This is a future narration mismatch, not a missing-audio defect.

12. **Recommended — approximately 0:19–0:48: tighten the terminology.**  
    **Evidence:** The subtitle says “Heading and path are different vectors.” A path is a trajectory, while a heading is a direction.  
    **Proposal:** Use “Boat heading and direction of motion differ,” and explicitly define `v` relative to water and `w` relative to the bank. Bold vector notation can be valid; arrow accents are an optional clarity improvement, not a mathematical requirement.

13. **Optional — opening and recap: clarify assumptions and time interpretation.**  
    **Proposal:** Briefly establish parallel banks, uniform current, constant 3 m/s through-water speed, and unrestricted landing position. If simultaneous recap motion is intended to represent a shared physical clock, let (b) finish approximately 12.7% later than (a) for equal widths. With no clock shown, synchronized illustrative playback is not independently a physics error.

Worth preserving: the current flows right-to-left; the main boat headings and straight trajectories are correct; the velocity circles have the correct radii and offsets; the impossibility of canceling the 4 m/s current is correctly represented; and both angle formulas, resultant speeds, and the \(4W/3\) answer are correct. Preserve the animated comparison in the recap while correcting its geometry.

Evidence limitation: I inspected modest-resolution rendered stills and sampled motion sequences, supplemented by source coordinates for exact measurements. This was not a frame-by-frame 60 fps audit. No aesthetic judgment or audio assessment is included. Evidence remains in `/tmp/folyos_math_review_DnNNpX`.

## Complete art review — Hooke

Artist handoff complete. I inspected targeted stills and sequential frames from the current render, with source checks for geometry. No project writes or Manim rendering. Evidence: [/tmp/river_artist_review.3mOp3e](/tmp/river_artist_review.3mOp3e).

1. **Must fix — 1:56–1:59: clipped explanation.**  
   **Observed:** “straight across is impossible” extends off the left edge; the explanation crowds the circle’s top.  
   **Propose:** Move the two-line explanation into the empty right half, approximately `(3.0, 1.2)` in scene coordinates. The circle itself is not clipped.

2. **Must fix — recap, 2:51–3:08: incorrect boat orientation.**  
   **Mathematical/visual encoding:** The left boat points straight across; the right boat points diagonally left along its downstream trajectory. Both should point diagonally right, upstream. Source confirms orientation uses `path_delta`.  
   **Propose:** Orient boats using their boat-through-water vectors while moving them along the resultant paths. Preserve the correct upstream orientations already present in the main physical-result scenes.

3. **Must fix — recap, 2:52–3:08: misleading vector geometry.**  
   **Mathematical/visual encoding:** In the “river faster” diagram, the mint boat vector is visibly longer than the current vector. Source lengths are approximately `0.98` versus `0.72`; the miniature also loses the tangent triangle’s perpendicular relationship.  
   **Propose:** Derive both recap triangles and trajectories from scaled versions of the actual case vectors. Keep these diagrams geometrically accurate without adding numerical answer cards.

4. **Must fix — recap, 2:51–3:08: persistent text/diagram collisions.**  
   **Observed:** Upper banks cross “boat movement”; arriving boats overlap those captions. Vector arrowheads intrude into `w = u + v`.  
   **Propose:** Reserve distinct rows for titles, captions/equations, and graphics. Raise titles/captions into the unused space beneath the header and maintain clearance for each boat’s complete animated envelope, including arrival.

5. **Recommended — recap: disconnected river construction.**  
   **Observed:** Blue water stops short of the mint banks. In case (b), the banks are horizontally staggered against a rectangular water area.  
   **Propose:** Derive both banks from the water rectangle’s edges and place crossing endpoints on them. Make the river wide enough to contain downstream displacement.

6. **Must fix — throughout: weak carmine contrast.**  
   **Observed:** Resultant paths, “but not shortest,” the `w` legend, `AB = (4/3) W`, and “drifts downstream” are substantially weaker than nearby mint/white elements. Source-color contrast is approximately 1.46:1 against water and 2.35:1 against the panel.  
   **Propose:** Use a lighter carmine tint for essential result vectors and text, or near-white explanatory text with carmine accents. Preserve a distinguishable pink current color. These ratios describe source colors, not every composited frame.

7. **Recommended — 1:06–1:24: clarify the final part (a) construction.**  
   **Observed:** “shortest path direction” crosses the circle and selected boat vector. Numerous ghost spokes remain, while the selected carmine resultant disappears.  
   **Propose:** Move the direction caption outside the circle into the right-side gap, using two lines and a short leader. Remove unused spokes after selection and retain a labeled carmine `w` arrow alongside the perpendicular reference.

8. **Recommended — 1:54–2:25: improve part (b) label placement.**  
   **Observed:** `|v| = 3` crosses the circle outline. The final triangle lacks direct `v`/`w` labels despite the detached `v ⟂ w` statement.  
   **Propose:** Put the radius caption below the circle, consistently with part (a), and label the selected segments away from the tangent point. Preserve the visible right-angle marker.

9. **Recommended — both sweeps, approximately 0:59–1:05 and 2:00–2:06: strengthen the visual landing.**  
   **Observed:** Both vector sweeps and rotating boat insets work, but the inset is small and isolated low on the right. Selected arrows fade away before the next construction appears.  
   **Propose:** Enlarge the inset approximately 40–50%, move it upward into available space, and ease into the selected heading. Hold briefly, then retain or transform those arrows directly into the final diagram.

10. **Recommended — 0:23–0:24: increase readable dwell.**  
    **Observed:** The rejected-heading captions are clearly visible only briefly; their entrance overlaps the departing pause prompt.  
    **Propose:** Complete the prompt’s exit first and allow roughly 2–3 seconds of full visibility for the captions. Exact timing should follow the eventual voiceover.

11. **Recommended — physical results, approximately 1:35–1:50 and 2:35–2:48: reduce panel dominance.**  
    **Observed / subjective assessment:** The rounded panels fit their text but occupy over half the image width, outweighing the route and boat. Part (a)’s extra pill almost touches the lower bank.  
    **Propose:** Use narrower, deliberately wrapped answer blocks; prioritize heading over speed. Integrate the extra pill’s wording or increase bank clearance. Consider reduced fill opacity and minimal borders while maintaining legibility.

12. **Recommended — 2:35–2:48: connect the path-length statement to its diagram.**  
    **Observed:** `AB = (4/3) W` appears without corresponding A, B, or W labels on the river.  
    **Propose:** Add unobtrusive endpoint/width labels, or replace that line with “path length = 4/3 × river width.” This is a labeling issue, not a claim that the formula is wrong.

13. **Optional — opening and river scenes: refine tonal hierarchy.**  
    **Observed / subjective suggestion:** Saturated blue water and mint banks dominate; current marks are faint. The lighter water strip has visibly abrupt boundaries.  
    **Propose:** Test darker Egyptian Blue water, slightly quieter bank lines, and modestly stronger current marks. Soften or remove the central strip. Keep the established palette family and leftward current.

14. **Recommended — recap, 2:48–3:08: allocate more space and time to animation.**  
    **Observed:** The boats cross for roughly two seconds, followed by a long static ending. Small diagrams leave considerable unused space.  
    **Propose:** After repairing layout, enlarge diagrams approximately 30–40% and stage vector addition, heading emphasis, and crossing as distinct beats. Use some final-hold time for another crossing or coordinated vector/path highlight.

Preserve the opening’s balanced composition, bold italic monospace treatment, u/current and v/boat convention, mint boat design, both functioning sweeps, correct main-scene boat headings, and recap without enclosing cards. A font replacement is not a requirement.

Uncertainty: sampling cannot exclude isolated one-frame artifacts or establish full-speed smoothness. Timing recommendations remain provisional until narration exists; missing audio is not a defect. The recap geometry findings are confirmed by source checks as well as rendered evidence.

## Complete teaching review — Huygens

Teacher reviewer — proposals for the main agent only. I inspected the current MP4 using overview stills, targeted frames, and sequences around the prediction, circle construction, tangency, and recap. Evidence is in [/tmp/teacher-river-review-7AiRQg](/tmp/teacher-river-review-7AiRQg). No project files were changed; no Manim rendering was performed.

1. **Must fix — 2:50–3:08: recap boats contradict the central lesson.**  
   **Observed physical error:** In the [174.5-second frame](/tmp/teacher-river-review-7AiRQg/174.5-recap.png) and surrounding sequence, the left boat points straight across; the right boat points diagonally downstream. Both follow their noses. Earlier physical demonstrations correctly show an upstream heading while travelling in another direction. Source confirms the recap orients boats using `path_delta`.  
   **Proposal:** Orient each boat using its water-relative velocity, and translate it along the resultant. Retain this difference throughout the movement and final hold. Otherwise, the final image teaches precisely the misconception the video aims to resolve.

2. **Must fix — approximately 2:27–2:30 and 2:51–3:08: preserve the velocity geometry when simplifying diagrams.**  
   **Observed mathematical depiction error:** At [148.5 seconds](/tmp/teacher-river-review-7AiRQg/148.5-vectors.png), the current arrow is shorter than the boat arrow despite representing 4 versus 3 m/s. Source confirms independent scales for the three arrows. In the recap’s part (b), the boat vector also exceeds the current vector: their source lengths are approximately 0.977 and 0.72. Its boat and resultant vectors are visibly not perpendicular, unlike the preceding tangent solution.  
   **Proposal:** Reuse the solved velocity components with one scale per diagram. Derive the physical path direction from that same resultant. This should also cover the slightly inconsistent resultant length in the part (a) physical scene. Compact diagrams can remain simple while preserving the relationships being taught.

3. **Must fix — approximately 2:09–2:25: identify which angle is being maximized.**  
   **Observed ambiguity, not an incorrect numerical answer:** The [138-second frame](/tmp/teacher-river-review-7AiRQg/138-tangent.png) places “largest feasible angle” beside the only marked angle, β. However, β describes the boat heading. The optimized angle is between the resultant and the downstream bank direction; here it is approximately 48.6°, while β is approximately 41.4°.  
   **Proposal:** Attach the optimization statement explicitly to the resultant. Either briefly mark a separate path angle, or use “reachable path closest to straight across.” Then introduce β separately as the heading measured from upstream.

4. **Recommended — 0:25–0:48: demonstrate why fastest and shortest differ.**  
   **Observed teaching gap:** The diagonal movement and later vertical reference show different routes, but “fastest crossing” is asserted without a visible explanation.  
   **Proposal:** Briefly show that the current contributes no cross-river component, and that pointing straight across gives the boat’s maximum cross-river component. Then compare the diagonal distance with the perpendicular bank separation. A short component animation and geometric comparison would support the claims without adding substantial algebra.

5. **Recommended — 1:55–2:10: make tangency an optimization argument.**  
   **Observed teaching gap:** The moving vectors demonstrate possible velocities, then the tangent solution appears. They do not clearly demonstrate why this particular reachable direction minimizes distance.  
   **Proposal:** Rotate a ray from the velocity origin toward straight across: first show intersection, then tangency, then a slightly steeper ray missing the circle. Link that rotation to routes between the banks. If an equation is helpful, use one relation, \(L=W/\sin\theta\), with θ explicitly defined as the path angle to the bank. The physical route comparison should carry the explanation.

6. **Must fix before recording — principally 0:48–1:24: reconcile the narration’s notation with the video.**  
   **Verified script mismatch:** The current video correctly uses **u = river, v = boat**, but [Script_recommendations.md:51](/home/csongi/Documents/Furfangos_szeminarium/folyos_video/Script_recommendations.md:51) assigns them oppositely.  
   **Proposal:** Update the future narration to the requested convention and explicitly define u relative to the bank, v relative to the water, and w relative to the bank. “Actual velocity” alone leaves the reference frame implicit. The early subtitle “Heading and path are different vectors” could also become “Where the boat points and where it travels can differ”; a path is not itself a velocity vector.

7. **Recommended — 1:10–1:50 and 2:11–2:48: align explanations with the diagrams they explain.**  
   **Verified scheduling mismatch:** The α derivation appears around 1:10–1:24 and disappears when its proposed narrated explanation starts at 1:24. Similarly, the β triangle disappears at 2:25, when the script begins explaining that triangle and its cosine.  
   **Proposal:** Keep the relevant triangle visible through the component/cosine explanation, or move those spoken lines earlier. Transfer the heading to the physical boat only after the angle is established. These are proposals for future recording and timing; no existing audio synchronization failure is being alleged.

8. **Recommended — approximately 0:50–1:05: build one complete vector sum before displaying all possibilities.**  
   **Observed sequence:** The equation and legend appear, then the circle, then numerous sample vectors; the prominent moving vector pair comes afterwards.  
   **Proposal:** First demonstrate one u arrow, one v arrow translated to its tip, and w joining the overall endpoints. Then rotate v to generate the circle. Explicitly distinguish the circle centre from the resultant’s origin. This gives novices a reason for the circle and reduces the risk of interpreting it as the boat’s spatial trajectory.

9. **Recommended — approximately 1:05–1:24: retain the selected resultant and connect the triangle to the equation.**  
   **Observed evidence:** In the [76-second frame](/tmp/teacher-river-review-7AiRQg/076-formula.png), the selected boat vector is prominent, but the final resultant is represented by a dashed vertical direction line rather than a clearly labelled carmine w arrow. The five algebraic lines arrive together.  
   **Proposal:** Keep u, v, and the chosen w visible; dim the unused construction further. Highlight the horizontal projection of v as it cancels u, then reveal the cosine steps in sequence. Label the horizontal reference as upstream/bank-parallel, and carry the same α onto the physical boat before its crossing.

10. **Recommended — approximately 2:35–2:48: define the quantities in the distance result.**  
    **Observed evidence:** The [160-second frame](/tmp/teacher-river-review-7AiRQg/160-result.png) shows `AB = (4/3) W`, but neither A, B, nor W is labelled on the river. The relation is mathematically correct, but the displayed geometry does not explain it.  
    **Proposal:** Mark the endpoints and bank separation, then link the path triangle to the velocity triangle. Alternatively, omit the extra distance result if it will not be explained. For geometric consistency, use the same shore-based endpoint convention throughout: the early fastest-crossing example visibly carries the boat’s centre slightly beyond the far bank, while other demonstrations end at it.

11. **Recommended — approximately 0:23–0:24: give the rejected choices enough reading and explanation time.**  
    **Observed motion evidence:** The [0.2-second sequence](/tmp/teacher-river-review-7AiRQg/choices-22.5-sequence.jpg) confirms that both explanatory lines fade in and immediately fade away, without a stable reading hold. Their entire transition occupies about 1.4 seconds.  
    **Proposal:** Present them individually alongside a corresponding heading, or retain them through the relevant spoken sentence. Preserve the corrected word **“directly”** in “directly upstream”: diagonal upstream rowing is the eventual solution.

12. **Recommended — 1:50–2:00: show the changing constraint continuously.**  
    **Observed evidence:** “The circle moves, but its radius stays 3” accompanies a newly drawn diagram after a scene clearance; the viewer does not see the previous circle move. The “straight across is impossible” caption also extends beyond the left edge during the [no-intersection sequence](/tmp/teacher-river-review-7AiRQg/no-intersection-sequence.jpg).  
    **Proposal:** Briefly restore the previous velocity construction, lengthen u from 2 to 4, and move the fixed-radius circle with its endpoint. Keep the impossibility statement fully readable beside the newly opened gap. This directly explains why the first method becomes unavailable.

13. **Recommended — 2:48–3:08: give the recap a teaching sequence after correcting its geometry.**  
    **Observed evidence:** Both vector constructions animate simultaneously, both boats cross together in approximately 2.2 seconds, and the remaining ending largely holds. In the [recap frame](/tmp/teacher-river-review-7AiRQg/174.5-recap.png), the v labels sit near the resultant arrows, while triangle tips intrude into the equations. This makes matching symbols, heading, and motion unnecessarily difficult.  
    **Proposal:** Briefly emphasize one case, demonstrate its heading-to-resultant-to-motion relationship, then do the other and finish with both visible. Position each label unambiguously beside its own arrow. Use some of the final hold for a second focused demonstration rather than additional numerical answers. An optional retrieval prompt could ask the learner to predict the path before the second boat moves.

14. **Recommended — approximately 0:32–0:48 and 2:35–2:48: protect teaching-critical contrast.**  
    **Observed visual evidence:** “but not shortest,” the downstream route, and `AB = (4/3) W` are substantially harder to read than the mint heading information.  
    **Proposal:** Ask the visual reviewer to strengthen the carmine-derived shade or its immediate background contrast for these elements. This matters pedagogically because the difficult-to-see information carries the distinction between heading and actual travel. Additional boxes are unnecessary.

Worth preserving: the principal α and β results are correct, as are \(\sqrt5\), \(\sqrt7\), and \(4W/3\). The main physical crossings correctly distinguish upstream heading from movement. The current consistently runs right to left, and the video’s u/v convention is already correct. The moving circle endpoint and rotating boat inset are useful teaching devices. The animated recap concept deserves preservation and refinement.

Limitations: this was rendered-frame and sampled-sequence inspection, supported by source geometry and timing checks, rather than uninterrupted playback or a novice comprehension test. Reading-time and instructional-sequence judgments are recommendations; the recap orientation, inconsistent vector geometry, and script notation conflict are directly verified. Missing audio is intentional and is not a defect.

## Completion record

All three reviews are included above: 41 numbered specialist entries, plus the main reviewer's workflow proposal. These entries include overlapping findings and optional alternatives. Only this Markdown report was added to the project; the video, Manim source, scripts, palette, and work-principles file were left unchanged. No proposed correction has been implemented.

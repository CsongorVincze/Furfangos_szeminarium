# Recommended corrections for “333 Problem 5”

## The important physics corrections

1. Keep three velocities distinct throughout:
   - **River velocity relative to the bank:** \(\vec u\), with \(|\vec u|=2\,\mathrm{m/s}\) or \(4\,\mathrm{m/s}\).
   - **Boat velocity relative to the water:** \(\vec v\), with \(|\vec v|=3\,\mathrm{m/s}\).
   - **Actual boat velocity relative to the bank:** \(\vec w=\vec u+\vec v\).

2. “Pointing the boat straight across” and “travelling straight across” are not the same thing. Pointing straight across maximizes the cross-river component, so it minimizes the **crossing time**, but the current makes the actual path diagonal. The problem asks for the **shortest path**.

3. The sentence “If you row against the stream, you end up not moving away from the bank” is only true if the boat points **directly** upstream. Pointing diagonally upstream is exactly what the optimal solution requires.

4. In part (a), describe \(\alpha\) unambiguously. The answer is
   \[
   \cos\alpha=\frac{2}{3},\qquad \alpha\approx48.2^\circ,
   \]
   where \(\alpha\) is the angle between the boat’s heading and the bank, measured from the upstream direction. Equivalently, the boat points \(41.8^\circ\) upstream from the straight-across direction.

5. The original draft stops after part (a). Part (b) needs the tangent construction:
   \[
   \cos\beta=\frac{3}{4},\qquad \beta\approx41.4^\circ.
   \]
   Here \(\beta\) is again measured from the bank on the upstream side. The actual path is diagonal downstream and has length \(4/3\) of the river width.

## Language and presentation corrections

- Use **bank**, not “coast,” for a river.
- Use one verb consistently; **row** works best for the wording of the problem.
- Replace “The good news are” with **“The good news is.”**
- Replace “our velocity” with **“the boat’s velocity relative to the water.”** This avoids confusion about reference frames.
- Say **“a circle of radius 3”**, not “a circle with length/radius 3.”
- Use spaces between values and units: **3 m/s**, **48.2°**.
- Correct the spelling errors in the draft: *speed, everywhere, stream, other, problem, earlier, about, vectors, length, radius, velocity, circle,* and *resultant*.
- Pause briefly whenever the diagram changes meaning: heading vector, current vector, and resultant vector should not appear all at once.

## Suggested voiceover script and timing

The animation is paced to the following version. The timings are targets rather than frame-perfect constraints; speak naturally and leave a short breath around each section change.

### 0:00-0:18 — Problem

Here is the problem. A boat moves at 3 metres per second relative to still water. A uniform river current flows along the bank. Which heading makes the boat’s path from one bank to the other as short as possible? Consider currents of 2 and 4 metres per second.

### 0:18-0:48 — Pause and think

Start with the slower current. Pause the video and predict the best heading. Pointing downstream adds drift, while pointing directly upstream gives no motion across. Pointing straight across maximizes the cross-river speed, so it gives the fastest crossing. But the current makes the actual path diagonal. Fastest is not shortest. The shortest path between parallel banks is perpendicular, so the boat’s actual velocity - not merely its heading - must point straight across.

### 0:48-1:24 — Vector picture for part (a)

Let \(\vec u\) be the current velocity and \(\vec v\) the boat’s velocity relative to the water. The actual velocity is their sum: \(\vec w=\vec u+\vec v\). Draw the current vector with length 2, pointing downstream. From its tip, draw every possible boat-velocity vector. They all have length 3, so their endpoints form a circle of radius 3. Every possible resultant starts at the origin and ends on this circle. For the shortest path, choose a resultant that points straight across. The perpendicular line intersects the circle, so this is possible.

### 1:24-1:50 — Answer to part (a)

The upstream component of the boat’s velocity must cancel the current. If \(\alpha\) is the angle between the heading and the bank, then \(3\cos\alpha=2\). Therefore \(\cos\alpha=2/3\), giving \(\alpha\approx48.2^\circ\). Point the boat 48.2 degrees to the bank, aimed upstream. Its actual speed is \(\sqrt{3^2-2^2}=\sqrt5\) metres per second, and its path is straight across: the absolute shortest route.

### 1:50-2:25 — Vector picture for part (b)

Now increase the current to 4 metres per second. The circle’s centre moves to 4, while its radius stays 3. The perpendicular line through the origin misses the circle. The current is too strong to cancel, so a straight-across path is impossible. Choose the reachable direction that comes closest to perpendicular. In the velocity diagram, this is the line from the origin tangent to the circle. At the tangent point, the boat-velocity vector is perpendicular to the resultant.

### 2:25-2:48 — Answer to part (b)

The tangent construction gives a right triangle. If \(\beta\) is the angle between the heading and the bank on the upstream side, then \(\cos\beta=3/4\), so \(\beta\approx41.4^\circ\). The boat still moves downstream as it crosses. Its resultant speed is \(\sqrt{4^2-3^2}=\sqrt7\) metres per second, and its path length is four thirds of the river width.

### 2:48-3:08 — Summary

In both cases, point the boat upstream. With a current of 2 metres per second, aim 48.2 degrees to the bank and cancel the drift. With a current of 4 metres per second, aim 41.4 degrees and accept some downstream drift. The key is to distinguish the heading from the actual path.

## Visual plan used for the Manim animation

- Introduce the river, the 3 m/s boat speed, and the two current speeds.
- Show why pointing straight across is fastest but produces a diagonal path.
- Build the velocity sum one vector at a time.
- Sweep fixed-length boat vectors to reveal the circle of possible endpoints.
- For part (a), intersect the circle with the perpendicular direction.
- For part (b), show that there is no intersection, then construct the tangent.
- Return to the river after each vector construction so the geometric answer is connected to the physical path.
- Finish with an open side-by-side comparison of the two vector additions and boat motions that can remain on screen while the voiceover concludes.

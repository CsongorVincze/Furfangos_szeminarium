"""Small-step intuition builder for problem F.4.

The three snails start at the vertices of an equilateral triangle.  At every
update they move simultaneously by a fixed distance toward the next snail:

    A -> B,  B -> C,  C -> A

The update is intentionally discrete, so the trails approximate the
logarithmic spirals from the solution rather than pretending to be exact.

Adjust STEP_CM and NUM_STEPS below, then render with Manim.  Environment
variables SNAIL_STEP_CM and SNAIL_NUM_STEPS override the defaults when useful.
"""

import os

import numpy as np
from manim import *


config.background_color = "#0B1020"


# Problem scale and the two useful controls for experimenting with the
# approximation.  The scene maps the 60 cm triangle side to 5 scene units.
SIDE_CM = 60.0
SPEED_CM_PER_MIN = 5.0
SCENE_SIDE = 5.0
STEP_CM = float(os.environ.get("SNAIL_STEP_CM", "2.0"))
NUM_STEPS = int(os.environ.get("SNAIL_NUM_STEPS", "20"))
STEP_SIZE = STEP_CM / SIDE_CM * SCENE_SIDE
STEP_TIME_MIN = STEP_CM / SPEED_CM_PER_MIN
STEP_DURATION = 0.18
MEETING_THRESHOLD = 2.0 * STEP_SIZE
ARROW_MIN_DISTANCE = max(0.75, 4.5 * STEP_SIZE)
LABEL_FADE_DISTANCE = max(0.9, 5.0 * STEP_SIZE)


COLORS = {
    "a": "#F6C85F",
    "b": "#56CCF2",
    "c": "#BB6BD9",
    "ink": "#F5F7FA",
    "muted": "#AAB5C4",
    "grid": "#334155",
    "accent": "#FF7A59",
}


def compute_positions(num_steps):
    """Return positions after each simultaneous fixed-length update."""
    radius = SCENE_SIDE / np.sqrt(3.0)
    angles = np.array([90.0, 210.0, 330.0]) * DEGREES
    positions = np.array([
        [radius * np.cos(angle), radius * np.sin(angle), 0.0]
        for angle in angles
    ])
    history = [positions.copy()]

    for _ in range(num_steps):
        next_positions = []
        for index, position in enumerate(positions):
            target = positions[(index + 1) % 3]
            direction = target - position
            distance = np.linalg.norm(direction)
            if distance == 0:
                next_positions.append(position.copy())
                continue
            move = min(STEP_SIZE, distance)
            next_positions.append(position + move * direction / distance)
        next_positions = np.array(next_positions)

        # A finite-step scheme can otherwise overshoot and leave a tiny
        # rotating triangle.  Once the remaining gap is only a couple of
        # step lengths, use the natural limiting picture: all meet at the
        # centroid.
        if np.linalg.norm(next_positions[1] - next_positions[0]) <= MEETING_THRESHOLD:
            positions = np.mean(next_positions, axis=0)
            next_positions = np.repeat(positions[None, :], 3, axis=0)

        positions = next_positions
        history.append(positions.copy())
    return history


def make_triangle(points):
    return Polygon(
        *points,
        stroke_color=COLORS["muted"],
        stroke_width=2,
        fill_color=COLORS["accent"],
        fill_opacity=0.035,
    )


def make_direction_marker(start, target):
    direction = target - start
    direction = direction / np.linalg.norm(direction)
    line = Line(
        start + 0.14 * direction,
        target - 0.22 * direction,
        stroke_width=2,
        color=COLORS["muted"],
    )
    tip = Triangle(
        fill_color=COLORS["muted"],
        fill_opacity=1,
        stroke_width=0,
    ).scale(0.11)
    tip.rotate(np.arctan2(direction[1], direction[0]) - PI / 2)
    tip.move_to(target - 0.18 * direction)
    return VGroup(line, tip)


def make_trail(points, color):
    trail = VMobject()
    trail.set_points_as_corners(points)
    trail.set_fill(opacity=0)
    trail.set_stroke(color=color, width=4, opacity=0.72)
    return trail


def update_trail(mob, points):
    mob.set_points_as_corners(points)
    mob.set_opacity(0.72)
    mob.set_fill(opacity=0)


class SnailsChaseTriangle(Scene):
    def construct(self):
        history = compute_positions(NUM_STEPS)
        snail_colors = [COLORS["a"], COLORS["b"], COLORS["c"]]
        snail_names = ["A", "B", "C"]
        label_offsets = [UP * 0.18, DOWN * 0.20 + LEFT * 0.16, DOWN * 0.20 + RIGHT * 0.16]

        title = Text("Three snails, one chase", font_size=38, color=COLORS["ink"])
        title.to_edge(UP, buff=0.28)
        controls = Text(
            f"step = {STEP_CM:g} cm    |    Δt = {STEP_TIME_MIN:.2f} min",
            font_size=21,
            color=COLORS["muted"],
        )
        controls.to_corner(UL, buff=0.34).shift(DOWN * 0.45)
        caption = Text(
            "Each snail moves a fixed step toward the next one.",
            font_size=23,
            color=COLORS["muted"],
        )
        caption.to_edge(DOWN, buff=0.32)

        center = Dot(ORIGIN, radius=0.06, color=COLORS["accent"])
        center_label = Text("meeting point", font_size=19, color=COLORS["accent"])
        center_label.next_to(center, DOWN, buff=0.12)

        step_label = Text("step", font_size=21, color=COLORS["muted"])
        step_number = Text("0", font_size=22, color=COLORS["ink"])
        step_total = Text(f"/ {NUM_STEPS}", font_size=21, color=COLORS["muted"])
        counter = VGroup(step_label, step_number, step_total).arrange(RIGHT, buff=0.08)
        counter.to_corner(UR, buff=0.34).shift(DOWN * 0.45)

        initial_points = history[0]
        triangle = make_triangle(initial_points)
        arrows = VGroup(*[
            make_direction_marker(
                initial_points[index], initial_points[(index + 1) % 3]
            )
            for index in range(3)
        ])
        dots = VGroup(*[
            Dot(point, radius=0.12, color=snail_colors[index])
            for index, point in enumerate(initial_points)
        ])
        labels = VGroup(*[
            Text(name, font_size=23, color=snail_colors[index]).move_to(
                point + label_offsets[index]
            )
            for index, (name, point) in enumerate(zip(snail_names, initial_points))
        ])
        trails = VGroup(*[
            make_trail([point, point + 0.001 * RIGHT], snail_colors[index]).set_opacity(0)
            for index, point in enumerate(initial_points)
        ])

        self.play(
            FadeIn(title),
            FadeIn(controls),
            FadeIn(caption),
            FadeIn(counter),
            FadeIn(center),
            FadeIn(center_label),
            FadeIn(triangle),
            FadeIn(arrows),
            FadeIn(dots),
            FadeIn(labels),
            run_time=1.3,
        )
        self.wait(0.5)

        for step in range(NUM_STEPS):
            old_points = history[step]
            new_points = history[step + 1]
            new_triangle = make_triangle(new_points)
            new_paths = [
                [frame[index] for frame in history[: step + 2]]
                for index in range(3)
            ]
            arrow_animations = []
            for index in range(3):
                arrow_start = new_points[index]
                arrow_target = new_points[(index + 1) % 3]
                arrow_distance = np.linalg.norm(arrow_target - arrow_start)
                if arrow_distance > ARROW_MIN_DISTANCE:
                    arrow_animations.append(
                        arrows[index].animate.become(
                            make_direction_marker(arrow_start, arrow_target)
                        ).set_opacity(1)
                    )
                else:
                    arrow_animations.append(arrows[index].animate.set_opacity(0))
            remaining_gap = np.linalg.norm(new_points[1] - new_points[0])
            if remaining_gap <= LABEL_FADE_DISTANCE:
                label_animations = [
                    labels[index].animate.move_to(
                        new_points[index] + label_offsets[index]
                    ).set_opacity(0)
                    for index in range(3)
                ]
            else:
                label_animations = [
                    labels[index].animate.move_to(
                        new_points[index] + label_offsets[index]
                    )
                    for index in range(3)
                ]

            new_step_number = Text(
                str(step + 1), font_size=22, color=COLORS["ink"]
            ).move_to(step_number)

            self.play(
                *[
                    dots[index].animate.move_to(new_points[index])
                    for index in range(3)
                ],
                *[
                    label_animation for label_animation in label_animations
                ],
                *[
                    UpdateFromFunc(
                        trails[index],
                        lambda mob, points=new_paths[index]: update_trail(mob, points),
                    )
                    for index in range(3)
                ],
                *arrow_animations,
                triangle.animate.become(new_triangle),
                step_number.animate.become(new_step_number),
                run_time=STEP_DURATION,
                rate_func=linear,
            )

        final_caption = Text(
            "The repeated steps curl all three paths toward the same point.",
            font_size=23,
            color=COLORS["ink"],
        )
        final_caption.move_to(caption.get_center())
        self.play(FadeOut(caption), FadeIn(final_caption), run_time=0.5)
        self.wait(1.5)

        self.play(
            FadeOut(VGroup(triangle, arrows, dots, labels, trails, center, center_label)),
            FadeOut(title),
            FadeOut(controls),
            FadeOut(counter),
            FadeOut(final_caption),
            run_time=0.8,
        )

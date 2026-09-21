"""Silent Manim animation for Problem F.5 from *333 furfangos feladat*.

The scene follows the revised voiceover in ``Script_recommendations.md``.
Its section boundaries are paced for a roughly 3:08 narration, while the
environment variable ``RIVER_PACE`` can scale the whole timeline.

Preview:
    manim -pql --media_dir folyos_video/rendered \
        folyos_video/river_crossing_f5.py RiverCrossingF5

Final render:
    manim -pqh --fps 60 --media_dir folyos_video/rendered \
        folyos_video/river_crossing_f5.py RiverCrossingF5
"""

import os

import numpy as np
from manim import *


config.background_color = "#FFFFFF"


COLORS = {
    # Roles follow work-principles/color_palette.png.  The scene uses the
    # light end of each family for explanatory objects and reserves the
    # deeper swatches for labels, vectors, and outlines.
    "water": "#C7E9F1",        # light blue A: river fill
    "water_light": "#9CDCEB",  # light blue B: soft water variation
    "bank": "#C9E2AE",         # light green A: shore fill
    "bank_edge": "#77B05D",    # green D: shore boundary
    "ink": "#222222",          # darker grey: primary text and outlines
    "muted": "#444444",        # dark grey: supporting labels
    "grid": "#29ABCA",         # blue D: geometry and panel outlines
    "boat": "#5CD0B3",         # teal C: boat and boat-through-water vector
    "current": "#C55F73",      # maroon C: river-current vector
    "result": "#CF5044",       # red E: actual/resultant velocity
    "result_light": "#F7A1A3", # red A: lighter path/result route
    "accent": "#E1A158",       # gold D: selected/optimal construction
    "warning": "#C78D46",      # gold E: cautionary alternatives
    "panel": "#F0F5F3",        # pale neutral panel on the white canvas
}

# Consolas is not installed in the Linux render environment.  Noto Sans Mono
# is the closest available monospace fallback, and the wrapper below applies
# the requested bold-italic treatment consistently to every prose text object.
FONT = "Noto Sans Mono"
_MANIM_TEXT = Text


def Text(text, *args, **kwargs):
    kwargs.setdefault("slant", "ITALIC")
    kwargs.setdefault("weight", "BOLD")
    return _MANIM_TEXT(text, *args, **kwargs)


PACE = float(os.environ.get("RIVER_PACE", "1.0"))


def make_boat(color=COLORS["boat"], scale=1.0):
    """A small top-view boat whose default heading is upward."""
    hull = Polygon(
        LEFT * 0.28 + DOWN * 0.38,
        RIGHT * 0.28 + DOWN * 0.38,
        RIGHT * 0.34 + UP * 0.10,
        UP * 0.48,
        LEFT * 0.34 + UP * 0.10,
        stroke_color=COLORS["ink"],
        stroke_width=2,
        fill_color=color,
        fill_opacity=1,
    )
    cockpit = RoundedRectangle(
        width=0.30,
        height=0.30,
        corner_radius=0.08,
        stroke_color=COLORS["ink"],
        stroke_width=1.4,
        fill_color=COLORS["panel"],
        fill_opacity=0.9,
    ).shift(DOWN * 0.05)
    nose = Triangle(
        stroke_width=0,
        fill_color=COLORS["ink"],
        fill_opacity=1,
    ).scale(0.055).move_to(UP * 0.35)
    return VGroup(hull, cockpit, nose).scale(scale)


def orient_boat(boat, vector):
    angle = np.arctan2(vector[1], vector[0])
    boat.rotate(angle - PI / 2)
    return boat


def pill(text, color=COLORS["ink"], width=2.7, font_size=24):
    label = Text(text, font=FONT, font_size=font_size, color=color)
    padded_width = max(width, label.width + 0.62)
    box = RoundedRectangle(
        width=padded_width,
        height=0.62,
        corner_radius=0.30,
        stroke_color=color,
        stroke_width=1.1,
        stroke_opacity=0.58,
        fill_color=COLORS["panel"],
        fill_opacity=0.80,
    )
    label.move_to(box)
    return VGroup(box, label)


def formula_panel(*rows, width=4.7):
    contents = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    padded_width = max(width, contents.width + 0.88)
    panel = RoundedRectangle(
        width=padded_width,
        height=contents.height + 0.70,
        corner_radius=0.30,
        stroke_color=COLORS["grid"],
        stroke_width=1.2,
        stroke_opacity=0.58,
        fill_color=COLORS["panel"],
        fill_opacity=0.86,
    )
    contents.move_to(panel)
    return VGroup(panel, contents)


def math_label(latex, font_size=32, color=COLORS["ink"]):
    """Render professional math with LaTeX's normal math typography."""
    return MathTex(latex, font_size=font_size, color=color)


def keep_on_screen(mob, h_buff=0.34, v_buff=0.24):
    """Shift a finished mobject into the safe area without changing its scale."""
    left = -config.frame_width / 2 + h_buff
    right = config.frame_width / 2 - h_buff
    bottom = -config.frame_height / 2 + v_buff
    top = config.frame_height / 2 - v_buff
    dx = 0.0
    dy = 0.0
    if mob.get_left()[0] < left:
        dx = left - mob.get_left()[0]
    elif mob.get_right()[0] > right:
        dx = right - mob.get_right()[0]
    if mob.get_bottom()[1] < bottom:
        dy = bottom - mob.get_bottom()[1]
    elif mob.get_top()[1] > top:
        dy = top - mob.get_top()[1]
    mob.shift(np.array([dx, dy, 0.0]))
    return mob


def river_stage(center_y=-0.25, water_height=4.25):
    """Return the river, its flow marks, and the two water-edge y values."""
    low = center_y - water_height / 2
    high = center_y + water_height / 2
    water = Rectangle(
        width=14.3,
        height=water_height,
        stroke_width=0,
        fill_color=COLORS["water"],
        fill_opacity=1,
    ).move_to(UP * center_y)
    water_glow = Rectangle(
        width=14.3,
        height=water_height * 0.32,
        stroke_width=0,
        fill_color=COLORS["water_light"],
        fill_opacity=0.12,
    ).move_to(UP * (center_y + 0.2))
    lower_bank = Rectangle(
        width=14.3,
        height=0.78,
        stroke_width=0,
        fill_color=COLORS["bank"],
        fill_opacity=0.94,
    ).move_to(UP * (low - 0.39))
    upper_bank = lower_bank.copy().move_to(UP * (high + 0.39))
    lower_edge = Line(
        LEFT * 7.15 + UP * low,
        RIGHT * 7.15 + UP * low,
        color=COLORS["bank_edge"],
        stroke_width=3.5,
    ).set_opacity(0.88)
    upper_edge = lower_edge.copy().shift(UP * (high - low))

    flow_marks = VGroup()
    for y in np.linspace(low + 0.55, high - 0.55, 3):
        for x in (-5.1, -1.7, 1.7, 5.1):
            flow_marks.add(
                Arrow(
                    np.array([x + 0.45, y, 0.0]),
                    np.array([x - 0.45, y, 0.0]),
                    buff=0,
                    color=COLORS["current"],
                    stroke_width=2.2,
                    max_tip_length_to_length_ratio=0.22,
                ).set_opacity(0.28)
            )
    return VGroup(water, water_glow, flow_marks, lower_bank, upper_bank, lower_edge, upper_edge), low, high


def vector_arrow(start, end, color, stroke_width=7, tip_ratio=0.16):
    return Arrow(
        start,
        end,
        buff=0,
        color=color,
        stroke_width=stroke_width,
        max_tip_length_to_length_ratio=tip_ratio,
    )


def angle_mark(center, vector_angle, symbol, color, bank_angle=0.0):
    """Mark the acute angle between an upstream heading and the bank."""
    radius = 0.58
    delta = vector_angle - bank_angle
    while delta < -PI:
        delta += TAU
    while delta > PI:
        delta -= TAU
    arc = Arc(
        radius=radius,
        start_angle=bank_angle,
        angle=delta,
        arc_center=center,
        color=color,
        stroke_width=3,
    )
    mid = bank_angle + 0.5 * delta
    label = math_label(symbol, font_size=32, color=color)
    label.move_to(center + 0.86 * np.array([np.cos(mid), np.sin(mid), 0]))
    return VGroup(arc, label)


class RiverCrossingF5(Scene):
    """One continuous, silent scene aligned to the corrected narration."""

    def construct(self):
        self.pace = PACE
        self.opening_problem()       # 0:00-0:18
        self.pause_and_think()       # 0:18-0:48
        self.case_a_vectors()        # 0:48-1:24
        self.case_a_result()         # 1:24-1:50
        self.case_b_vectors()        # 1:50-2:25
        self.case_b_result()         # 2:25-2:48
        self.summary()               # 2:48-3:08

    def playp(self, *animations, run_time=1.0, **kwargs):
        self.play(*animations, run_time=run_time * self.pace, **kwargs)

    def hold_to(self, timestamp):
        """Pad a chapter so its endpoint stays aligned with the voiceover."""
        remaining = timestamp * self.pace - self.renderer.time
        if remaining > 0:
            self.wait(remaining)

    def clear_scene(self, run_time=0.7):
        if self.mobjects:
            self.playp(
                *[FadeOut(mob, shift=DOWN * 0.04) for mob in list(self.mobjects)],
                run_time=run_time,
            )

    def sweep_velocity_circle(self, origin, center, radius, target_angle, widget_pos):
        """Move the resultant tip around the reachable-velocity circle.

        The carmine arrow is the net velocity, the mint arrow is the boat's
        velocity through the water, and the small boat inset makes the change
        in heading explicit while the tip travels along the circle.
        """
        tracker = ValueTracker(-PI / 2)

        def point_on_circle():
            theta = tracker.get_value()
            return center + radius * np.array([np.cos(theta), np.sin(theta), 0])

        moving_result = always_redraw(
            lambda: vector_arrow(
                origin,
                point_on_circle(),
                COLORS["result"],
                stroke_width=6,
            )
        )
        moving_boat = always_redraw(
            lambda: vector_arrow(
                center,
                point_on_circle(),
                COLORS["boat"],
                stroke_width=6,
            )
        )
        moving_tip = always_redraw(
            lambda: Dot(point_on_circle(), radius=0.10, color=COLORS["accent"])
        )
        heading_boat = always_redraw(
            lambda: orient_boat(
                make_boat(scale=0.58),
                point_on_circle() - center,
            ).move_to(widget_pos)
        )
        inset_top = Line(
            widget_pos + LEFT * 0.95 + UP * 0.38,
            widget_pos + RIGHT * 0.95 + UP * 0.38,
            color=COLORS["bank_edge"],
            stroke_width=2.4,
        ).set_opacity(0.72)
        inset_bottom = Line(
            widget_pos + LEFT * 0.95 + DOWN * 0.38,
            widget_pos + RIGHT * 0.95 + DOWN * 0.38,
            color=COLORS["bank_edge"],
            stroke_width=2.4,
        ).set_opacity(0.72)
        inset_current = Line(
            widget_pos + RIGHT * 0.65,
            widget_pos + LEFT * 0.65,
            color=COLORS["current"],
            stroke_width=2,
        ).set_opacity(0.34)
        heading_caption = Text(
            "heading changes",
            font=FONT,
            font_size=19,
            color=COLORS["muted"],
        ).move_to(widget_pos + DOWN * 0.82)

        sweep_group = VGroup(
            moving_result,
            moving_boat,
            moving_tip,
            inset_top,
            inset_bottom,
            inset_current,
            heading_boat,
            heading_caption,
        )
        self.add(sweep_group)
        self.playp(FadeIn(sweep_group), run_time=0.7)
        self.playp(
            tracker.animate.set_value(target_angle + TAU),
            run_time=5.0,
            rate_func=linear,
        )
        self.playp(FadeOut(sweep_group), run_time=0.7)
        self.remove(sweep_group)

    def header(self, title):
        title_mob = Text(title, font=FONT, font_size=40, color=COLORS["ink"])
        title_mob.to_edge(UP, buff=0.26)
        underline_width = min(max(2.4, title_mob.width + 0.35), config.frame_width - 0.80)
        line = Line(
            LEFT * (underline_width / 2),
            RIGHT * (underline_width / 2),
            color=COLORS["accent"],
            stroke_width=4,
        )
        line.next_to(title_mob, DOWN, buff=0.12)
        return VGroup(title_mob, line)

    def opening_problem(self):
        self.next_section("Problem", skip_animations=False)
        title = Text(
            "The shortest way across a river",
            font=FONT,
            font_size=48,
            color=COLORS["ink"],
        ).to_edge(UP, buff=0.34)
        title_underline_width = min(title.width + 0.45, config.frame_width - 0.80)
        title_underline = Line(
            LEFT * (title_underline_width / 2),
            RIGHT * (title_underline_width / 2),
            color=COLORS["accent"],
            stroke_width=4,
        ).next_to(title, DOWN, buff=0.12)
        prompt_lines = VGroup(
            Text("A boat moves at 3 m/s in still water.", font=FONT, font_size=23, color=COLORS["ink"]),
            Text("A uniform current flows along the river.", font=FONT, font_size=23, color=COLORS["ink"]),
            Text("Which heading crosses from bank to bank by the shortest path?", font=FONT, font_size=22, color=COLORS["ink"]),
            VGroup(
                Text("a) current = 2 m/s", font=FONT, font_size=22, color=COLORS["accent"]),
                Text("b) current = 4 m/s", font=FONT, font_size=22, color=COLORS["warning"]),
            ).arrange(RIGHT, buff=0.72),
            Text("Source: 333 furfangos feladat  •  Problem 5", font=FONT, font_size=18, color=COLORS["muted"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        prompt_panel = RoundedRectangle(
            width=min(prompt_lines.width + 0.86, config.frame_width - 0.90),
            height=prompt_lines.height + 0.72,
            corner_radius=0.28,
            stroke_color=COLORS["accent"],
            stroke_width=1.4,
            stroke_opacity=0.62,
            fill_color=COLORS["panel"],
            fill_opacity=0.90,
        )
        prompt_lines.move_to(prompt_panel)
        prompt_card = VGroup(prompt_panel, prompt_lines).move_to(np.array([0, 1.10, 0]))
        keep_on_screen(prompt_card)

        river, low, high = river_stage(center_y=-1.28, water_height=2.55)
        boat = make_boat(scale=0.78).move_to(np.array([-3.2, low + 0.42, 0]))
        across_arrow = vector_arrow(
            boat.get_center() + UP * 0.45,
            boat.get_center() + UP * 1.55,
            COLORS["boat"],
            stroke_width=5,
        )
        across_label = math_label(r"v = 3\,\mathrm{m/s}", font_size=29, color=COLORS["boat"])
        across_label.next_to(across_arrow, LEFT, buff=0.22)

        current_label = pill("uniform current", COLORS["current"], width=2.55, font_size=22)
        current_label.move_to(np.array([3.65, 0.28, 0]))
        cases = VGroup(
            pill("a)  2 m/s", COLORS["accent"], width=2.20),
            pill("b)  4 m/s", COLORS["warning"], width=2.20),
        ).arrange(DOWN, buff=0.18).next_to(current_label, DOWN, buff=0.20)
        keep_on_screen(VGroup(current_label, cases))

        question = Text(
            "Which heading gives the shortest path?",
            font=FONT,
            font_size=30,
            color=COLORS["ink"],
        ).move_to(np.array([0, -3.45, 0]))

        self.playp(FadeIn(title, shift=UP * 0.15), Create(title_underline), run_time=1.5)
        self.playp(FadeIn(prompt_card, shift=UP * 0.10), run_time=2.0)
        self.wait(2.0 * self.pace)
        self.playp(FadeOut(prompt_card), run_time=0.8)
        self.playp(FadeIn(river), run_time=1.2)
        self.playp(FadeIn(boat), GrowArrow(across_arrow), FadeIn(across_label), run_time=1.4)
        self.playp(FadeIn(current_label), LaggedStart(*[FadeIn(c) for c in cases], lag_ratio=0.22), run_time=1.4)
        self.playp(Write(question), run_time=1.1)
        self.hold_to(18)

    def pause_and_think(self):
        self.next_section("Pause and think", skip_animations=False)
        self.clear_scene()
        header = self.header("First: current = 2 m/s")
        river, low, high = river_stage(center_y=-0.35, water_height=3.65)
        start = np.array([-3.25, low, 0])
        boat = make_boat(scale=0.72).move_to(start)

        heading = vector_arrow(start, start + UP * 1.45, COLORS["boat"], stroke_width=6)
        heading_label = math_label(r"\mathbf{v}", font_size=31, color=COLORS["boat"])
        heading_label.next_to(heading, LEFT, buff=0.10)
        current = vector_arrow(start, start + LEFT * 1.05, COLORS["current"], stroke_width=6)
        current_label = math_label(r"\mathbf{u}", font_size=31, color=COLORS["current"])
        current_label.next_to(current, DOWN, buff=0.10)

        water_height = high - low
        diagonal_end = start + np.array([-water_height * 2 / 3, water_height, 0])
        actual_path = DashedLine(start, diagonal_end, dash_length=0.15, color=COLORS["result_light"], stroke_width=5)
        shortest_path = DashedLine(
            start,
            np.array([start[0], high, 0]),
            dash_length=0.15,
            color=COLORS["accent"],
            stroke_width=4,
        ).set_opacity(0.70)

        fastest = pill("fastest crossing", COLORS["boat"], width=2.55, font_size=22)
        fastest.move_to(np.array([3.9, -0.15, 0]))
        not_shortest = pill("but not shortest", COLORS["result_light"], width=2.65, font_size=22)
        not_shortest.next_to(fastest, DOWN, buff=0.18)
        distinction = VGroup(
            Text("boat heading", font=FONT, font_size=29, color=COLORS["ink"]),
            math_label(r"\mathbf{v} \ne \mathbf{w}", font_size=29, color=COLORS["ink"]),
            Text("actual path", font=FONT, font_size=29, color=COLORS["ink"]),
        ).arrange(RIGHT, buff=0.18).to_edge(DOWN, buff=0.24)
        pause_card = pill("Pause and predict the best heading", COLORS["accent"], width=4.55, font_size=23)
        pause_card.move_to(np.array([0, -0.25, 0]))
        bad_choices = VGroup(
            pill("downstream  →  extra drift", COLORS["warning"], width=3.55, font_size=20),
            pill("directly upstream  →  no crossing", COLORS["muted"], width=4.15, font_size=20),
        ).arrange(DOWN, buff=0.16).move_to(np.array([3.75, -0.20, 0]))
        keep_on_screen(VGroup(fastest, not_shortest))
        keep_on_screen(bad_choices)

        self.playp(FadeIn(header), FadeIn(river), run_time=1.3)
        self.playp(FadeIn(pause_card, scale=0.96), run_time=0.8)
        self.wait(2.0 * self.pace)
        self.playp(FadeOut(pause_card), FadeIn(bad_choices), run_time=0.8)
        self.wait(1.4 * self.pace)
        self.playp(FadeOut(bad_choices), run_time=0.6)
        self.playp(FadeIn(boat), GrowArrow(heading), FadeIn(heading_label), run_time=1.3)
        self.playp(GrowArrow(current), FadeIn(current_label), run_time=1.1)
        self.playp(Create(actual_path), run_time=2.2)
        moved_boat = boat.copy().move_to(diagonal_end)
        self.playp(Transform(boat, moved_boat), run_time=2.5, rate_func=linear)
        self.playp(FadeIn(fastest), FadeIn(not_shortest), run_time=1.1)
        self.playp(Create(shortest_path), Write(distinction), run_time=1.5)
        self.hold_to(48)

    def case_a_vectors(self):
        self.next_section("Part a vector construction", skip_animations=False)
        self.clear_scene()
        header = self.header("Part (a): build the velocity diagram")
        self.playp(FadeIn(header), run_time=1.0)

        scale = 0.85
        origin = np.array([-0.80, -0.28, 0])
        center = origin + LEFT * (2 * scale)
        radius = 3 * scale
        current = vector_arrow(origin, center, COLORS["current"], stroke_width=7)
        current_label = math_label(r"\mathbf{u}", font_size=31, color=COLORS["current"])
        current_label.next_to(current, DOWN, buff=0.12)
        origin_dot = Dot(origin, radius=0.07, color=COLORS["ink"])
        center_dot = Dot(center, radius=0.07, color=COLORS["current"])

        equation = VGroup(
            math_label(r"\mathbf{w}", font_size=37, color=COLORS["result"]),
            math_label("=", font_size=37, color=COLORS["ink"]),
            math_label(r"\mathbf{u}", font_size=37, color=COLORS["current"]),
            math_label("+", font_size=37, color=COLORS["ink"]),
            math_label(r"\mathbf{v}", font_size=37, color=COLORS["boat"]),
        ).arrange(RIGHT, buff=0.15)
        equation.move_to(np.array([4.55, 1.75, 0]))
        legend = VGroup(
            VGroup(
                math_label(r"\mathbf{u}", font_size=24, color=COLORS["current"]),
                Text("river current", font=FONT, font_size=21, color=COLORS["current"]),
            ).arrange(RIGHT, buff=0.22),
            VGroup(
                math_label(r"\mathbf{v}", font_size=24, color=COLORS["boat"]),
                Text("boat through water", font=FONT, font_size=21, color=COLORS["boat"]),
            ).arrange(RIGHT, buff=0.22),
            VGroup(
                math_label(r"\mathbf{w}", font_size=24, color=COLORS["result_light"]),
                Text("actual velocity", font=FONT, font_size=21, color=COLORS["result_light"]),
            ).arrange(RIGHT, buff=0.22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(equation, DOWN, buff=0.34)
        keep_on_screen(VGroup(equation, legend))

        self.playp(FadeIn(origin_dot), GrowArrow(current), FadeIn(current_label), run_time=1.4)
        self.playp(FadeIn(center_dot), Write(equation), FadeIn(legend), run_time=1.5)

        demo_endpoint = center + UP * radius
        demo_boat_vector = vector_arrow(center, demo_endpoint, COLORS["boat"], stroke_width=5)
        demo_result_vector = vector_arrow(origin, demo_endpoint, COLORS["result"], stroke_width=5)
        self.playp(GrowArrow(demo_boat_vector), GrowArrow(demo_result_vector), run_time=1.0)
        self.playp(FadeOut(VGroup(demo_boat_vector, demo_result_vector)), run_time=0.5)

        circle = Circle(radius=radius, color=COLORS["boat"], stroke_width=3.5).move_to(center)
        circle_label = VGroup(
            Text("all endpoints with", font=FONT, font_size=22, color=COLORS["boat"]),
            math_label(r"v = 3\,\mathrm{m/s}", font_size=22, color=COLORS["boat"]),
        ).arrange(RIGHT, buff=0.16).move_to(np.array([-1.6, -3.20, 0]))

        sample_boat_arrows = VGroup()
        sample_result_lines = VGroup()
        for theta in np.linspace(0, TAU, 12, endpoint=False):
            endpoint = center + radius * np.array([np.cos(theta), np.sin(theta), 0])
            sample_boat_arrows.add(
                vector_arrow(center, endpoint, COLORS["boat"], stroke_width=3.0, tip_ratio=0.10).set_opacity(0.28)
            )
            sample_result_lines.add(
                Line(origin, endpoint, color=COLORS["result"], stroke_width=1.8).set_opacity(0.16)
            )

        self.playp(Create(circle), FadeIn(circle_label), run_time=1.5)
        self.playp(LaggedStart(*[GrowArrow(a) for a in sample_boat_arrows], lag_ratio=0.07), run_time=2.8)
        self.playp(LaggedStart(*[Create(line) for line in sample_result_lines], lag_ratio=0.05), run_time=2.0)

        target_angle = np.arctan2(np.sqrt(5), 2)
        self.sweep_velocity_circle(
            origin,
            center,
            radius,
            target_angle,
            np.array([3.3, -1.55, 0]),
        )

        target_line = DashedLine(
            origin + DOWN * 2.65,
            origin + UP * 2.65,
            dash_length=0.13,
            color=COLORS["accent"],
            stroke_width=4,
        )
        target_label = VGroup(
            Text("shortest path", font=FONT, font_size=21, color=COLORS["accent"]),
            Text("direction", font=FONT, font_size=21, color=COLORS["accent"]),
        ).arrange(DOWN, buff=0.04).move_to(np.array([1.30, -2.55, 0]))
        self.playp(
            FadeOut(VGroup(sample_boat_arrows, sample_result_lines)),
            Create(target_line),
            FadeIn(target_label),
            run_time=1.5,
        )

        tangent_y = np.sqrt(3**2 - 2**2) * scale
        endpoint = origin + UP * tangent_y
        endpoint_dot = Dot(endpoint, radius=0.11, color=COLORS["accent"])
        boat_vector = vector_arrow(center, endpoint, COLORS["boat"], stroke_width=7)
        boat_label = math_label(r"\mathbf{v}", font_size=32, color=COLORS["boat"])
        boat_label.next_to(boat_vector.get_center(), LEFT, buff=0.14)

        self.playp(FadeIn(endpoint_dot, scale=1.8), run_time=0.7)
        self.playp(GrowArrow(boat_vector), FadeIn(boat_label), run_time=1.5)

        theta = np.arctan2(endpoint[1] - center[1], endpoint[0] - center[0])
        alpha = angle_mark(center, theta, r"\alpha", COLORS["accent"])
        upstream = DashedLine(center, center + RIGHT * 1.05, color=COLORS["muted"], stroke_width=2)
        formula = formula_panel(
            math_label(r"v\cos\alpha = u", font_size=27, color=COLORS["ink"]),
            math_label(r"3\cos\alpha = 2", font_size=30, color=COLORS["ink"]),
            math_label(r"\cos\alpha = \frac{2}{3}", font_size=30, color=COLORS["ink"]),
            math_label(r"\alpha = \arccos\!\left(\frac{2}{3}\right)", font_size=27, color=COLORS["ink"]),
            math_label(r"\alpha \approx 48.2^\circ", font_size=34, color=COLORS["accent"]),
            width=4.10,
        ).move_to(np.array([4.65, -1.65, 0]))
        keep_on_screen(formula)
        self.playp(Create(upstream), Create(alpha), run_time=1.0)
        self.playp(FadeIn(formula[0], shift=UP * 0.12), run_time=0.4)
        for row in formula[1]:
            self.playp(Write(row), run_time=0.42)
        self.hold_to(84)

    def case_a_result(self):
        self.next_section("Part a physical result", skip_animations=False)
        self.clear_scene()
        header = self.header("Part (a): cancel the drift")
        river, low, high = river_stage(center_y=-0.35, water_height=3.70)
        start = np.array([-2.55, low, 0])
        end = np.array([start[0], high, 0])
        heading_vector = np.array([2.0, np.sqrt(5), 0])
        boat = orient_boat(make_boat(scale=0.78), heading_vector).move_to(start)
        route = DashedLine(start, end, dash_length=0.14, color=COLORS["result_light"], stroke_width=5)
        overlay_scale = 0.28
        heading = vector_arrow(start, start + overlay_scale * heading_vector, COLORS["boat"], stroke_width=6)
        current = vector_arrow(start, start + overlay_scale * np.array([-2.0, 0.0, 0.0]), COLORS["current"], stroke_width=6)
        net = vector_arrow(start, start + overlay_scale * np.array([0.0, np.sqrt(5), 0.0]), COLORS["result"], stroke_width=6)

        answer = formula_panel(
            Text("Heading", font=FONT, font_size=22, color=COLORS["muted"]),
            VGroup(
                math_label(r"\alpha = 48.2^\circ", font_size=27, color=COLORS["accent"]),
                Text("to the bank, upstream", font=FONT, font_size=22, color=COLORS["accent"]),
            ).arrange(RIGHT, buff=0.16),
            math_label(r"w \approx 2.24\,\mathrm{m/s}", font_size=25, color=COLORS["ink"]),
            width=5.35,
        ).move_to(np.array([3.85, -0.20, 0]))
        keep_on_screen(answer)
        shortest = pill("absolute shortest path", COLORS["accent"], width=3.35, font_size=22)
        shortest.next_to(answer, DOWN, buff=0.28)
        keep_on_screen(shortest)

        self.playp(FadeIn(header), FadeIn(river), run_time=1.2)
        self.playp(FadeIn(boat), GrowArrow(heading), GrowArrow(current), run_time=1.4)
        self.playp(GrowArrow(net), Create(route), run_time=1.4)
        self.playp(FadeOut(VGroup(heading, current, net)), run_time=0.6)
        self.playp(MoveAlongPath(boat, Line(start, end)), run_time=4.0, rate_func=linear)
        self.playp(FadeIn(answer, shift=LEFT * 0.12), FadeIn(shortest), run_time=1.3)
        self.hold_to(110)

    def case_b_vectors(self):
        self.next_section("Part b tangent construction", skip_animations=False)
        self.clear_scene()
        header = self.header("Part (b): current = 4 m/s")
        self.playp(FadeIn(header), run_time=1.0)

        scale = 0.85
        origin = np.array([-0.80, -0.28, 0])
        center = origin + LEFT * (4 * scale)
        radius = 3 * scale
        current = vector_arrow(origin, center, COLORS["current"], stroke_width=7)
        current_label = math_label(r"u = 4\,\mathrm{m/s}", font_size=30, color=COLORS["current"])
        current_label.next_to(current, DOWN, buff=0.13)
        circle = Circle(radius=radius, color=COLORS["boat"], stroke_width=3.5).move_to(center)
        circle_label = math_label(r"v = 3\,\mathrm{m/s}", font_size=30, color=COLORS["boat"])
        circle_label.move_to(center + DOWN * 2.12)
        origin_dot = Dot(origin, radius=0.08, color=COLORS["ink"])

        self.playp(FadeIn(origin_dot), GrowArrow(current), FadeIn(current_label), run_time=1.4)
        self.playp(Create(circle), FadeIn(circle_label), run_time=1.5)

        target_line = DashedLine(
            origin + DOWN * 2.65,
            origin + UP * 2.65,
            dash_length=0.13,
            color=COLORS["accent"],
            stroke_width=4,
        )
        miss = VGroup(
            Text("no intersection", font=FONT, font_size=25, color=COLORS["warning"]),
            Text("straight across is impossible", font=FONT, font_size=22, color=COLORS["muted"]),
        ).arrange(DOWN, buff=0.10).move_to(np.array([3.05, 1.35, 0]))
        keep_on_screen(miss)
        self.playp(Create(target_line), run_time=1.2)
        self.playp(FadeIn(miss, shift=RIGHT * 0.12), Wiggle(target_line, scale_value=1.02), run_time=1.5)

        sample_lines = VGroup()
        for theta in np.linspace(-0.72, 0.72, 9):
            endpoint = center + radius * np.array([np.cos(theta), np.sin(theta), 0])
            sample_lines.add(Line(origin, endpoint, color=COLORS["result"], stroke_width=2).set_opacity(0.17))
        self.playp(LaggedStart(*[Create(line) for line in sample_lines], lag_ratio=0.07), run_time=2.0)

        # Tangency coordinates for a circle of radius v centered u units away.
        tangent_unscaled = np.array([-(4**2 - 3**2) / 4, 3 * np.sqrt(4**2 - 3**2) / 4, 0])
        tangent = origin + scale * tangent_unscaled
        boat_vector = vector_arrow(center, tangent, COLORS["boat"], stroke_width=7)
        result_vector = vector_arrow(origin, tangent, COLORS["result"], stroke_width=7)
        tangent_dot = Dot(tangent, radius=0.11, color=COLORS["accent"])
        tangent_note = pill(
            "path closest to straight across",
            COLORS["accent"],
            width=4.65,
            font_size=18,
        ).move_to(np.array([3.55, -1.55, 0]))
        keep_on_screen(tangent_note)

        self.playp(
            FadeOut(miss),
            target_line.animate.set_opacity(0.24),
            sample_lines.animate.set_opacity(0.07),
            run_time=0.8,
        )
        target_angle = np.arctan2(3 * np.sqrt(7) / 4, 9 / 4)
        self.sweep_velocity_circle(
            origin,
            center,
            radius,
            target_angle,
            np.array([3.3, -1.55, 0]),
        )
        self.playp(GrowArrow(result_vector), FadeIn(tangent_dot), run_time=1.6)
        self.playp(GrowArrow(boat_vector), FadeIn(tangent_note), run_time=1.4)

        right_angle = RightAngle(
            Line(tangent, origin),
            Line(tangent, center),
            length=0.26,
            quadrant=(1, -1),
            color=COLORS["accent"],
            stroke_width=3,
        )
        self.playp(Create(right_angle), run_time=0.9)

        theta = np.arctan2(tangent[1] - center[1], tangent[0] - center[0])
        beta = angle_mark(center, theta, r"\beta", COLORS["accent"])
        path_theta = np.arctan2(tangent[1] - origin[1], tangent[0] - origin[0])
        path_angle = angle_mark(origin, path_theta, r"\phi", COLORS["result_light"], bank_angle=PI)
        upstream = DashedLine(center, center + RIGHT * 1.05, color=COLORS["muted"], stroke_width=2)
        formula = formula_panel(
            math_label(r"\cos\beta = \frac{3}{4}", font_size=32, color=COLORS["ink"]),
            math_label(r"\beta \approx 41.4^\circ", font_size=35, color=COLORS["accent"]),
            width=3.45,
        ).move_to(np.array([4.95, 1.25, 0]))
        keep_on_screen(formula)
        triangle_note = math_label(
            r"\mathbf{v} \perp \mathbf{w}",
            font_size=30,
            color=COLORS["ink"],
        ).move_to(np.array([4.55, -0.38, 0]))
        keep_on_screen(triangle_note)
        path_note = VGroup(
            math_label(r"\phi", font_size=22, color=COLORS["result_light"]),
            Text("path angle", font=FONT, font_size=19, color=COLORS["result_light"]),
        ).arrange(RIGHT, buff=0.14).move_to(np.array([4.55, -0.88, 0]))
        keep_on_screen(path_note)

        self.playp(Create(upstream), Create(beta), Create(path_angle), run_time=1.0)
        self.playp(FadeIn(formula, shift=UP * 0.10), FadeIn(triangle_note), FadeIn(path_note), run_time=1.4)
        self.hold_to(145)

    def case_b_result(self):
        self.next_section("Part b physical result", skip_animations=False)
        self.clear_scene()
        header = self.header("Part (b): the best feasible path")
        river, low, high = river_stage(center_y=-0.35, water_height=3.70)
        start = np.array([-2.25, low, 0])
        water_height = high - start[1]
        tangent_resultant = np.array([-7 / 4, 3 * np.sqrt(7) / 4, 0])
        tangent_heading_vector = np.array([9 / 4, 3 * np.sqrt(7) / 4, 0])
        tangent_end = start + tangent_resultant * (water_height / tangent_resultant[1])

        # Compare a nearby heading with the tangent heading at the river itself.
        # The nearby choice produces a visibly more diagonal path; the tangent
        # is the reachable path closest to the straight-across reference.
        tangent_heading_angle = np.arctan2(tangent_heading_vector[1], tangent_heading_vector[0])
        nearby_heading_angle = tangent_heading_angle + 0.32
        nearby_heading_vector = 3 * np.array(
            [np.cos(nearby_heading_angle), np.sin(nearby_heading_angle), 0]
        )
        nearby_resultant = np.array([-4.0, 0.0, 0.0]) + nearby_heading_vector
        nearby_end = start + nearby_resultant * (water_height / nearby_resultant[1])

        other_heading_angle = tangent_heading_angle - 0.30
        other_heading_vector = 3 * np.array(
            [np.cos(other_heading_angle), np.sin(other_heading_angle), 0]
        )
        other_resultant = np.array([-4.0, 0.0, 0.0]) + other_heading_vector
        other_end = start + other_resultant * (water_height / other_resultant[1])

        boat = orient_boat(
            make_boat(color=COLORS["warning"], scale=0.78),
            nearby_heading_vector,
        ).move_to(start)
        tangent_boat = orient_boat(make_boat(scale=0.78), tangent_heading_vector).move_to(start)
        other_boat = orient_boat(
            make_boat(color=COLORS["muted"], scale=0.78),
            other_heading_vector,
        ).move_to(start)
        nearby_route = DashedLine(
            start,
            nearby_end,
            dash_length=0.14,
            color=COLORS["warning"],
            stroke_width=4,
        ).set_opacity(0.82)
        tangent_route = DashedLine(
            start,
            tangent_end,
            dash_length=0.14,
            color=COLORS["result_light"],
            stroke_width=5,
        )
        other_route = DashedLine(
            start,
            other_end,
            dash_length=0.14,
            color=COLORS["muted"],
            stroke_width=4,
        ).set_opacity(0.55)
        vertical_reference = DashedLine(
            start,
            np.array([start[0], high, 0]),
            dash_length=0.12,
            color=COLORS["muted"],
            stroke_width=2,
        ).set_opacity(0.45)

        overlay_scale = 0.28
        nearby_heading = vector_arrow(
            start,
            start + overlay_scale * nearby_heading_vector,
            COLORS["warning"],
            stroke_width=6,
        )
        tangent_heading = vector_arrow(
            start,
            start + overlay_scale * tangent_heading_vector,
            COLORS["boat"],
            stroke_width=6,
        )
        other_heading = vector_arrow(
            start,
            start + overlay_scale * other_heading_vector,
            COLORS["muted"],
            stroke_width=6,
        )
        current = vector_arrow(start, start + overlay_scale * np.array([-4.0, 0.0, 0.0]), COLORS["current"], stroke_width=6)

        # A compact copy of the velocity circle stays on screen while the
        # candidate paths are drawn in the river below it.
        inset_center = np.array([4.55, 2.05, 0])
        inset_origin = inset_center + RIGHT * 0.72
        inset_radius = 0.52
        circle_tracker = ValueTracker(nearby_heading_angle)

        def inset_tip():
            theta = circle_tracker.get_value()
            return inset_center + inset_radius * np.array([np.cos(theta), np.sin(theta), 0])

        inset_circle = Circle(radius=inset_radius, color=COLORS["boat"], stroke_width=2.2).move_to(inset_center)
        inset_current = vector_arrow(inset_origin, inset_center, COLORS["current"], stroke_width=3, tip_ratio=0.24)
        inset_origin_dot = Dot(inset_origin, radius=0.045, color=COLORS["ink"])
        inset_boat_vector = always_redraw(
            lambda: vector_arrow(inset_center, inset_tip(), COLORS["boat"], stroke_width=3, tip_ratio=0.24)
        )
        inset_result_vector = always_redraw(
            lambda: vector_arrow(inset_origin, inset_tip(), COLORS["result"], stroke_width=3, tip_ratio=0.24)
        )
        inset_tip_dot = always_redraw(lambda: Dot(inset_tip(), radius=0.06, color=COLORS["accent"]))
        inset_label = math_label(r"v = 3\,\mathrm{m/s}", font_size=18, color=COLORS["boat"])
        inset_label.move_to(inset_center + UP * 0.76)
        inset_group = VGroup(
            inset_circle,
            inset_current,
            inset_origin_dot,
            inset_boat_vector,
            inset_result_vector,
            inset_tip_dot,
            inset_label,
        )

        width_marker = BraceBetweenPoints(
            start,
            np.array([start[0], high, 0]),
            direction=LEFT,
            color=COLORS["muted"],
        )
        width_label = VGroup(
            Text("river width", font=FONT, font_size=17, color=COLORS["muted"]),
            math_label(r"W", font_size=19, color=COLORS["muted"]),
        ).arrange(RIGHT, buff=0.10)
        width_label.next_to(width_marker, LEFT, buff=0.10)
        straight_note = Text("straight across", font=FONT, font_size=18, color=COLORS["muted"])
        straight_note.move_to(np.array([-0.95, high - 0.28, 0]))
        tangent_note = Text(
            "tangent = closest feasible path",
            font=FONT,
            font_size=20,
            color=COLORS["accent"],
        ).move_to(np.array([4.45, -1.20, 0]))
        keep_on_screen(VGroup(straight_note, tangent_note))

        answer = formula_panel(
            Text("Heading", font=FONT, font_size=22, color=COLORS["muted"]),
            VGroup(
                math_label(r"\beta = 41.4^\circ", font_size=27, color=COLORS["accent"]),
                Text("to the bank, upstream", font=FONT, font_size=22, color=COLORS["accent"]),
            ).arrange(RIGHT, buff=0.16),
            math_label(r"w \approx 2.65\,\mathrm{m/s}", font_size=25, color=COLORS["ink"]),
            math_label(r"\text{path length} = \frac{4}{3}\times\text{river width}", font_size=20, color=COLORS["result_light"]),
            width=5.40,
        ).move_to(np.array([3.80, -0.05, 0]))
        keep_on_screen(answer)

        self.playp(FadeIn(header), FadeIn(river), run_time=1.2)
        self.playp(
            FadeIn(boat),
            GrowArrow(nearby_heading),
            GrowArrow(current),
            Create(vertical_reference),
            Create(nearby_route),
            Create(width_marker),
            FadeIn(width_label),
            FadeIn(straight_note),
            FadeIn(inset_group),
            run_time=1.7,
        )
        self.playp(
            circle_tracker.animate.set_value(nearby_heading_angle + TAU),
            run_time=2.6,
            rate_func=linear,
        )
        self.playp(
            circle_tracker.animate.set_value(other_heading_angle),
            Transform(boat, other_boat),
            Transform(nearby_heading, other_heading),
            Create(other_route),
            run_time=1.4,
            rate_func=linear,
        )
        self.playp(
            circle_tracker.animate.set_value(tangent_heading_angle),
            Transform(boat, tangent_boat),
            Transform(nearby_heading, tangent_heading),
            Create(tangent_route),
            FadeIn(tangent_note),
            run_time=1.4,
            rate_func=linear,
        )
        self.playp(FadeOut(inset_group), run_time=0.7)
        self.playp(MoveAlongPath(boat, Line(start, tangent_end)), run_time=4.2, rate_func=linear)
        self.playp(
            FadeOut(VGroup(boat, nearby_heading, current, tangent_note, straight_note)),
            FadeIn(answer, shift=LEFT * 0.12),
            run_time=1.3,
        )
        self.hold_to(168)

    def summary(self):
        self.next_section("Summary", skip_animations=False)
        self.clear_scene()
        header = self.header("Same idea, two different geometries")

        def mini_card(card_center, title_text, title_color, current_vector, boat_vector, path_text, path_color):
            """Build a compact recap from the exact solved velocity vectors."""
            vector_scale = 0.25
            path_scale = 0.55
            current_vector = np.array(current_vector, dtype=float)
            boat_vector = np.array(boat_vector, dtype=float)
            resultant_vector = current_vector + boat_vector

            title = Text(title_text, font=FONT, font_size=22, color=title_color)
            title.move_to(card_center + UP * 1.28)

            vector_caption = Text("vector addition", font=FONT, font_size=18, color=COLORS["muted"])
            vector_caption.move_to(card_center + LEFT * 1.14 + UP * 0.94)
            path_caption = Text("boat movement", font=FONT, font_size=18, color=COLORS["muted"])
            path_caption.move_to(card_center + RIGHT * 1.34 + UP * 0.94)
            equation = math_label(r"\mathbf{w} = \mathbf{u} + \mathbf{v}", font_size=24, color=COLORS["ink"])
            equation.move_to(card_center + LEFT * 1.14 + UP * 0.58)

            vector_origin = card_center + LEFT * 1.05 + DOWN * 0.36
            vector_center = vector_origin + current_vector * vector_scale
            vector_tip = vector_center + boat_vector * vector_scale
            u_arrow = vector_arrow(vector_origin, vector_center, COLORS["current"], stroke_width=4, tip_ratio=0.22)
            v_arrow = vector_arrow(vector_center, vector_tip, COLORS["boat"], stroke_width=4, tip_ratio=0.22)
            w_arrow = vector_arrow(vector_origin, vector_tip, COLORS["result"], stroke_width=4, tip_ratio=0.22)
            u_label = math_label(r"\mathbf{u}", font_size=20, color=COLORS["current"])
            u_label.move_to(vector_origin + current_vector * vector_scale * 0.5 + DOWN * 0.13)
            v_label = math_label(r"\mathbf{v}", font_size=20, color=COLORS["boat"])
            v_label.move_to(vector_center + boat_vector * vector_scale * 0.52 + RIGHT * 0.12)
            w_label = math_label(r"\mathbf{w}", font_size=20, color=COLORS["result_light"])
            w_label.move_to(vector_origin + resultant_vector * vector_scale * 0.52 + LEFT * 0.13)
            vector_dots = VGroup(
                Dot(vector_origin, radius=0.045, color=COLORS["ink"]),
                Dot(vector_center, radius=0.045, color=COLORS["current"]),
                Dot(vector_tip, radius=0.055, color=COLORS["accent"]),
            )

            path_start = card_center + RIGHT * 1.34 + DOWN * 0.64
            path_end = path_start + resultant_vector * path_scale
            river_width = 2.18
            river = Rectangle(
                width=river_width,
                height=path_end[1] - path_start[1],
                stroke_width=0,
                fill_color=COLORS["water"],
                fill_opacity=0.84,
            ).move_to(np.array([path_start[0], (path_start[1] + path_end[1]) / 2, 0]))
            bank_left = path_start[0] - river_width / 2
            bank_right = path_start[0] + river_width / 2
            banks = VGroup(
                Line(np.array([bank_left, path_start[1], 0]), np.array([bank_right, path_start[1], 0]), color=COLORS["bank_edge"], stroke_width=3),
                Line(np.array([bank_left, path_end[1], 0]), np.array([bank_right, path_end[1], 0]), color=COLORS["bank_edge"], stroke_width=3),
            )
            boat_path = DashedLine(path_start, path_end, dash_length=0.08, color=path_color, stroke_width=3)
            mini_boat = orient_boat(make_boat(scale=0.28), boat_vector).move_to(path_start)
            path_label = Text(path_text, font=FONT, font_size=16, color=path_color)
            path_label.move_to(card_center + RIGHT * 1.34 + DOWN * 1.48)

            static = VGroup(title, vector_caption, path_caption, equation, river, banks, boat_path, mini_boat, path_label)
            return {
                "static": static,
                "u": u_arrow,
                "v": v_arrow,
                "w": w_arrow,
                "labels": VGroup(u_label, v_label, w_label),
                "dots": vector_dots,
                "boat": mini_boat,
                "path": Line(path_start, path_end),
            }

        left = mini_card(
            LEFT * 3.05 + DOWN * 0.25,
            "a) river slower than boat",
            COLORS["accent"],
            np.array([-2.0, 0.0, 0]),
            np.array([2.0, np.sqrt(5), 0]),
            "straight across",
            COLORS["accent"],
        )
        right = mini_card(
            RIGHT * 3.05 + DOWN * 0.25,
            "b) river faster than boat",
            COLORS["warning"],
            np.array([-4.0, 0.0, 0]),
            np.array([9 / 4, 3 * np.sqrt(7) / 4, 0]),
            "drifts downstream",
            COLORS["result_light"],
        )

        divider = Line(UP * 1.50, DOWN * 1.55, color=COLORS["muted"], stroke_width=1.2).set_opacity(0.28)

        final_line = math_label(r"\mathbf{u} + \mathbf{v} = \mathbf{w}", font_size=31, color=COLORS["ink"]).move_to(DOWN * 2.65)
        keep_on_screen(final_line)

        self.playp(FadeIn(header), FadeIn(divider), run_time=1.0)
        self.playp(FadeIn(left["static"], shift=RIGHT * 0.15), FadeIn(right["static"], shift=LEFT * 0.15), run_time=1.2)
        self.playp(FadeIn(left["dots"]), FadeIn(right["dots"]), GrowArrow(left["u"]), GrowArrow(right["u"]), run_time=0.8)
        self.playp(
            GrowArrow(left["v"]),
            GrowArrow(right["v"]),
            FadeIn(left["labels"][0]),
            FadeIn(right["labels"][0]),
            FadeIn(left["labels"][1]),
            FadeIn(right["labels"][1]),
            run_time=0.9,
        )
        self.playp(
            GrowArrow(left["w"]),
            GrowArrow(right["w"]),
            FadeIn(left["labels"][2]),
            FadeIn(right["labels"][2]),
            run_time=0.9,
        )
        self.playp(
            MoveAlongPath(left["boat"], left["path"]),
            MoveAlongPath(right["boat"], right["path"]),
            run_time=2.2,
            rate_func=linear,
        )
        self.playp(Write(final_line), run_time=1.3)
        self.hold_to(188)

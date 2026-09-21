"""A short, pedagogical animation of problem F.1 from 333 furfangos feladat.

The animation follows the book's second solution:
1. Among five meetings, one snail (renamed alpha) met all three others.
2. Ride with alpha. The other three trajectories all pass through alpha's
   position.
3. If beta met both gamma and delta, the three straight trajectories must be
   one straight line. Gamma and delta therefore meet eventually as well.

Render with, for example:
    manim -pql snails_solution.py SnailsSolution
"""

from manim import *


config.background_color = "#0B1020"


COLORS = {
    "alpha": "#F6C85F",
    "beta": "#56CCF2",
    "gamma": "#BB6BD9",
    "delta": "#6FCF97",
    "ink": "#F5F7FA",
    "muted": "#AAB5C4",
    "grid": "#334155",
    "accent": "#FF7A59",
}


def snail(color, name, scale=1.0):
    """A deliberately simple snail marker: body, shell, eye, and label."""
    body = RoundedRectangle(
        width=0.52,
        height=0.20,
        corner_radius=0.09,
        stroke_width=0,
        fill_color=color,
        fill_opacity=1,
    )
    shell = Circle(
        radius=0.16,
        stroke_color=COLORS["ink"],
        stroke_width=1.5,
        fill_color=color,
        fill_opacity=1,
    ).shift(LEFT * 0.08 + UP * 0.09)
    shell_ring = Arc(
        radius=0.075,
        start_angle=0,
        angle=1.7 * PI,
        color=COLORS["ink"],
        stroke_width=1.2,
    ).move_to(shell.get_center())
    head = Circle(
        radius=0.105,
        stroke_width=0,
        fill_color=color,
        fill_opacity=1,
    ).shift(RIGHT * 0.28 + UP * 0.01)
    eye = Dot(
        head.get_center() + RIGHT * 0.035 + UP * 0.045,
        radius=0.018,
        color=COLORS["ink"],
    )
    feeler_1 = Line(
        head.get_center() + RIGHT * 0.04 + UP * 0.075,
        head.get_center() + RIGHT * 0.11 + UP * 0.14,
        color=color,
        stroke_width=2,
    )
    feeler_2 = Line(
        head.get_center() + RIGHT * 0.08 + UP * 0.06,
        head.get_center() + RIGHT * 0.17 + UP * 0.10,
        color=color,
        stroke_width=2,
    )
    label = Text(name, font_size=23, color=COLORS["ink"])
    label.next_to(body, DOWN, buff=0.08)
    return VGroup(body, shell, shell_ring, head, eye, feeler_1, feeler_2, label).scale(scale)


def pill(text, color=COLORS["ink"], fill="#16233A", width=2.0):
    box = RoundedRectangle(
        width=width,
        height=0.48,
        corner_radius=0.12,
        stroke_color=color,
        stroke_width=1.5,
        fill_color=fill,
        fill_opacity=1,
    )
    words = Text(text, font_size=22, color=color)
    words.move_to(box.get_center())
    return VGroup(box, words)


class SnailsSolution(Scene):
    def construct(self):
        self.intro()
        self.counting_step()
        self.riding_frame_step()
        self.collinearity_step()
        self.future_meeting_step()
        self.conclusion()

    def intro(self):
        title = Text("The last snail meeting", font_size=44, color=COLORS["ink"])
        subtitle = Text("Problem F.1 — a visual proof", font_size=25, color=COLORS["muted"])
        subtitle.next_to(title, DOWN, buff=0.18)

        snails = VGroup(
            snail(COLORS["alpha"], "α"),
            snail(COLORS["beta"], "β"),
            snail(COLORS["gamma"], "γ"),
            snail(COLORS["delta"], "δ"),
        ).arrange(RIGHT, buff=0.55).scale(0.85)
        snails.next_to(subtitle, DOWN, buff=0.62)

        premise = Text(
            "Four snails move uniformly along straight paths.\n"
            "Five of the six pair meetings have already happened.",
            font_size=27,
            line_spacing=0.8,
            color=COLORS["ink"],
        )
        premise.next_to(snails, DOWN, buff=0.52)

        self.play(FadeIn(title, shift=UP * 0.2), FadeIn(subtitle))
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in snails], lag_ratio=0.12))
        self.play(Write(premise))
        self.wait(1.0)
        self.play(FadeOut(VGroup(title, subtitle, snails, premise)))

    def meeting_graph(self):
        points = {
            "α": LEFT * 2.4 + UP * 1.25,
            "β": RIGHT * 2.4 + UP * 1.25,
            "γ": LEFT * 2.4 + DOWN * 1.15,
            "δ": RIGHT * 2.4 + DOWN * 1.15,
        }
        dots = VGroup()
        labels = VGroup()
        for name, pos in points.items():
            color = {
                "α": COLORS["alpha"],
                "β": COLORS["beta"],
                "γ": COLORS["gamma"],
                "δ": COLORS["delta"],
            }[name]
            dots.add(Dot(pos, radius=0.15, color=color))
            labels.add(Text(name, font_size=28, color=COLORS["ink"]).next_to(pos, UP, buff=0.16))

        edge_pairs = [("α", "β"), ("α", "γ"), ("α", "δ"), ("β", "γ"), ("β", "δ"), ("γ", "δ")]
        edges = VGroup()
        for first, second in edge_pairs:
            edges.add(Line(points[first], points[second], color=COLORS["grid"], stroke_width=4))
        return points, VGroup(edges, dots, labels)

    def counting_step(self):
        header = Text("Step 1: choose a snail that met all three", font_size=32, color=COLORS["ink"])
        header.to_edge(UP, buff=0.45)
        explanation = Text(
            "If every snail had met at most two others, there would be at most 4 × 2 = 8 ends.\n"
            "But five meetings create 5 × 2 = 10 ends.\n"
            "10 > 8, so one snail met all three others. Rename it α.",
            font_size=20,
            line_spacing=0.8,
            color=COLORS["muted"],
        ).to_edge(DOWN, buff=0.28)
        points, graph = self.meeting_graph()
        edges, dots, labels = graph

        self.play(FadeIn(header, shift=DOWN * 0.2))
        self.play(Create(edges), FadeIn(dots), FadeIn(labels))

        occurred = [0, 1, 2, 3, 4]
        active_edges = VGroup()
        for index in occurred:
            edge = edges[index].copy().set_color(COLORS["accent"]).set_stroke(width=6)
            active_edges.add(edge)
            self.play(Create(edge), run_time=0.35)
        missing = edges[5].copy().set_color(COLORS["muted"]).set_stroke(width=3, opacity=0.35)
        self.play(Create(missing), run_time=0.3)

        alpha_ring = Circle(
            radius=0.34,
            color=COLORS["alpha"],
            stroke_width=4,
        ).move_to(points["α"])
        alpha_tag = pill("α met β, γ, δ", color=COLORS["alpha"], width=2.55)
        alpha_tag.next_to(points["α"], RIGHT, buff=0.35)
        self.play(Create(alpha_ring), FadeIn(alpha_tag, shift=RIGHT * 0.15))
        self.play(Write(explanation))
        self.wait(1.2)
        self.play(FadeOut(VGroup(header, explanation, graph, active_edges, missing, alpha_ring, alpha_tag)))

    def riding_frame_step(self):
        header = Text("Step 2: ride with α", font_size=34, color=COLORS["ink"])
        header.to_edge(UP, buff=0.45)
        sub = Text(
            "In this inertial frame, α is fixed at the origin.",
            font_size=25,
            color=COLORS["muted"],
        ).next_to(header, DOWN, buff=0.14)

        axis = Line(LEFT * 5.7, RIGHT * 5.7, color=COLORS["grid"], stroke_width=3)
        origin = Dot(ORIGIN, radius=0.16, color=COLORS["alpha"])
        origin_label = Text("α", font_size=30, color=COLORS["alpha"]).next_to(origin, UP, buff=0.16)
        origin_note = Text("origin", font_size=21, color=COLORS["muted"]).next_to(origin, DOWN, buff=0.14)

        paths = VGroup(
            Line(LEFT * 4.7 + DOWN * 1.65, RIGHT * 4.7 + UP * 1.65, color=COLORS["beta"], stroke_width=4),
            Line(LEFT * 4.7 + UP * 1.15, RIGHT * 4.7 + DOWN * 1.15, color=COLORS["gamma"], stroke_width=4),
            Line(LEFT * 4.7 + DOWN * 0.75, RIGHT * 4.7 + UP * 0.75, color=COLORS["delta"], stroke_width=4),
        )
        path_labels = VGroup(
            Text("β path", font_size=21, color=COLORS["beta"]).next_to(paths[0].get_end(), UP, buff=0.05),
            Text("γ path", font_size=21, color=COLORS["gamma"]).next_to(paths[1].get_start(), UP, buff=0.05),
            Text("δ path", font_size=21, color=COLORS["delta"]).next_to(paths[2].get_end(), UP, buff=0.05),
        )

        note = Text(
            "β, γ, and δ each met α,\nso each path passes through the origin.",
            font_size=25,
            line_spacing=0.8,
            color=COLORS["ink"],
        ).to_edge(DOWN, buff=0.42)

        self.play(FadeIn(header), FadeIn(sub))
        self.play(Create(axis), FadeIn(origin), FadeIn(origin_label), FadeIn(origin_note))
        self.play(LaggedStart(*[Create(path) for path in paths], lag_ratio=0.2), FadeIn(path_labels))

        # Three distinct crossings at the fixed point, one at a time.
        passing_snails = [
            snail(COLORS["beta"], "β", 0.72).move_to(paths[0].point_from_proportion(0.36)),
            snail(COLORS["gamma"], "γ", 0.72).move_to(paths[1].point_from_proportion(0.68)),
            snail(COLORS["delta"], "δ", 0.72).move_to(paths[2].point_from_proportion(0.34)),
        ]
        for mover in passing_snails:
            self.add(mover)
            self.play(mover.animate.move_to(origin.get_center()), run_time=0.8)
            self.play(mover.animate.move_to(mover.get_center() + RIGHT * 0.001), run_time=0.05)
            self.remove(mover)

        self.play(Write(note))
        self.wait(1.1)
        self.play(FadeOut(VGroup(header, sub, axis, origin, origin_label, origin_note, paths, path_labels, note)))

    def collinearity_step(self):
        header = Text("Step 3: two meetings force one line", font_size=33, color=COLORS["ink"])
        header.to_edge(UP, buff=0.45)
        statement = Text(
            "Each path already passes through α's position.\n"
            "β also met γ and δ at separate points.\n"
            "Two different straight paths cannot intersect twice.",
            font_size=23,
            line_spacing=0.8,
            color=COLORS["ink"],
        ).to_edge(DOWN, buff=0.42)

        base = Line(LEFT * 4.8, RIGHT * 4.8, color=COLORS["grid"], stroke_width=3)
        origin = Dot(ORIGIN, radius=0.13, color=COLORS["alpha"])
        origin_label = Text("α's position", font_size=21, color=COLORS["muted"]).next_to(origin, DOWN, buff=0.16)

        beta_path = Line(LEFT * 4.6 + DOWN * 1.05, RIGHT * 4.6 + UP * 1.05, color=COLORS["beta"], stroke_width=5)
        gamma_path = Line(LEFT * 4.6 + UP * 1.05, RIGHT * 4.6 + DOWN * 1.05, color=COLORS["gamma"], stroke_width=5)
        delta_path = Line(LEFT * 4.6 + DOWN * 0.55, RIGHT * 4.6 + UP * 0.55, color=COLORS["delta"], stroke_width=5)

        # First show two possible meeting locations without claiming that
        # either meeting is geometrically valid yet.  Each becomes a real
        # meeting only after the corresponding path is forced onto beta's.
        point_p = RIGHT * 2.15 + UP * 0.49
        point_q = LEFT * 2.15 + DOWN * 0.49
        possible_p = Dot(point_p, radius=0.13, color=COLORS["accent"], fill_opacity=0.28)
        possible_p_label = Text("possible P?", font_size=20, color=COLORS["muted"]).next_to(possible_p, UP, buff=0.16)
        possible_q = Dot(point_q, radius=0.13, color=COLORS["accent"], fill_opacity=0.28)
        possible_q_label = Text("possible Q?", font_size=20, color=COLORS["muted"]).next_to(possible_q, DOWN, buff=0.16)

        self.play(FadeIn(header), Create(base), FadeIn(origin), FadeIn(origin_label))
        self.play(Create(beta_path), Create(gamma_path), Create(delta_path))
        self.play(FadeIn(possible_p), FadeIn(possible_p_label), FadeIn(possible_q), FadeIn(possible_q_label))
        self.play(Write(statement))
        self.wait(0.9)

        actual_p = Dot(point_p, radius=0.14, color=COLORS["accent"])
        actual_p_label = Text("P: β–γ", font_size=21, color=COLORS["accent"]).next_to(actual_p, UP, buff=0.16)
        self.play(
            Transform(gamma_path, beta_path.copy().set_color(COLORS["gamma"])),
            FadeOut(VGroup(possible_p, possible_p_label)),
            FadeIn(actual_p),
            FadeIn(actual_p_label),
            run_time=1.0,
        )

        actual_q = Dot(point_q, radius=0.14, color=COLORS["accent"])
        actual_q_label = Text("Q: β–δ", font_size=21, color=COLORS["accent"]).next_to(actual_q, DOWN, buff=0.16)
        self.play(
            Transform(delta_path, beta_path.copy().set_color(COLORS["delta"])),
            FadeOut(VGroup(possible_q, possible_q_label)),
            FadeIn(actual_q),
            FadeIn(actual_q_label),
            run_time=1.0,
        )

        shared_line = Line(LEFT * 4.8, RIGHT * 4.8, color=COLORS["ink"], stroke_width=7)
        shared_label = Text("β, γ, δ must share this straight line", font_size=25, color=COLORS["ink"])
        shared_label.next_to(shared_line, UP, buff=0.26)
        self.play(
            Transform(beta_path, shared_line.copy().set_color(COLORS["beta"])),
            Transform(gamma_path, shared_line.copy().set_color(COLORS["gamma"])),
            Transform(delta_path, shared_line.copy().set_color(COLORS["delta"])),
            FadeOut(VGroup(actual_p, actual_p_label, actual_q, actual_q_label, origin, origin_label, base)),
            run_time=1.25,
        )
        self.play(FadeIn(shared_label, shift=UP * 0.15))
        self.wait(1.0)
        self.play(FadeOut(VGroup(header, statement, beta_path, gamma_path, delta_path, shared_label)))

    def future_meeting_step(self):
        header = Text("Step 4: the sixth meeting is unavoidable", font_size=32, color=COLORS["ink"])
        header.to_edge(UP, buff=0.45)
        line = Line(LEFT * 5.25, RIGHT * 5.25, color=COLORS["ink"], stroke_width=4)
        path_label = Text("common straight path", font_size=22, color=COLORS["muted"]).next_to(line, DOWN, buff=0.16)
        alpha_dot = Dot(ORIGIN, radius=0.14, color=COLORS["alpha"])
        alpha_label = Text("α fixed at O", font_size=20, color=COLORS["alpha"]).next_to(alpha_dot, UP, buff=0.16)
        arrows = VGroup(
            Arrow(LEFT * 0.8 + UP * 0.65, LEFT * 2.3 + UP * 0.65, buff=0, color=COLORS["beta"], stroke_width=3),
            Arrow(RIGHT * 0.2 + DOWN * 0.65, LEFT * 1.6 + DOWN * 0.65, buff=0, color=COLORS["gamma"], stroke_width=3),
            Arrow(RIGHT * 2.7 + UP * 0.65, LEFT * 0.2 + UP * 0.65, buff=0, color=COLORS["delta"], stroke_width=3),
        )
        speed_note = Text("constant velocities", font_size=22, color=COLORS["muted"]).next_to(arrows, DOWN, buff=0.16)

        past_meetings = Text(
            "Past meetings:  α–β ✓    α–γ ✓    α–δ ✓    β–γ ✓    β–δ ✓",
            font_size=21,
            color=COLORS["muted"],
        ).next_to(header, DOWN, buff=0.14)

        # These are a schematic but kinematically consistent set of positions:
        # x_beta = -(t+1.5), x_gamma = -2(t+1), x_delta = -3(t+0.6).
        def position_at(t):
            return {
                "β": -(t + 1.5),
                "γ": -2 * (t + 1.0),
                "δ": -3 * (t + 0.6),
            }

        scale = 0.8
        def x_on_line(x):
            return RIGHT * (x / scale)

        current_t = ValueTracker(-1.6)
        movers = {
            "β": snail(COLORS["beta"], "β", 0.74),
            "γ": snail(COLORS["gamma"], "γ", 0.74),
            "δ": snail(COLORS["delta"], "δ", 0.74),
        }
        for name, mover in movers.items():
            # The colored shell/body is enough to identify the moving snails
            # here; hiding the small built-in labels keeps the one-dimensional
            # track readable when two snails meet.
            mover[-1].set_opacity(0)
            mover.move_to(x_on_line(position_at(current_t.get_value())[name]))
            mover.shift(UP * 0.1)

        time_text = Text("t = −1.6", font_size=24, color=COLORS["muted"]).to_edge(DOWN, buff=0.42)
        conclusion = Text(
            "γ and δ approach each other along the shared path.\n"
            "Their sixth meeting occurs at t > 0.",
            font_size=24,
            line_spacing=0.8,
            color=COLORS["ink"],
        )
        conclusion.to_edge(DOWN, buff=0.42)

        self.play(FadeIn(header), FadeIn(past_meetings), Create(line), FadeIn(path_label), FadeIn(alpha_dot), FadeIn(alpha_label), FadeIn(arrows), FadeIn(speed_note))
        self.play(*[FadeIn(mover) for mover in movers.values()])
        self.play(FadeIn(time_text))

        def move_mover(mover, name):
            return mover.add_updater(
                lambda mob: mob.move_to(
                    x_on_line(position_at(current_t.get_value())[name]) + UP * 0.1
                )
            )

        for name, mover in movers.items():
            move_mover(mover, name)

        # The five earlier meetings pass in a compact sequence.
        self.play(current_t.animate.set_value(-1.5), run_time=0.55)
        self.play(current_t.animate.set_value(-1.0), run_time=0.55)
        self.play(current_t.animate.set_value(-0.6), run_time=0.55)
        self.play(current_t.animate.set_value(-0.5), run_time=0.50)
        self.play(current_t.animate.set_value(-0.15), run_time=0.50)
        self.play(Transform(time_text, Text("t = 0 — five meetings have happened", font_size=24, color=COLORS["ink"]).to_edge(DOWN, buff=0.42)))
        self.wait(0.65)

        future_event = Dot(x_on_line(-2.4), radius=0.17, color=COLORS["accent"])
        future_event_label = Text("γ–δ", font_size=25, color=COLORS["accent"]).next_to(future_event, UP, buff=0.18)
        self.play(current_t.animate.set_value(0.2), run_time=1.25)
        self.play(
            FadeIn(future_event),
            FadeIn(future_event_label),
            FadeOut(past_meetings),
            FadeOut(speed_note),
            FadeOut(time_text),
        )
        self.remove(past_meetings, speed_note, time_text)
        self.play(Write(conclusion))
        self.wait(1.1)
        for mover in movers.values():
            mover.clear_updaters()
        self.play(FadeOut(VGroup(header, line, path_label, alpha_dot, alpha_label, arrows, *movers.values(), future_event, future_event_label, conclusion)))

    def conclusion(self):
        answer = Text("Yes — the sixth meeting must happen.", font_size=40, color=COLORS["ink"])
        reason = Text(
            "Five meetings force three snails onto one straight trajectory.\n"
            "The remaining pair on that trajectory eventually meets.",
            font_size=26,
            line_spacing=0.8,
            color=COLORS["muted"],
        ).next_to(answer, DOWN, buff=0.28)
        check = Circle(radius=0.54, color=COLORS["accent"], stroke_width=5)
        check_mark = Text("✓", font_size=53, color=COLORS["accent"]).move_to(check.get_center())
        mark = VGroup(check, check_mark).next_to(answer, LEFT, buff=0.45)
        source = Text("F.1 • based on the book's second solution", font_size=20, color=COLORS["muted"])
        source.to_edge(DOWN, buff=0.45)

        self.play(FadeIn(mark, scale=0.7), Write(answer))
        self.play(FadeIn(reason, shift=UP * 0.15), FadeIn(source))
        self.wait(2.0)

"""A concise 2D-to-3D visualization of the first solution of problem F.1.

The scene focuses on the geometric trick in the book:

* x-y shows the ordinary spatial picture;
* t is revealed as the third coordinate, so each uniformly moving snail has
  a straight worldline;
* A, B, C determine a plane, while P and Q force d into that plane;
* c and d therefore meet at the sixth event.

Render with:
    manim -qh snails_worldlines_3d.py SnailsWorldlines3D
"""

import numpy as np

from manim import *


config.background_color = "#0B1020"


COLORS = {
    "a": "#F6C85F",
    "b": "#56CCF2",
    "c": "#BB6BD9",
    "d": "#6FCF97",
    "ink": "#F5F7FA",
    "muted": "#AAB5C4",
    "grid": "#334155",
    "accent": "#FF7A59",
}


class SnailsWorldlines3D(ThreeDScene):
    def construct(self):
        # In the abstract plane spanned by B-A and C-A, the five known
        # meetings are A, B, C, P, Q.  The sixth event R is deliberately
        # later in t than all five known events.
        A = np.array([-1.2, -0.8, 0.0])
        B = np.array([1.2, -0.8, 2.0])
        C = np.array([-1.2, 1.2, 4.0])
        p_factor = 1.15
        q_factor = 1.8
        P = A + p_factor * (C - A)
        Q = A + q_factor * (B - A)
        # R is the exact intersection of c and d.  On c, the coefficients
        # of (B-A) and (C-A) add to 1; on d, it lies on the line P-Q.
        r_u = q_factor * (1.0 - p_factor) / (q_factor - p_factor)
        R = A + r_u * (B - A) + (1.0 - r_u) * (C - A)

        # Start with a genuinely flat spatial construction.  These copies
        # have no time coordinate; they are the 2D paths seen at the opening.
        def flat(point):
            return np.array([point[0], point[1], 0.0])

        A2, B2, C2, P2, Q2 = map(flat, (A, B, C, P, Q))
        flat_worldlines = VGroup(
            Line3D(A2 - 0.18 * (C2 - A2), P2 + 0.20 * (C2 - A2), thickness=0.040, color=COLORS["a"]),
            Line3D(A2 - 0.18 * (B2 - A2), Q2 + 0.18 * (B2 - A2), thickness=0.040, color=COLORS["b"]),
            Line3D(B2 - 0.22 * (C2 - B2), C2 + 0.72 * (C2 - B2), thickness=0.040, color=COLORS["c"]),
            Line3D(P2 - 0.42 * (P2 - Q2), Q2 + 0.12 * (P2 - Q2), thickness=0.040, color=COLORS["d"]),
        )

        # The same paths become straight spacetime worldlines only after t is
        # introduced as the third coordinate.
        a_line = Line3D(A - 0.18 * (C - A), P + 0.20 * (C - A), thickness=0.040, color=COLORS["a"])
        b_line = Line3D(A - 0.18 * (B - A), Q + 0.18 * (B - A), thickness=0.040, color=COLORS["b"])
        c_line = Line3D(B - 0.22 * (C - B), C + 0.72 * (C - B), thickness=0.040, color=COLORS["c"])
        d_line = Line3D(P - 0.42 * (P - Q), Q + 0.12 * (P - Q), thickness=0.040, color=COLORS["d"])
        worldlines_3d = VGroup(a_line, b_line, c_line, d_line)
        worldlines = flat_worldlines

        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-2.5, 4, 1],
            z_range=[-1, 6, 1],
            x_length=8.0,
            y_length=5.8,
            z_length=5.6,
            axis_config={"color": COLORS["grid"], "stroke_width": 2},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
            z_axis_config={"include_numbers": False},
        )
        axes.z_axis.set_opacity(0)

        x_label = Text("x", font_size=23, color=COLORS["muted"]).move_to(axes.x_axis.get_end() + RIGHT * 0.15)
        y_label = Text("y", font_size=23, color=COLORS["muted"]).move_to(axes.y_axis.get_end() + UP * 0.15)
        # Keep the time label in the screen plane so it cannot disappear
        # behind a worldline when the camera tilts.
        t_label = Text("t", font_size=34, color=COLORS["accent"]).to_corner(UR, buff=0.75)
        self.add_fixed_orientation_mobjects(x_label, y_label)
        self.add_fixed_in_frame_mobjects(t_label)
        t_label.set_opacity(0)

        title = Text("The spacetime trick", font_size=36, color=COLORS["ink"]).to_edge(UP, buff=0.25)
        caption = Text("2D: only the spatial paths are visible.", font_size=23, color=COLORS["muted"])
        caption.to_edge(DOWN, buff=0.36)
        self.add_fixed_in_frame_mobjects(title, caption)

        frame_center = np.array([0.0, 0.0, 2.4])
        self.set_camera_orientation(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            zoom=0.72,
            frame_center=frame_center,
        )
        self.play(FadeIn(title), FadeIn(caption))
        self.play(Create(axes), LaggedStart(*[Create(line) for line in flat_worldlines], lag_ratio=0.14))
        self.wait(1.0)

        # Tilt the camera so the hidden time coordinate becomes visible.
        next_caption = Text("Add time t as the third coordinate.", font_size=23, color=COLORS["muted"])
        next_caption.move_to(caption.get_center())
        next_caption.set_opacity(0)
        self.add_fixed_in_frame_mobjects(next_caption)
        self.play(FadeOut(caption), axes.z_axis.animate.set_opacity(1), t_label.animate.set_opacity(1), run_time=0.4)
        self.remove(caption)
        self.camera.remove_fixed_in_frame_mobjects(caption)
        self.play(next_caption.animate.set_opacity(1), run_time=0.4)
        caption = next_caption
        self.move_camera(
            phi=62 * DEGREES,
            theta=-55 * DEGREES,
            zoom=0.72,
            frame_center=frame_center,
            run_time=2.2,
        )
        self.play(Transform(flat_worldlines, worldlines_3d), run_time=0.9)
        worldlines = flat_worldlines
        a_line, b_line, c_line, d_line = worldlines

        line_labels = VGroup(*[
            Text("a", font_size=23, color=COLORS["a"]).move_to(A + 0.88 * (C - A) + UP * 0.18),
            Text("b", font_size=23, color=COLORS["b"]).move_to(A + 0.72 * (B - A) + RIGHT * 0.15),
            Text("c", font_size=23, color=COLORS["c"]).move_to(B + 0.62 * (C - B) + LEFT * 0.15),
            Text("d", font_size=23, color=COLORS["d"]).move_to(P + 0.48 * (Q - P) + RIGHT * 0.15),
        ])
        self.add_fixed_orientation_mobjects(*line_labels)

        event_points = {"A": A, "B": B, "C": C, "P": P, "Q": Q}
        event_offsets = {
            "A": LEFT * 0.18 + DOWN * 0.17,
            "B": RIGHT * 0.18 + DOWN * 0.16,
            "C": LEFT * 0.28 + UP * 0.16,
            "P": RIGHT * 0.28 + UP * 0.16,
            "Q": RIGHT * 0.22 + DOWN * 0.18,
        }
        event_dots = VGroup(*[
            Dot3D(point, radius=0.10, color=COLORS["accent"])
            for point in event_points.values()
        ])
        event_labels = [
            Text(name, font_size=22, color=COLORS["accent"]).move_to(event_points[name] + event_offsets[name])
            for name in event_points
        ]
        self.add_fixed_orientation_mobjects(*event_labels)

        event_caption = Text("The five meetings are A, B, C, P, Q.", font_size=23, color=COLORS["muted"])
        event_caption.move_to(caption.get_center())
        event_caption.set_opacity(0)
        self.add_fixed_in_frame_mobjects(event_caption)
        self.play(
            FadeIn(line_labels),
            FadeIn(event_dots),
            FadeIn(VGroup(*event_labels)),
            FadeOut(caption),
            run_time=0.6,
        )
        self.remove(caption)
        self.camera.remove_fixed_in_frame_mobjects(caption)
        self.play(event_caption.animate.set_opacity(1), run_time=0.4)
        caption = event_caption

        # A, B, C visibly determine a plane.
        plane_triangle = Polygon(
            A, B, C,
            stroke_color=COLORS["accent"],
            stroke_width=3,
            fill_color=COLORS["accent"],
            fill_opacity=0.16,
        )
        plane_u = B - A
        plane_v = C - A
        # A compact quadrilateral through the relevant events keeps the plane
        # visible without sending its far corners outside the spacetime box.
        plane = Polygon(
            A, Q, P, R,
            stroke_color=COLORS["accent"],
            stroke_width=2,
            fill_color=COLORS["accent"],
            fill_opacity=0.08,
        )
        plane_caption = Text("A, B, C determine one plane.", font_size=23, color=COLORS["ink"])
        plane_caption.move_to(caption.get_center())
        plane_caption.set_opacity(0)
        self.add_fixed_in_frame_mobjects(plane_caption)
        self.play(FadeIn(plane_triangle), FadeOut(caption), run_time=0.55)
        self.remove(caption)
        self.camera.remove_fixed_in_frame_mobjects(caption)
        self.play(plane_caption.animate.set_opacity(1), run_time=0.45)
        caption = plane_caption
        self.play(FadeIn(plane), FadeOut(plane_triangle), Indicate(event_dots[:3]), run_time=1.0)

        pq_caption = Text("P and Q lie in that same plane.", font_size=23, color=COLORS["ink"])
        pq_caption.move_to(caption.get_center())
        pq_caption.set_opacity(0)
        self.add_fixed_in_frame_mobjects(pq_caption)
        self.play(Indicate(event_dots[3:]), FadeOut(caption), run_time=0.6)
        self.remove(caption)
        self.camera.remove_fixed_in_frame_mobjects(caption)
        self.play(pq_caption.animate.set_opacity(1), run_time=0.4)
        caption = pq_caption

        d_caption = Text("d passes through P and Q, so d is in the plane.", font_size=22, color=COLORS["ink"])
        d_caption.move_to(caption.get_center())
        d_caption.set_opacity(0)
        self.add_fixed_in_frame_mobjects(d_caption)
        self.play(Indicate(d_line, color=COLORS["d"]), FadeOut(caption), run_time=0.7)
        self.remove(caption)
        self.camera.remove_fixed_in_frame_mobjects(caption)
        self.play(d_caption.animate.set_opacity(1), run_time=0.45)
        caption = d_caption

        # The remaining two worldlines are now coplanar and intersect at R.
        R_dot = Dot3D(R, radius=0.14, color=COLORS["accent"])
        R_label = Text("R: sixth meeting", font_size=22, color=COLORS["accent"]).move_to(
            R + LEFT * 0.95 + UP * 0.42 + OUT * 0.12
        )
        self.add_fixed_orientation_mobjects(R_label)
        final_caption = Text("c and d intersect: the sixth meeting.", font_size=23, color=COLORS["ink"])
        final_caption.move_to(caption.get_center())
        final_caption.set_opacity(0)
        self.add_fixed_in_frame_mobjects(final_caption)
        self.play(
            Indicate(c_line, color=COLORS["c"]),
            FadeIn(R_dot),
            FadeIn(R_label),
            FadeOut(caption),
            run_time=0.75,
        )
        self.remove(caption)
        self.camera.remove_fixed_in_frame_mobjects(caption)
        self.play(final_caption.animate.set_opacity(1), run_time=0.5)
        caption = final_caption
        self.play(Flash(R_dot, color=COLORS["accent"]), run_time=0.8)

        # Let the coordinate frame rotate so the coplanarity can be seen from
        # more than one angle; labels stay readable while the geometry turns.
        # Clear the explanatory caption before the camera moves.  A fresh
        # fixed-frame caption after the rotation avoids leaving transformed
        # glyphs behind while the 3D renderer is moving the scene.
        self.play(FadeOut(caption), run_time=0.35)
        self.remove(caption)
        self.camera.remove_fixed_in_frame_mobjects(caption)
        self.begin_ambient_camera_rotation(rate=0.075)
        self.wait(3.4)
        self.stop_ambient_camera_rotation()
        rotate_caption = Text("Rotate the frame: all four worldlines are coplanar.", font_size=22, color=COLORS["muted"])
        rotate_caption.to_edge(DOWN, buff=0.36)
        rotate_caption.set_opacity(0)
        self.add_fixed_in_frame_mobjects(rotate_caption)
        self.play(rotate_caption.animate.set_opacity(1), run_time=0.5)
        self.wait(0.8)

        self.play(
            FadeOut(VGroup(axes, worldlines, plane, event_dots, *line_labels, *event_labels, R_dot, R_label)),
            FadeOut(title),
            FadeOut(rotate_caption),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(t_label),
        )

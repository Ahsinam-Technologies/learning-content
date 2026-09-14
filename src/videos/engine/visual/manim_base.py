"""
BayesStack Manim base classes and visual styling constants.
Integrates the BayesStack mint & teal color system, typography, and layout templates into Manim.
"""
from typing import Dict, Any, Optional

# BayesStack Visual Color Palette (Hex & RGB)
BAYES_TEAL = "#0B6763"
BAYES_BRAND_TEAL = "#056766"
BAYES_DEEP_TEAL = "#084C49"
BAYES_DARK = "#091A18"
BAYES_INK = "#123333"
BAYES_PALE = "#E4F2EF"
BAYES_BORDER = "#D7E8E4"
BAYES_WHITE = "#FFFFFF"

# Semantic Accents
BAYES_AMBER = "#964200"
BAYES_BLUE = "#125282"
BAYES_PLUM = "#5E3268"
BAYES_GREEN = "#1A6634"
BAYES_BROWN = "#5F370E"

# Typography and Resolution Defaults
DEFAULT_VIDEO_FPS = 30
DEFAULT_VIDEO_RES = (1920, 1080)
DEFAULT_FONT = "Outfit"

try:
    from manim import (
        Scene, Text, Tex, MathTex, VGroup, Rectangle, RoundedRectangle,
        Create, Write, FadeIn, FadeOut, Transform, ReplacementTransform,
        config, UP, DOWN, LEFT, RIGHT, ORIGIN, UL, UR, DL, DR
    )
    MANIM_AVAILABLE = True
except ImportError:
    MANIM_AVAILABLE = False
    class Scene:
        """Stub Scene class when manim is not installed locally."""
        pass

class BayesStackScene(Scene):
    """
    Base Scene class with BayesStack branding, header banners, and responsive layout grids.
    """

    def construct(self):
        if not MANIM_AVAILABLE:
            print("Notice: Manim is not installed in the current environment. Running in mock/dry-run mode.")
            return

        # Configure background
        self.camera.background_color = BAYES_DARK

    def create_title(self, title_text: str, subtitle_text: Optional[str] = None):
        """Creates a standardized BayesStack title banner at the top of the frame."""
        if not MANIM_AVAILABLE:
            return None

        title = Text(title_text, font=DEFAULT_FONT, color=BAYES_WHITE, weight="BOLD").scale(0.8)
        title.to_corner(UL).shift(RIGHT * 0.5 + DOWN * 0.3)

        line = Rectangle(
            width=13.0, height=0.03,
            color=BAYES_TEAL, fill_color=BAYES_TEAL, fill_opacity=1.0
        ).next_to(title, DOWN, aligned_edge=LEFT).shift(DOWN * 0.1)

        group = VGroup(title, line)
        if subtitle_text:
            subtitle = Text(subtitle_text, font="Inter", color=BAYES_PALE).scale(0.5)
            subtitle.next_to(line, DOWN, aligned_edge=LEFT).shift(DOWN * 0.1)
            group.add(subtitle)

        return group

    def create_card(self, title: str, content: str, width: float = 6.0, height: float = 4.0):
        """Creates a styled card container for equations, definitions, or code."""
        if not MANIM_AVAILABLE:
            return None

        card_bg = RoundedRectangle(
            corner_radius=0.15, width=width, height=height,
            color=BAYES_TEAL, fill_color=BAYES_INK, fill_opacity=0.9
        )
        card_title = Text(title, font=DEFAULT_FONT, color=BAYES_PALE, weight="BOLD").scale(0.5)
        card_title.next_to(card_bg.get_top(), DOWN, buff=0.3)

        sep = Rectangle(width=width - 0.6, height=0.02, color=BAYES_TEAL, fill_opacity=1.0)
        sep.next_to(card_title, DOWN, buff=0.15)

        card_body = Text(content, font="Inter", color=BAYES_WHITE).scale(0.4)
        card_body.next_to(sep, DOWN, buff=0.3)

        return VGroup(card_bg, card_title, sep, card_body)

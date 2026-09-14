"""
Manim Scene Script Template for BayesStack Video Generation.
Save in course videos session folder: <Course>/videos/session-XX-<name>/scene.py
"""
import sys
import os

# Add src to python path for importing engine visual helpers
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

try:
    from manim import *
    from videos.engine.visual.manim_base import (
        BayesStackScene, BAYES_TEAL, BAYES_DARK, BAYES_PALE, BAYES_INK,
        BAYES_AMBER, BAYES_BLUE, BAYES_WHITE
    )
except ImportError:
    # Fallback stub for syntax checking without manim installed
    class BayesStackScene:
        def construct(self): pass

class SessionVideoScene(BayesStackScene):
    """
    Manim Scene orchestrating visual animations synchronized with narration.yaml.
    """

    def construct(self):
        super().construct()
        
        # --- Scene 1: Introduction ---
        title = self.create_title("Session 01: Core Principles", "BayesStack Computational Foundations")
        if title:
            self.play(FadeIn(title))
            self.wait(2)

        # --- Scene 2: Mathematical Derivation Card ---
        card = self.create_card(
            title="Bayes' Rule Invariant",
            content="p(theta | y) = [ p(y | theta) * p(theta) ] / p(y)",
            width=8.0, height=3.5
        )
        if card:
            self.play(Create(card))
            self.wait(3)
            self.play(FadeOut(card))

        # --- Scene 3: Summary Outro ---
        outro = self.create_card(
            title="Key Takeaways",
            content="1. Always calculate in log-space\n2. Maintain proper conjugate priors\n3. Check prior predictive bounds",
            width=8.5, height=4.0
        )
        if outro:
            self.play(Create(outro))
            self.wait(3)

if __name__ == "__main__":
    # Allows rendering via: python3 scene.py -pql
    pass

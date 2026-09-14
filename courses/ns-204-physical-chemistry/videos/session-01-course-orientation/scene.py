"""
Manim Scene Script for BayesStack Video Generation.
Course: NS 204 - Physical Chemistry | Session 01: Course Orientation
"""
import sys
import os

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
    class BayesStackScene:
        def construct(self): pass

class SessionScene(BayesStackScene):
    """
    4-Scene Animation Script for NS 204 Session 01
    """

    def construct(self):
        super().construct()
        
        # --- Scene 1: Introduction ---
        title = self.create_title("NS 204: Session 01", "Course Orientation")
        card1 = self.create_card(
            title="Overview & Motivation",
            content="Course: Physical Chemistry\n\nSession Goal: Establish fundamental definitions & invariants.",
            width=10.0, height=3.5
        )
        if title and card1:
            self.play(FadeIn(title))
            card1.move_to(ORIGIN)
            self.play(Create(card1))
            self.wait(3)
            self.play(FadeOut(card1))

        # --- Scene 2: Formal Model ---
        card2 = self.create_card(
            title="Core Conceptual Framework",
            content="State Space & Equations:\n\nStructured Formulation with Rigorous Invariants",
            width=10.0, height=3.5
        )
        if card2:
            card2.move_to(ORIGIN)
            self.play(Create(card2))
            self.wait(4)
            self.play(FadeOut(card2))

        # --- Scene 3: Practical Implementation ---
        card3 = self.create_card(
            title="System & Algorithmic Design",
            content="Applied Properties:\n\n1. Numerical Robustness\n2. Scalable Computation\n3. Modularity",
            width=10.0, height=3.5
        )
        if card3:
            card3.move_to(ORIGIN)
            self.play(Create(card3))
            self.wait(4)
            self.play(FadeOut(card3))

        # --- Scene 4: Summary ---
        card4 = self.create_card(
            title="Session Takeaways",
            content="Key Results:\n\n- Foundational properties established\n- Read Chapter 01 in Notes",
            width=10.0, height=3.5
        )
        if card4:
            card4.move_to(ORIGIN)
            self.play(Create(card4))
            self.wait(4)
            self.play(FadeOut(card4), FadeOut(title))

if __name__ == "__main__":
    pass

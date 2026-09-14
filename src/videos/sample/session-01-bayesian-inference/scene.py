"""
Manim Scene Animation for Sample Video: Foundations of Bayesian Inference
Course: SAMPLE 101 | Session 01
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

class BayesianInferenceScene(BayesStackScene):
    """
    4-Scene Animation Pipeline matching narration.yaml for Session 01:
    1. Probability as Logic
    2. Bayes' Rule Formula Decomposition
    3. Conjugacy & Precision Weighting
    4. Production Numerical Stability Invariants
    """

    def construct(self):
        super().construct()
        
        # --- Scene 1: Introduction & Epistemic Probability ---
        title = self.create_title("Session 01: Bayesian Inference", "BayesStack Computational Foundations")
        card1 = self.create_card(
            title="Scientific Inquiry as Inverse Problem",
            content="Latent State (theta)  -->  Data Generating Process  -->  Observations (y)\n\nProbability = Representation of Incomplete Information",
            width=10.0, height=3.5
        )
        if title and card1:
            self.play(FadeIn(title))
            card1.move_to(ORIGIN)
            self.play(Create(card1))
            self.wait(3)
            self.play(FadeOut(card1))

        # --- Scene 2: Anatomy of Bayes' Rule ---
        card2 = self.create_card(
            title="Bayes' Theorem Decomposition",
            content="Posterior = [ Likelihood x Prior ] / Marginal Evidence\n\np(theta | y) = [ p(y | theta) * p(theta) ] / p(y)",
            width=10.5, height=3.8
        )
        if card2:
            card2.move_to(ORIGIN)
            self.play(Create(card2))
            self.wait(4)
            self.play(FadeOut(card2))

        # --- Scene 3: Precision-Weighted Normal Updating ---
        card3 = self.create_card(
            title="Precision-Weighted Conjugate Updating",
            content="Posterior Precision = Prior Precision + Sample Precision\n\ntau_post = tau_0 + n * tau_data\nmu_post = (tau_0 * mu_0 + n * tau_data * y_bar) / tau_post",
            width=11.0, height=4.0
        )
        if card3:
            card3.move_to(ORIGIN)
            self.play(Create(card3))
            self.wait(4)
            self.play(FadeOut(card3))

        # --- Scene 4: Production Invariants & Log-Space ---
        card4 = self.create_card(
            title="Production Invariant: Log-Space Computation",
            content="Avoid Underflow: log p(theta | y) = log p(y | theta) + log p(theta) - log p(y)\n\nAlways use log-sum-exp for evidence summation.",
            width=11.0, height=3.8
        )
        if card4:
            card4.move_to(ORIGIN)
            self.play(Create(card4))
            self.wait(4)
            self.play(FadeOut(card4), FadeOut(title))

if __name__ == "__main__":
    pass

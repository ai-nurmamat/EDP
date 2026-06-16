"""
Expected Domain Perception
期望域感知法

Flow Amplification Analysis Engine.

This module implements the probability flow amplification effect analysis,
which is one of the most powerful analytical tools in Expected Domain Perception.

The amplification effect is based on:
- Time series momentum (Moskowitz et al., 2012)
- Information cascade models (Banerjee, 1992)

A Methodology for Asymmetric Expected Value Discovery Based on Probability Flow and Domain Awareness

References:
    Moskowitz, T.J., Ooi, Y.H. & Pedersen, L.H. (2012). "Time Series Momentum."
    Journal of Financial Economics, 104(2), 228-250.

    Banerjee, A.V. (1992). "A Simple Model of Herd Behavior."
    The Quarterly Journal of Economics, 107(3), 797-817.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from .probability_engine import FlowDirection, FlowReport, FlowResult


class AmplificationLevel(Enum):
    """Classification of amplification effect strength."""

    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class AmplificationResult:
    """
    Result of amplification effect calculation for a single outcome.

    The amplification score is calculated as:
    Amplification_Score = Base_Flow × Directional_Consistency × Gradient_Position
    """

    outcome: str
    base_flow_pp: float
    directional_consistency: float  # 0.0 to 1.0
    gradient_position: float  # Normalized position in gradient
    amplification_score: float
    level: AmplificationLevel
    confidence: float = 1.0  # Confidence after domain awareness validation

    def is_reliable(self, min_confidence: float = 0.5) -> bool:
        """Check if amplification result is reliable enough for use."""
        return self.confidence >= min_confidence and self.level != AmplificationLevel.NONE


@dataclass
class AmplificationReport:
    """
    Complete amplification analysis report for a market.

    Contains all amplification results and aggregate statistics.
    """

    match_id: str
    flow_report: FlowReport
    amplifications: list[AmplificationResult] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)

    def get_high_amplification(self) -> list[AmplificationResult]:
        """Return outcomes with high or very high amplification."""
        return [
            a
            for a in self.amplifications
            if a.level in (AmplificationLevel.HIGH, AmplificationLevel.VERY_HIGH)
        ]

    def get_reliable_amplifications(self, min_confidence: float = 0.5) -> list[AmplificationResult]:
        """Return all reliable amplification results."""
        return [a for a in self.amplifications if a.is_reliable(min_confidence)]


class FlowAnalyzer:
    """
    Probability flow amplification effect analyzer.

    The amplification effect occurs when probability flow shows money moving
    from outcome A to outcome B, typically meaning adjacent outcomes on the
    same directional gradient are also flowing in the same direction.

    Example:
        >>> analyzer = FlowAnalyzer()
        >>> report = analyzer.calculate_amplification(flow_report, gradient_map)
        >>> high_amp = report.get_high_amplification()
    """

    # Thresholds for amplification level classification
    AMPLIFICATION_THRESHOLD_LOW = 1.0
    AMPLIFICATION_THRESHOLD_MEDIUM = 3.0
    AMPLIFICATION_THRESHOLD_HIGH = 5.0
    AMPLIFICATION_THRESHOLD_VERY_HIGH = 10.0

    # Minimum base flow to enable amplification (in percentage points)
    MIN_BASE_FLOW_THRESHOLD = 2.0

    def __init__(self, config: Optional[dict] = None):
        """
        Initialize the flow analyzer.

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.min_base_flow = self.config.get(
            "min_base_flow", self.MIN_BASE_FLOW_THRESHOLD
        )

    def calculate_directional_consistency(
        self,
        flow_report: FlowReport,
        outcome: str,
        adjacent_outcomes: list[str],
    ) -> float:
        """
        Calculate directional consistency for an outcome.

        Directional consistency is the proportion of adjacent outcomes
        in the same direction that have positive flow.

        Args:
            flow_report: Flow analysis report
            outcome: The outcome to analyze
            adjacent_outcomes: List of adjacent outcomes in same direction

        Returns:
            Consistency score between 0.0 and 1.0
        """
        if not adjacent_outcomes:
            return 0.0

        flow_map = {f.outcome: f for f in flow_report.flows}
        positive_count = 0

        for adj_outcome in adjacent_outcomes:
            if adj_outcome in flow_map:
                if flow_map[adj_outcome].direction == FlowDirection.POSITIVE:
                    positive_count += 1

        return positive_count / len(adjacent_outcomes)

    def calculate_gradient_position(
        self,
        outcome: str,
        outcome_probabilities: dict[str, float],
        direction_outcomes: list[str],
    ) -> float:
        """
        Calculate normalized gradient position for an outcome.

        Higher probability outcomes have lower gradient position values,
        meaning lower amplification potential. Lower probability outcomes
        have higher gradient position, meaning higher amplification potential.

        Args:
            outcome: The outcome to analyze
            outcome_probabilities: All outcome probabilities
            direction_outcomes: Outcomes in the same direction

        Returns:
            Normalized gradient position between 0.0 and 1.0
        """
        if outcome not in outcome_probabilities:
            return 0.0

        direction_probs = {
            o: outcome_probabilities.get(o, 0) for o in direction_outcomes
        }

        if not direction_probs:
            return 0.0

        max_prob = max(direction_probs.values())
        min_prob = min(direction_probs.values())

        if max_prob == min_prob:
            return 0.5

        # Invert: lower probability = higher position
        outcome_prob = outcome_probabilities[outcome]
        position = (max_prob - outcome_prob) / (max_prob - min_prob)

        return position

    def classify_amplification_level(self, score: float) -> AmplificationLevel:
        """
        Classify amplification score into a level.

        Args:
            score: The amplification score

        Returns:
            AmplificationLevel classification
        """
        if score < self.AMPLIFICATION_THRESHOLD_LOW:
            return AmplificationLevel.NONE
        elif score < self.AMPLIFICATION_THRESHOLD_MEDIUM:
            return AmplificationLevel.LOW
        elif score < self.AMPLIFICATION_THRESHOLD_HIGH:
            return AmplificationLevel.MEDIUM
        elif score < self.AMPLIFICATION_THRESHOLD_VERY_HIGH:
            return AmplificationLevel.HIGH
        else:
            return AmplificationLevel.VERY_HIGH

    def calculate_amplification(
        self,
        flow_report: FlowReport,
        gradient_map: dict[str, list[str]],
        outcome_probabilities: dict[str, float],
        domain_confidence: Optional[dict[str, float]] = None,
    ) -> AmplificationReport:
        """
        Calculate amplification effect for all outcomes.

        Amplification_Score = Base_Flow × Directional_Consistency × Gradient_Position

        Args:
            flow_report: Flow analysis report
            gradient_map: Dictionary mapping outcomes to their adjacent outcomes
            outcome_probabilities: Current true probabilities
            domain_confidence: Optional confidence scores from domain awareness

        Returns:
            AmplificationReport with all amplification results
        """
        amplifications = []
        domain_confidence = domain_confidence or {}

        for flow_result in flow_report.flows:
            outcome = flow_result.outcome
            base_flow = flow_result.flow_pp

            # Safeguard 2: Skip if base flow below threshold
            if abs(base_flow) < self.min_base_flow:
                amplifications.append(
                    AmplificationResult(
                        outcome=outcome,
                        base_flow_pp=base_flow,
                        directional_consistency=0.0,
                        gradient_position=0.0,
                        amplification_score=0.0,
                        level=AmplificationLevel.NONE,
                        confidence=domain_confidence.get(outcome, 0.0),
                    )
                )
                continue

            # Get adjacent outcomes in same direction
            adjacent = gradient_map.get(outcome, [])

            # Calculate components
            directional_consistency = self.calculate_directional_consistency(
                flow_report, outcome, adjacent
            )
            gradient_position = self.calculate_gradient_position(
                outcome, outcome_probabilities, adjacent
            )

            # Calculate amplification score
            # Only positive flows get amplified
            if flow_result.direction == FlowDirection.POSITIVE:
                amplification_score = (
                    base_flow * directional_consistency * (1 + gradient_position)
                )
            else:
                amplification_score = 0.0

            # Classify level
            level = self.classify_amplification_level(amplification_score)

            # Apply domain confidence (Safeguard 1)
            confidence = domain_confidence.get(outcome, 1.0)
            adjusted_score = amplification_score * confidence

            amplifications.append(
                AmplificationResult(
                    outcome=outcome,
                    base_flow_pp=base_flow,
                    directional_consistency=directional_consistency,
                    gradient_position=gradient_position,
                    amplification_score=adjusted_score,
                    level=level,
                    confidence=confidence,
                )
            )

        return AmplificationReport(
            match_id=flow_report.match_id,
            flow_report=flow_report,
            amplifications=amplifications,
        )


__all__ = [
    "AmplificationLevel",
    "AmplificationResult",
    "AmplificationReport",
    "FlowAnalyzer",
]

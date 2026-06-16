"""
SPAF - Sports Analytics Framework
Probability Flow Amplification Engine

This module implements the probability flow amplification effect analysis,
one of the most innovative components of the SPAF framework.

The amplification effect is based on:
- Time series momentum theory (Moskowitz et al., 2012)
- Information cascade models (Banerjee, 1992)
- Market efficiency analysis (Wolfers & Zitzewitz, 2006)

⚠️ ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional
import math


class AmplificationLevel(Enum):
    """Classification of amplification effect strength."""

    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"
    EXCEPTIONAL = "exceptional"


@dataclass
class GradientEdge:
    """
    Represents an edge in the outcome gradient graph.

    Links outcomes that are adjacent in the probability space.
    """

    source_outcome: str
    target_outcome: str
    transition_probability: float = 1.0  # How likely flow transfers along this edge
    distance: float = 1.0  # Distance in probability space


@dataclass
class GradientGraph:
    """
    Graph structure representing relationships between outcomes.

    Nodes are outcomes, edges represent potential flow amplification paths.
    """

    nodes: list[str] = field(default_factory=list)
    edges: list[GradientEdge] = field(default_factory=list)
    adjacency_map: dict[str, list[str]] = field(default_factory=dict)

    def add_edge(self, source: str, target: str, distance: float = 1.0) -> None:
        """Add a directed edge from source to target."""
        if source not in self.nodes:
            self.nodes.append(source)
        if target not in self.nodes:
            self.nodes.append(target)
        
        edge = GradientEdge(
            source_outcome=source,
            target_outcome=target,
            distance=distance,
        )
        self.edges.append(edge)
        
        if source not in self.adjacency_map:
            self.adjacency_map[source] = []
        self.adjacency_map[source].append(target)

    def get_adjacent_outcomes(self, outcome: str) -> list[str]:
        """Get all outcomes adjacent to the given outcome."""
        return self.adjacency_map.get(outcome, [])

    @staticmethod
    def build_correct_score_gradient() -> "GradientGraph":
        """Build gradient graph for correct score market."""
        graph = GradientGraph()
        
        # Home win direction (increasing margin)
        home_scores = ["1:0", "2:0", "2:1", "3:0", "3:1", "3:2", "4:0", "4:1", "4:2", "4:3"]
        for i in range(len(home_scores) - 1):
            graph.add_edge(home_scores[i], home_scores[i + 1], distance=1.0)
        
        # Draw direction
        draws = ["0:0", "1:1", "2:2", "3:3"]
        for i in range(len(draws) - 1):
            graph.add_edge(draws[i], draws[i + 1], distance=1.0)
        
        # Away win direction
        away_scores = ["0:1", "0:2", "1:2", "0:3", "1:3", "2:3", "0:4", "1:4", "2:4", "3:4"]
        for i in range(len(away_scores) - 1):
            graph.add_edge(away_scores[i], away_scores[i + 1], distance=1.0)
        
        # Cross-direction edges (smaller probability)
        graph.add_edge("1:0", "1:1", distance=2.0)  # Home to Draw
        graph.add_edge("1:1", "0:1", distance=2.0)  # Draw to Away
        graph.add_edge("2:0", "2:1", distance=1.5)
        graph.add_edge("2:1", "2:2", distance=2.0)
        graph.add_edge("3:0", "3:1", distance=1.5)
        graph.add_edge("3:1", "3:2", distance=1.5)
        
        return graph


@dataclass
class AmplificationResult:
    """
    Result of amplification effect calculation for a single outcome.

    The amplification score is calculated as:
    Amplification_Score = Base_Flow × Directional_Consistency × Gradient_Position × Market_Momentum

    This represents how the probability flow is expected to propagate
    through adjacent outcomes in the gradient graph.
    """

    outcome: str
    base_flow_pp: float  # Base probability flow in percentage points
    directional_consistency: float  # 0.0 to 1.0
    gradient_position: float  # Normalized position in gradient
    market_momentum: float  # Cross-market momentum factor
    amplification_score: float  # Final amplified score
    level: AmplificationLevel
    confidence: float = 1.0
    propagation_depth: int = 1  # How many steps the flow can propagate
    adjacent_signals: list[tuple[str, float]] = field(default_factory=list)

    def is_reliable(self, min_confidence: float = 0.5) -> bool:
        """Check if amplification result is reliable enough for use."""
        return (
            self.confidence >= min_confidence and 
            self.level != AmplificationLevel.NONE
        )

    def get_signal_strength(self) -> float:
        """Calculate overall signal strength (0-1)."""
        return min(self.amplification_score / 10.0, 1.0)


@dataclass
class AmplificationReport:
    """
    Complete amplification analysis report for a market.

    Contains all amplification results with propagation analysis.
    """

    match_id: str
    outcomes: list[str]
    amplifications: list[AmplificationResult] = field(default_factory=list)
    aggregate_momentum: float = 0.0
    market_cascade_risk: float = 0.0  # Risk of cascading false signals
    generated_at: datetime = field(default_factory=datetime.now)

    def get_high_amplification(self) -> list[AmplificationResult]:
        """Return outcomes with high or very high amplification."""
        return [
            a for a in self.amplifications
            if a.level in (
                AmplificationLevel.HIGH, 
                AmplificationLevel.VERY_HIGH,
                AmplificationLevel.EXCEPTIONAL
            )
        ]

    def get_reliable_amplifications(
        self, 
        min_confidence: float = 0.5
    ) -> list[AmplificationResult]:
        """Return all reliable amplification results."""
        return [a for a in self.amplifications if a.is_reliable(min_confidence)]

    def get_cascading_signals(self) -> dict[str, list[str]]:
        """
        Get signals that could cascade through the gradient.

        Returns mapping of primary signals to their cascade effects.
        """
        cascading = {}
        for amp in self.get_high_amplification():
            if amp.propagation_depth > 1:
                cascading[amp.outcome] = [
                    adj[0] for adj in amp.adjacent_signals[:amp.propagation_depth]
                ]
        return cascading


class FlowAmplificationEngine:
    """
    Advanced probability flow amplification effect analyzer.

    The amplification effect occurs when probability flow shows movement
    from outcome A to outcome B, typically meaning adjacent outcomes on the
    same directional gradient are also flowing in the same direction.

    This creates a cascading effect where the initial signal "amplifies"
    as it propagates through related outcomes.

    Example:
        >>> engine = FlowAmplificationEngine()
        >>> report = engine.calculate_amplification(flow_report, gradient_graph)
        >>> high_amp = report.get_high_amplification()
    """

    # Amplification thresholds
    THRESHOLD_LOW = 1.0
    THRESHOLD_MEDIUM = 3.0
    THRESHOLD_HIGH = 6.0
    THRESHOLD_VERY_HIGH = 10.0
    THRESHOLD_EXCEPTIONAL = 15.0

    # Minimum base flow to enable amplification (in percentage points)
    MIN_BASE_FLOW_THRESHOLD = 1.0

    # Momentum factors
    CROSS_MARKET_MOMENTUM_WINDOW = 3  # Number of adjacent outcomes to check

    def __init__(self, config: Optional[dict[str, Any]] = None):
        """
        Initialize the flow amplification engine.

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.min_base_flow = self.config.get(
            "min_base_flow", self.MIN_BASE_FLOW_THRESHOLD
        )
        self.confidence_decay = self.config.get("confidence_decay", 0.9)

    def calculate_directional_consistency(
        self,
        flow_directions: dict[str, str],
        outcome: str,
        adjacent_outcomes: list[str],
    ) -> float:
        """
        Calculate directional consistency for an outcome.

        Directional consistency is the proportion of adjacent outcomes
        in the same direction that have positive/upward flow.

        Args:
            flow_directions: Map of outcome -> direction (upward/downward/stable)
            outcome: The outcome to analyze
            adjacent_outcomes: List of adjacent outcomes

        Returns:
            Consistency score between 0.0 and 1.0
        """
        if not adjacent_outcomes:
            return 0.0

        outcome_direction = flow_directions.get(outcome, "neutral")
        
        # Count adjacent with same or supportive direction
        consistent_count = 0
        for adj in adjacent_outcomes:
            adj_direction = flow_directions.get(adj, "neutral")
            
            if outcome_direction == "positive":
                # Positive is supported by positive or slight neutral drift
                if adj_direction in ("positive", "neutral"):
                    consistent_count += 1
            elif outcome_direction == "negative":
                # Negative is supported by negative or neutral
                if adj_direction in ("negative", "neutral"):
                    consistent_count += 1
            else:
                # Neutral is supported by neutral
                if adj_direction == "neutral":
                    consistent_count += 1

        return consistent_count / len(adjacent_outcomes)

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

        This is based on the intuition that long-shots have more room
        for probability flow to "amplify" them.

        Args:
            outcome: The outcome to analyze
            outcome_probabilities: All outcome probabilities
            direction_outcomes: Outcomes in the same direction

        Returns:
            Normalized gradient position between 0.0 and 1.0
        """
        if outcome not in outcome_probabilities:
            return 0.0

        direction_probs = [
            outcome_probabilities.get(o, 0) for o in direction_outcomes
        ]

        if not direction_probs or max(direction_probs) == 0:
            return 0.5

        max_prob = max(direction_probs)
        min_prob = min(direction_probs)

        if max_prob == min_prob:
            return 0.5

        # Invert: lower probability = higher position = more amplification potential
        outcome_prob = outcome_probabilities[outcome]
        position = (max_prob - outcome_prob) / (max_prob - min_prob)

        return position

    def calculate_market_momentum(
        self,
        outcome: str,
        flow_pp: float,
        adjacent_flows: list[tuple[str, float]],
        outcome_probabilities: dict[str, float],
    ) -> float:
        """
        Calculate cross-market momentum factor.

        This factor captures whether the flow in adjacent outcomes
        is reinforcing or conflicting with the primary flow.

        Args:
            outcome: The outcome to analyze
            flow_pp: The base flow for this outcome
            adjacent_flows: List of (outcome, flow_pp) for adjacent outcomes
            outcome_probabilities: All outcome probabilities

        Returns:
            Momentum multiplier (typically 0.5 to 1.5)
        """
        if not adjacent_flows:
            return 1.0

        # Check consistency of flow direction
        momentum_sum = 0.0
        for adj_outcome, adj_flow in adjacent_flows:
            # Weighted by probability (higher prob = more influence)
            weight = outcome_probabilities.get(adj_outcome, 0.1)
            
            # Sign indicates same or opposite direction
            sign = 1.0 if (flow_pp >= 0) == (adj_flow >= 0) else -1.0
            momentum_sum += sign * abs(adj_flow) * weight

        # Normalize to 0.5-1.5 range
        avg_momentum = momentum_sum / len(adjacent_flows) if adjacent_flows else 0.0
        
        # Map to multiplier
        if avg_momentum > 3.0:
            return 1.5
        elif avg_momentum > 1.0:
            return 1.3
        elif avg_momentum > 0:
            return 1.1
        elif avg_momentum > -1.0:
            return 0.9
        else:
            return 0.7

    def calculate_propagation_depth(
        self,
        outcome: str,
        flow_pp: float,
        direction: str,
        gradient_graph: GradientGraph,
        flow_directions: dict[str, str],
        visited: Optional[set[str]] = None,
        max_depth: int = 3,
    ) -> tuple[int, list[tuple[str, float]]]:
        """
        Calculate how deep the flow can propagate through the gradient.

        Uses BFS to find all outcomes that would receive flow.

        Args:
            outcome: Starting outcome
            flow_pp: Flow at starting point
            direction: Flow direction
            gradient_graph: The gradient graph
            flow_directions: Map of outcome -> direction
            visited: Set of already visited outcomes
            max_depth: Maximum propagation depth

        Returns:
            Tuple of (max_depth_reached, list of (outcome, signal_strength))
        """
        if visited is None:
            visited = set()

        if outcome in visited or max_depth <= 0:
            return 0, []

        visited.add(outcome)
        adjacent = gradient_graph.get_adjacent_outcomes(outcome)
        
        depth = 0
        signals = []
        
        for adj_outcome in adjacent:
            if adj_outcome in visited:
                continue
                
            adj_direction = flow_directions.get(adj_outcome, "neutral")
            
            # Check if flow would propagate (same or supporting direction)
            if direction == "positive" and adj_direction in ("positive", "neutral"):
                depth = 1
                # Signal strength decays with distance
                signals.append((adj_outcome, flow_pp * 0.7))
            elif direction == "negative" and adj_direction in ("negative", "neutral"):
                depth = 1
                signals.append((adj_outcome, flow_pp * 0.7))
        
        return depth, signals

    def classify_amplification_level(self, score: float) -> AmplificationLevel:
        """
        Classify amplification score into a level.

        Args:
            score: The amplification score

        Returns:
            AmplificationLevel classification
        """
        if score < self.THRESHOLD_LOW:
            return AmplificationLevel.NONE
        elif score < self.THRESHOLD_MEDIUM:
            return AmplificationLevel.LOW
        elif score < self.THRESHOLD_HIGH:
            return AmplificationLevel.MEDIUM
        elif score < self.THRESHOLD_VERY_HIGH:
            return AmplificationLevel.HIGH
        elif score < self.THRESHOLD_EXCEPTIONAL:
            return AmplificationLevel.VERY_HIGH
        else:
            return AmplificationLevel.EXCEPTIONAL

    def calculate_amplification(
        self,
        flow_report,  # FlowReport from probability_engine
        outcome_probabilities: dict[str, float],
        gradient_graph: Optional[GradientGraph] = None,
        confidence_modifiers: Optional[dict[str, float]] = None,
    ) -> AmplificationReport:
        """
        Calculate amplification effect for all outcomes.

        Amplification_Score = Base_Flow × Directional_Consistency × 
                              Gradient_Position × Market_Momentum

        Args:
            flow_report: Flow analysis report from ProbabilityEngine
            outcome_probabilities: Current true probabilities
            gradient_graph: Optional gradient graph for propagation analysis
            confidence_modifiers: Optional confidence adjustments from domain awareness

        Returns:
            AmplificationReport with all results
        """
        # Build default gradient if not provided
        if gradient_graph is None:
            gradient_graph = GradientGraph.build_correct_score_gradient()

        confidence_modifiers = confidence_modifiers or {}

        # Build flow direction map
        flow_directions = {
            f.outcome: f.direction.value 
            for f in flow_report.flows
        }

        amplifications = []

        for flow_result in flow_report.flows:
            outcome = flow_result.outcome
            base_flow = flow_result.flow_pp

            # Skip if base flow below threshold
            if abs(base_flow) < self.min_base_flow:
                amplifications.append(
                    AmplificationResult(
                        outcome=outcome,
                        base_flow_pp=base_flow,
                        directional_consistency=0.0,
                        gradient_position=0.0,
                        market_momentum=1.0,
                        amplification_score=0.0,
                        level=AmplificationLevel.NONE,
                        confidence=confidence_modifiers.get(outcome, 1.0),
                        propagation_depth=0,
                        adjacent_signals=[],
                    )
                )
                continue

            # Get adjacent outcomes from gradient graph
            adjacent = gradient_graph.get_adjacent_outcomes(outcome)

            # Calculate components
            directional_consistency = self.calculate_directional_consistency(
                flow_directions, outcome, adjacent
            )

            # Get all outcomes in same direction for gradient position
            direction_outcomes = [
                o for o, d in flow_directions.items() 
                if d == flow_result.direction.value
            ]
            
            gradient_position = self.calculate_gradient_position(
                outcome, outcome_probabilities, direction_outcomes
            )

            # Calculate adjacent flows for momentum
            adjacent_flows = [
                (f.outcome, f.flow_pp) 
                for f in flow_report.flows 
                if f.outcome in adjacent
            ]

            market_momentum = self.calculate_market_momentum(
                outcome, base_flow, adjacent_flows, outcome_probabilities
            )

            # Calculate amplification score
            if flow_result.direction.value == "positive":
                # Only positive flows get amplified
                amplification_score = (
                    base_flow * 
                    directional_consistency * 
                    (1 + gradient_position) * 
                    market_momentum
                )
            else:
                amplification_score = 0.0

            # Classify level
            level = self.classify_amplification_level(amplification_score)

            # Calculate propagation depth
            propagation_depth, adjacent_signals = self.calculate_propagation_depth(
                outcome,
                base_flow,
                flow_result.direction.value,
                gradient_graph,
                flow_directions,
            )

            # Apply domain confidence
            confidence = confidence_modifiers.get(outcome, 1.0)
            adjusted_score = amplification_score * confidence

            amplifications.append(
                AmplificationResult(
                    outcome=outcome,
                    base_flow_pp=base_flow,
                    directional_consistency=directional_consistency,
                    gradient_position=gradient_position,
                    market_momentum=market_momentum,
                    amplification_score=adjusted_score,
                    level=level,
                    confidence=confidence,
                    propagation_depth=propagation_depth,
                    adjacent_signals=adjacent_signals,
                )
            )

        # Calculate aggregate momentum
        aggregate_momentum = sum(
            a.amplification_score for a in amplifications
        ) / max(len(amplifications), 1)

        # Calculate cascade risk (high momentum with low consistency = risky)
        high_momentum = [a for a in amplifications if a.amplification_score > 5.0]
        cascade_risk = 0.0
        for amp in high_momentum:
            if amp.directional_consistency < 0.5:
                cascade_risk += 0.2

        return AmplificationReport(
            match_id=flow_report.match_id,
            outcomes=[a.outcome for a in amplifications],
            amplifications=amplifications,
            aggregate_momentum=aggregate_momentum,
            market_cascade_risk=min(cascade_risk, 1.0),
        )


__all__ = [
    "AmplificationLevel",
    "GradientEdge",
    "GradientGraph",
    "AmplificationResult",
    "AmplificationReport",
    "FlowAmplificationEngine",
]

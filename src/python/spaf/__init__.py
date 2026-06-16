"""
SPAF - Sports Analytics Framework

A comprehensive domain-aware, situational-awareness-driven, probability-flow-based
sports analytics optimization system.

For academic research and educational purposes only.

Example:
    >>> from spaf import ProbabilityEngine, FlowAmplificationEngine, DomainAwarenessSystem
    >>>
    >>> # Initialize engines
    >>> engine = ProbabilityEngine()
    >>> amplifier = FlowAmplificationEngine()
    >>> awareness = DomainAwarenessSystem()
    >>>
    >>> # Calculate true probability
    >>> result = engine.calculate_true_probability({
    ...     'home': 1.50,
    ...     'draw': 4.20,
    ...     'away': 6.00
    ... })
    >>> print(result.true_probabilities)
"""

from .probability_engine import (
    MarketType,
    FlowDirection,
    IntelligenceSource,
    ProbabilitySnapshot,
    TrueProbabilityResult,
    BayesianPrior,
    BayesianPosterior,
    FlowResult,
    FlowReport,
    EloRating,
    ProbabilityEngine,
)

from .flow_amplification import (
    AmplificationLevel,
    GradientEdge,
    GradientGraph,
    AmplificationResult,
    AmplificationReport,
    FlowAmplificationEngine,
)

from .domain_awareness import (
    IntelligenceWeight,
    ConfidenceLevel,
    IntelligenceRecord,
    TeamIntelligence,
    MatchIntelligence,
    DomainAwarenessReport,
    DomainAwarenessSystem,
)

from .strategy_engine import (
    RiskLevel,
    ValidationResult,
    StrategySelection,
    Strategy,
    StrategyBundle,
    StrategyEngine,
)

__version__ = "4.2.0"
__author__ = "SPAF Team"
__license__ = "MIT"

__all__ = [
    # Probability Engine
    "MarketType",
    "FlowDirection",
    "IntelligenceSource",
    "ProbabilitySnapshot",
    "TrueProbabilityResult",
    "BayesianPrior",
    "BayesianPosterior",
    "FlowResult",
    "FlowReport",
    "EloRating",
    "ProbabilityEngine",
    # Flow Amplification
    "AmplificationLevel",
    "GradientEdge",
    "GradientGraph",
    "AmplificationResult",
    "AmplificationReport",
    "FlowAmplificationEngine",
    # Domain Awareness
    "IntelligenceWeight",
    "ConfidenceLevel",
    "IntelligenceRecord",
    "TeamIntelligence",
    "MatchIntelligence",
    "DomainAwarenessReport",
    "DomainAwarenessSystem",
    # Strategy Engine
    "RiskLevel",
    "ValidationResult",
    "StrategySelection",
    "Strategy",
    "StrategyBundle",
    "StrategyEngine",
]

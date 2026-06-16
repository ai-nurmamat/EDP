"""
Expected Domain Perception
期望域感知法

A Methodology for Asymmetric Expected Value Discovery Based on Probability Flow and Domain Awareness
基于概率流向与全域感知的非对称期望值优势发现方法论

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

from .value_betting import (
    ValueClassification,
    OutcomeCategory,
    ValueMetrics,
    ValueOpportunity,
    ValuePortfolio,
    ValueAssessmentEngine,
)

__version__ = "1.0.0"
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
    # Value Assessment
    "ValueClassification",
    "OutcomeCategory",
    "ValueMetrics",
    "ValueOpportunity",
    "ValuePortfolio",
    "ValueAssessmentEngine",
]

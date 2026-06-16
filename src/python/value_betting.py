"""
SPAF - Sports Analytics Framework
Value Assessment Module - Probability Philosophy Core

This module implements the core probability philosophy of the SPAF framework:
- NOT researching the most likely outcome (lowest odds)
- BUT identifying outcomes with positive Expected Value (EV)
- The key: Multiple failures + One success = Overall profit

Academic Foundation:
- Kelly Criterion (Kelly, 1956) - EV maximization
- Value Assessment Theory - Market inefficiency identification
- Power Law Distribution - Few successes cover many failures
- Prospect Theory (Kahneman & Tversky, 1979) - Risk asymmetry

⚠️ ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional
import math


class ValueClassification(Enum):
    """Classification of value based on EV analysis."""

    EXCEPTIONAL = "exceptional"  # High value opportunity
    HIGH = "high"              # Significant value
    MODERATE = "moderate"      # Moderate value
    FAIR = "fair"             # Market fair pricing
    POOR = "poor"             # Below market value


class OutcomeCategory(Enum):
    """Category of outcome based on market probability."""

    FAVORITE = "favorite"      # High probability (> 60%)
    BALANCED = "balanced"      # Medium probability (30-60%)
    UNDERDOG = "underdog"      # Low probability (< 30%)
    LONG_SHOT = "long_shot"   # Very low probability (< 10%)


@dataclass
class ValueMetrics:
    """
    Comprehensive metrics for value assessment analysis.

    Core Philosophy:
    - We DON'T research lowest odds (most likely)
    - We DO assess outcomes where: Market_Odds > Fair_Odds
    - The "value" comes from market inefficiency identification
    """

    outcome: str

    # Market data
    market_odds: float
    implied_probability: float  # 1/market_odds

    # Our assessment
    assessed_probability: float  # From Domain Awareness System
    assessed_odds: float  # Fair odds based on assessment

    # Value analysis
    value_ratio: float  # market_odds / assessed_odds
    expected_value: float  # EV per unit allocated
    kelly_fraction: float  # Recommended allocation fraction (Kelly criterion)

    # Probability category
    outcome_category: OutcomeCategory

    # Classification
    value_classification: ValueClassification

    # Supporting signals
    flow_direction: str = "stable"
    amplification_score: float = 0.0
    intelligence_confidence: float = 0.5

    @property
    def has_positive_ev(self) -> bool:
        """Check if this outcome has positive expected value."""
        return self.expected_value > 0

    @property
    def is_value_opportunity(self) -> bool:
        """Check if this is a valid value opportunity (positive EV + reasonable confidence)."""
        return self.has_positive_ev and self.value_ratio > 1.1

    @property
    def risk_reward_ratio(self) -> float:
        """Calculate risk-reward ratio for this opportunity."""
        if self.assessed_probability == 0:
            return float('inf')
        return (1 - self.assessed_probability) / self.assessed_probability

    def get_allocation_fraction(self, bankroll: float, fraction_type: str = "half_kelly") -> float:
        """
        Calculate recommended allocation using Kelly criterion variants.

        Kelly Formula: f* = (p × b - q) / b
        Where:
        - f* = fraction of bankroll to allocate
        - p = probability of success
        - q = probability of failure (1-p)
        - b = odds received (profit/1 unit allocated)

        Args:
            bankroll: Total available capital
            fraction_type: 'kelly' (full), 'half_kelly' (50%), 'quarter_kelly' (25%)

        Returns:
            Recommended allocation amount
        """
        p = self.assessed_probability
        b = self.market_odds - 1  # Net odds
        q = 1 - p

        # Kelly fraction
        if b <= 0:
            kelly = 0
        else:
            kelly = (p * b - q) / b

        # Apply Kelly variants
        if fraction_type == "full_kelly":
            fraction = kelly
        elif fraction_type == "half_kelly":
            fraction = kelly / 2
        elif fraction_type == "quarter_kelly":
            fraction = kelly / 4
        else:
            fraction = kelly / 2  # Default to half Kelly

        # Calculate allocation
        allocation = bankroll * max(fraction, 0)

        return allocation


@dataclass
class ValueOpportunity:
    """
    A single value opportunity recommendation.

    Key Principle:
    - NOT: Research lowest odds (most likely to succeed)
    - BUT: Identify highest value (positive EV)
    """

    outcome: str
    market: str
    match_id: str

    # Core metrics
    market_odds: float
    assessed_probability: float
    expected_value: float
    value_classification: ValueClassification

    # Risk management
    recommended_allocation: float
    kelly_fraction: float

    # Confidence signals
    flow_confidence: float
    intelligence_confidence: float
    combined_confidence: float

    # Academic justification
    justification: str = ""

    def __post_init__(self):
        """Generate academic justification based on metrics."""
        if not self.justification:
            self.justification = self._generate_justification()

    def _generate_justification(self) -> str:
        """Generate academic justification for this value opportunity."""
        parts = []

        # Value statement
        if self.value_classification == ValueClassification.EXCEPTIONAL:
            parts.append(f"Exceptionally mispriced: Market offers {self.market_odds:.2f} for outcome estimated at {1/self.assessed_probability:.2f}.")
        elif self.value_classification == ValueClassification.HIGH:
            parts.append(f"Significant value: Market odds {self.market_odds:.2f} exceed fair odds {1/self.assessed_probability:.2f}.")

        # Probability context
        if self.assessed_probability < 0.3:
            parts.append(f"Low probability event ({self.assessed_probability:.1%}) but compensated by high odds.")
        elif self.assessed_probability < 0.5:
            parts.append(f"Moderate probability ({self.assessed_probability:.1%}) with favorable odds.")
        else:
            parts.append(f"High probability ({self.assessed_probability:.1%}) with value premium.")

        # EV statement
        parts.append(f"Expected Value: {self.expected_value:.2f} per unit (positive EV = mathematical edge).")

        # Strategy context
        parts.append(f"Multiple such opportunities: N failures covered by 1 success (Power Law distribution).")

        return " ".join(parts)


@dataclass
class ValuePortfolio:
    """
    A portfolio of value opportunities implementing the "multiple trials, one success" philosophy.

    Core Philosophy:
    - We identify many value opportunities across different events
    - Most will fail (this is expected and budgeted)
    - Few successes will cover all failures + generate profit
    - Key: The VALUE (positive EV) in each opportunity guarantees long-term profitability
    """

    opportunities: list[ValueOpportunity] = field(default_factory=list)

    # Portfolio parameters
    total_bankroll: float
    allocation_fraction: float = 0.05  # 5% of bankroll per opportunity (Kelly-based)

    # Statistics
    created_at: datetime = field(default_factory=datetime.now)

    # Metadata
    min_value_ratio: float = 1.15  # Minimum value_ratio to include
    min_ev: float = 0.05  # Minimum positive EV threshold

    def calculate_portfolio_ev(self) -> float:
        """
        Calculate total portfolio Expected Value.

        This is the KEY metric: Even if most fail,
        the total EV of the portfolio determines long-term profitability.
        """
        if not self.opportunities:
            return 0.0

        total_ev = sum(o.expected_value * o.recommended_allocation for o in self.opportunities)
        return total_ev

    def get_expected_outcomes(self, success_rate: float) -> dict[str, Any]:
        """
        Calculate expected outcomes based on assumed success rate.

        This demonstrates the "multiple failures, one success" model:
        - If success_rate = 20% (5 events succeed on average)
        - And we have 20 opportunities
        - Then ~4 succeed, ~16 fail

        Args:
            success_rate: Expected success rate (typically low)

        Returns:
            Dictionary with expected results
        """
        n_opportunities = len(self.opportunities)
        expected_successes = n_opportunities * success_rate
        expected_failures = n_opportunities * (1 - success_rate)

        # Calculate returns
        successes = [o for o in self.opportunities if o.market_odds > 1]
        failures = [o for o in self.opportunities]

        total_potential_wins = sum(o.market_odds * o.recommended_allocation for o in successes)
        total_allocated = sum(o.recommended_allocation for o in self.opportunities)

        # Expected outcome
        expected_profit = (expected_successes * total_potential_wins / max(n_opportunities, 1)) - total_allocated

        return {
            "total_opportunities": n_opportunities,
            "expected_successes": expected_successes,
            "expected_failures": expected_failures,
            "success_rate": success_rate,
            "total_allocated": total_allocated,
            "expected_profit": expected_profit,
            "roi": expected_profit / total_allocated if total_allocated > 0 else 0,
        }

    def get_risk_analysis(self) -> dict[str, Any]:
        """
        Analyze portfolio risk using probability theory.

        Based on Power Law: Few big successes > Many small failures
        """
        if not self.opportunities:
            return {"risk_level": "none"}

        # Sort by value
        sorted_opportunities = sorted(self.opportunities, key=lambda x: x.value_ratio, reverse=True)

        # Calculate loss scenarios
        total_allocated = sum(o.recommended_allocation for o in self.opportunities)
        max_loss = total_allocated  # If ALL fail

        # Calculate potential successes
        top_values = sorted_opportunities[:3]  # Top 3 value opportunities
        best_case_wins = sum(o.market_odds * o.recommended_allocation for o in top_values)
        best_case_profit = best_case_wins - total_allocated

        # Risk classification
        if best_case_profit > total_allocated * 3:
            risk_level = "HIGH_POTENTIAL"
        elif best_case_profit > total_allocated:
            risk_level = "MODERATE_POTENTIAL"
        else:
            risk_level = "LOW_POTENTIAL"

        return {
            "risk_level": risk_level,
            "max_loss": max_loss,
            "best_case_profit": best_case_profit,
            "best_case_roi": best_case_profit / total_allocated if total_allocated > 0 else 0,
            "top_value_opportunities": [o.outcome for o in top_values],
            "concentration_risk": len(top_values) / len(self.opportunities) if self.opportunities else 0,
        }


class ValueAssessmentEngine:
    """
    Core engine implementing the Value Assessment Philosophy.

    DIFFERENT FROM TRADITIONAL APPROACH:
    ┌─────────────────────────────────────────────────────────────────┐
    │  TRADITIONAL (❌)          │  VALUE ASSESSMENT (✅ SPAF)        │
    ├─────────────────────────────────────────────────────────────────┤
    │  Research lowest odds        │  Identify highest EV               │
    │  (most likely to succeed)    │  (best expected return)           │
    │                             │                                   │
    │  High success rate           │  Low success rate, high returns    │
    │  Many small wins             │  Few big wins cover failures      │
    │  Guaranteed long-term loss    │  Mathematical long-term edge     │
    └─────────────────────────────────────────────────────────────────┘

    Core Formula:
    EV = P(success) × (Odds - 1) - P(failure) × 1
    Value exists when: Market_Odds > Fair_Odds (EV > 0)

    Example:
    - Market offers 8.0 odds for an outcome we assess at 15% probability
    - Fair odds = 1/0.15 = 6.67
    - Value Ratio = 8.0 / 6.67 = 1.20 (> 1.0 = VALUE!)
    - EV = 0.15 × 7 - 0.85 × 1 = 0.20 per unit (positive!)

    Even with only 15% success rate, this opportunity is profitable in the long run.
    The key: IDENTIFY MANY SUCH OPPORTUNITIES, and the positive EV compounds.

    ⚠️ ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY
    """

    # Value classification thresholds
    THRESHOLD_EXCEPTIONAL = 1.30
    THRESHOLD_HIGH = 1.20
    THRESHOLD_MODERATE = 1.10
    THRESHOLD_FAIR = 1.00

    # Probability category thresholds
    THRESHOLD_FAVORITE = 0.60
    THRESHOLD_BALANCED = 0.30
    THRESHOLD_UNDERDOG = 0.10

    def __init__(self, config: Optional[dict[str, Any]] = None):
        """
        Initialize the Value Assessment Engine.

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.min_value_ratio = self.config.get("min_value_ratio", 1.15)
        self.min_ev = self.config.get("min_ev", 0.05)
        self.use_kelly = self.config.get("use_kelly", True)

    def calculate_value_metrics(
        self,
        outcome: str,
        market_odds: float,
        assessed_probability: float,
        flow_confidence: float = 0.5,
        intelligence_confidence: float = 0.5,
    ) -> ValueMetrics:
        """
        Calculate comprehensive value metrics for an opportunity.

        Args:
            outcome: Name of the outcome
            market_odds: Market decimal odds
            assessed_probability: Our assessed true probability (0-1)
            flow_confidence: Confidence from probability flow analysis
            intelligence_confidence: Confidence from domain awareness

        Returns:
            ValueMetrics with comprehensive analysis
        """
        # Implied probability from market odds
        implied_probability = 1.0 / market_odds

        # Fair odds based on our assessment
        assessed_odds = 1.0 / assessed_probability if assessed_probability > 0 else float('inf')

        # Value ratio: How much value exists
        value_ratio = market_odds / assessed_odds if assessed_odds > 0 else 0

        # Expected Value calculation
        ev = assessed_probability * (market_odds - 1) - (1 - assessed_probability) * 1

        # Kelly fraction
        if market_odds > 1:
            b = market_odds - 1
            p = assessed_probability
            q = 1 - p
            kelly = max((p * b - q) / b, 0) if b > 0 else 0
        else:
            kelly = 0

        # Classify outcome
        if implied_probability >= self.THRESHOLD_FAVORITE:
            category = OutcomeCategory.FAVORITE
        elif implied_probability >= self.THRESHOLD_BALANCED:
            category = OutcomeCategory.BALANCED
        elif implied_probability >= self.THRESHOLD_UNDERDOG:
            category = OutcomeCategory.UNDERDOG
        else:
            category = OutcomeCategory.LONG_SHOT

        # Classify value
        if value_ratio >= self.THRESHOLD_EXCEPTIONAL:
            classification = ValueClassification.EXCEPTIONAL
        elif value_ratio >= self.THRESHOLD_HIGH:
            classification = ValueClassification.HIGH
        elif value_ratio >= self.THRESHOLD_MODERATE:
            classification = ValueClassification.MODERATE
        elif value_ratio >= self.THRESHOLD_FAIR:
            classification = ValueClassification.FAIR
        else:
            classification = ValueClassification.POOR

        return ValueMetrics(
            outcome=outcome,
            market_odds=market_odds,
            implied_probability=implied_probability,
            assessed_probability=assessed_probability,
            assessed_odds=assessed_odds,
            value_ratio=value_ratio,
            expected_value=ev,
            kelly_fraction=kelly,
            outcome_category=category,
            value_classification=classification,
            flow_direction="positive" if flow_confidence > 0.6 else "neutral",
            amplification_score=0,
            intelligence_confidence=intelligence_confidence,
        )

    def identify_value_opportunities(
        self,
        market_odds: dict[str, float],
        assessed_probabilities: dict[str, float],
        flow_confidences: Optional[dict[str, float]] = None,
        intelligence_confidences: Optional[dict[str, float]] = None,
    ) -> list[ValueOpportunity]:
        """
        Identify value opportunities from market odds and assessments.

        This is the CORE METHOD of the Value Assessment Philosophy:
        1. Get market odds for all outcomes
        2. Get our assessed probabilities (from Domain Awareness)
        3. Calculate value for EACH outcome
        4. Select the ones with HIGHEST VALUE (not highest probability)

        Args:
            market_odds: Dictionary of outcome -> market odds
            assessed_probabilities: Dictionary of outcome -> our assessed probability
            flow_confidences: Optional confidence from flow analysis
            intelligence_confidences: Optional confidence from domain awareness

        Returns:
            List of ValueOpportunity recommendations, sorted by value (highest first)
        """
        flow_confidences = flow_confidences or {k: 0.5 for k in market_odds}
        intelligence_confidences = intelligence_confidences or {k: 0.5 for k in market_odds}

        value_opportunities = []

        for outcome, odds in market_odds.items():
            prob = assessed_probabilities.get(outcome, 0.33)
            flow_conf = flow_confidences.get(outcome, 0.5)
            intel_conf = intelligence_confidences.get(outcome, 0.5)

            # Calculate value metrics
            metrics = self.calculate_value_metrics(
                outcome=outcome,
                market_odds=odds,
                assessed_probability=prob,
                flow_confidence=flow_conf,
                intelligence_confidence=intel_conf,
            )

            # Skip if not positive EV or below threshold
            if metrics.expected_value <= self.min_ev:
                continue
            if metrics.value_ratio < self.min_value_ratio:
                continue

            # Calculate recommended allocation (using Kelly)
            recommended_allocation = metrics.get_allocation_fraction(
                bankroll=1000,  # Would be passed from portfolio
                fraction_type="half_kelly"
            )

            # Combined confidence
            combined_conf = (flow_conf + intel_conf) / 2

            opportunity = ValueOpportunity(
                outcome=outcome,
                market="1X2",  # Default market
                match_id="unknown",
                market_odds=odds,
                assessed_probability=prob,
                expected_value=metrics.expected_value,
                value_classification=metrics.value_classification,
                recommended_allocation=recommended_allocation,
                kelly_fraction=metrics.kelly_fraction,
                flow_confidence=flow_conf,
                intelligence_confidence=intel_conf,
                combined_confidence=combined_conf,
            )

            value_opportunities.append(opportunity)

        # Sort by value ratio (HIGHEST VALUE FIRST, not highest probability!)
        value_opportunities.sort(key=lambda x: x.value_ratio, reverse=True)

        return value_opportunities

    def calculate_portfolio_recommendations(
        self,
        value_opportunities: list[ValueOpportunity],
        total_bankroll: float,
        max_opportunities_per_event: int = 3,
    ) -> ValuePortfolio:
        """
        Create a value portfolio implementing the "multiple trials" philosophy.

        Key Principle:
        - We want DIVERSIFIED value opportunities
        - Each opportunity has positive EV individually
        - Combined, they form a portfolio with positive expected return
        - Even if many fail, the successes cover all failures + profit

        Args:
            value_opportunities: List of identified value opportunities
            total_bankroll: Total available capital
            max_opportunities_per_event: Maximum opportunities per match/event

        Returns:
            ValuePortfolio with optimized allocation
        """
        # Group by match
        match_opportunities = {}
        for opp in value_opportunities:
            if opp.match_id not in match_opportunities:
                match_opportunities[opp.match_id] = []
            if len(match_opportunities[opp.match_id]) < max_opportunities_per_event:
                match_opportunities[opp.match_id].append(opp)

        # Flatten back
        selected_opportunities = []
        for opps in match_opportunities.values():
            selected_opportunities.extend(opps)

        # Calculate allocations based on value ratio
        total_value = sum(o.value_ratio for o in selected_opportunities)

        for opp in selected_opportunities:
            # Proportional allocation based on value
            proportion = opp.value_ratio / total_value if total_value > 0 else 0
            base_allocation = total_bankroll * self.allocation_fraction
            opp.recommended_allocation = base_allocation * proportion * (opp.value_ratio / 1.2)

        portfolio = ValuePortfolio(
            opportunities=selected_opportunities,
            total_bankroll=total_bankroll,
            allocation_fraction=self.allocation_fraction,
        )

        return portfolio

    def explain_value_philosophy(self) -> str:
        """
        Generate academic explanation of the Value Assessment Philosophy.

        Returns:
            Formatted explanation of the probability philosophy
        """
        explanation = """
================================================================================
SPAF VALUE ASSESSMENT PHILOSOPHY - Academic Explanation
================================================================================

CORE PRINCIPLE:
┌──────────────────────────────────────────────────────────────────────────────┐
│  We do NOT research the outcome most likely to happen (lowest odds).          │
│  We DO assess outcomes where: Market_Odds > Fair_Odds (Positive EV).         │
│                                                                               │
│  The KEY: Even if we fail 80% of the time, the 20% that succeed generate     │
│  enough profit to cover all failures AND generate additional profit.          │
└──────────────────────────────────────────────────────────────────────────────┘

MATHEMATICAL FOUNDATION:
────────────────────────────────────────────────────────────────────────────────
Expected Value (EV) = P(success) × (Odds - 1) - P(failure) × 1

Example:
• Market offers 8.0 odds for outcome A
• Our assessment: P(A) = 15% (0.15)
• Implied by market: P(A) = 12.5% (1/8.0)
• Market underestimates → VALUE EXISTS!

EV = 0.15 × 7 - 0.85 × 1 = 1.05 - 0.85 = +0.20 per unit allocated

Even succeeding only 15% of the time, this opportunity is profitable in the long run!

THE "N TRIALS, 1 SUCCESS" MODEL:
────────────────────────────────────────────────────────────────────────────────
If we identify 20 such opportunities at average odds of 8.0 with 5% allocation each:

Expected outcomes (based on 15% true probability):
• Successes: 20 × 15% = 3 opportunities
• Failures: 20 × 85% = 17 opportunities

If 3 succeed at 8.0 odds:
• Profit from successes: 3 × 5% × 8.0 = 120% of bankroll
• Loss from 17 failures: 17 × 5% = 85% of bankroll
• Net profit: 120% - 85% = +35% of bankroll!

The power law: Few extreme successes > many small failures.

ACADEMIC SUPPORT:
────────────────────────────────────────────────────────────────────────────────
• Kelly Criterion (Kelly, 1956): Maximize log wealth growth
• Value Assessment Theory: Market inefficiency identification
• Prospect Theory (Kahneman & Tversky, 1979): Risk asymmetry
• Power Law Distribution: Extreme event statistics

IMPLEMENTATION IN SPAF:
────────────────────────────────────────────────────────────────────────────────
1. Domain Awareness System → Assesses TRUE probability of events
2. Value Assessment Engine → Compares Market_Odds vs Fair_Odds
3. Value Portfolio → Diversifies across multiple value opportunities
4. Risk Management → Kelly-based allocation sizing

KEY METRICS:
• Value Ratio = Market_Odds / Fair_Odds (>1 = value)
• Expected Value (EV) = Positive indicates mathematical edge
• Kelly Fraction = Optimal allocation size for long-term growth

⚠️ DISCLAIMER: This framework is for ACADEMIC RESEARCH only.
================================================================================
"""
        return explanation


__all__ = [
    "ValueClassification",
    "OutcomeCategory",
    "ValueMetrics",
    "ValueOpportunity",
    "ValuePortfolio",
    "ValueAssessmentEngine",
]

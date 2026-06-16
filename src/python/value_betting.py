"""
SPAF - Sports Analytics Framework
Value Betting Module - Probability Philosophy Core

This module implements the core probability philosophy of the SPAF framework:
- NOT betting on the most likely outcome (lowest odds)
- BUT betting on outcomes with positive Expected Value (EV)
- The key: Multiple small losses + One big win = Overall profit

Academic Foundation:
- Kelly Criterion (Kelly, 1956) - EV maximization
- Value Betting Theory - Odds inefficiency exploitation
- Power Law Distribution - Few big wins cover many small losses
- Prospect Theory (Kahneman & Tversky, 1979) - Risk-seeking in loss domain

⚠️ ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional
import math


class ValueClassification(Enum):
    """Classification of betting value based on EV analysis."""

    # High value: Strong positive EV, rare opportunities
    EXCEPTIONAL = "exceptional"
    # Medium-high value: Good positive EV
    HIGH = "high"
    # Moderate value: Positive but marginal EV
    MODERATE = "moderate"
    # No value: Market efficiently priced
    FAIR = "fair"
    # Negative value: Against the odds
    POOR = "poor"


class OutcomeCategory(Enum):
    """Category of outcome based on market probability."""

    # High probability (market implied prob > 60%)
    FAVORITE = "favorite"
    # Medium probability (30-60%)
    BALANCED = "balanced"
    # Low probability (< 30%)
    UNDERDOG = "underdog"
    # Very low probability (< 10%)
    LONG_SHOT = "long_shot"


@dataclass
class ValueMetrics:
    """
    Comprehensive metrics for value betting analysis.

    Core Philosophy:
    - We DON'T bet on lowest odds (most likely)
    - We DO bet on outcomes where: Market_Odds > Fair_Odds
    - The "value" comes from odds inefficiency
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
    expected_value: float  # EV per unit staked
    kelly_fraction: float  # Recommended stake fraction (Kelly criterion)

    # Probability category
    outcome_category: OutcomeCategory

    # Academic classification
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
    def is_value_bet(self) -> bool:
        """Check if this is a valid value bet (positive EV + reasonable confidence)."""
        return self.has_positive_ev and self.value_ratio > 1.1

    @property
    def risk_reward_ratio(self) -> float:
        """Calculate risk-reward ratio for this bet."""
        if self.assessed_probability == 0:
            return float('inf')
        return (1 - self.assessed_probability) / self.assessed_probability

    def get_stake_fraction(self, bankroll: float, fraction_type: str = "half_kelly") -> float:
        """
        Calculate recommended stake using Kelly criterion variants.

        Kelly Formula: f* = (p × b - q) / b
        Where:
        - f* = fraction of bankroll to bet
        - p = probability of winning
        - q = probability of losing (1-p)
        - b = odds received on bet (profit/1 unit stake)

        Args:
            bankroll: Total available bankroll
            fraction_type: 'kelly' (full), 'half_kelly' (50%), 'quarter_kelly' (25%)

        Returns:
            Recommended stake amount
        """
        p = self.assessed_probability
        b = self.market_odds - 1  # Net odds received
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

        # Calculate stake
        stake = bankroll * max(fraction, 0)

        return stake


@dataclass
class ValueBet:
    """
    A single value bet recommendation.

    Key Principle:
    - NOT: Bet on lowest odds (most likely to win)
    - BUT: Bet on highest value (positive EV)
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
    recommended_stake: float
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
        """Generate academic justification for this value bet."""
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
        parts.append(f"Multiple such bets: N failures covered by 1 success (Power Law distribution).")

        return " ".join(parts)


@dataclass
class ValuePortfolio:
    """
    A portfolio of value bets implementing the "multiple trials, one success" philosophy.

    Core Philosophy:
    - We place many value bets across different events
    - Most will lose (this is expected and budgeted)
    - Few big winners will cover all losses + generate profit
    - Key: The VALUE (positive EV) in each bet guarantees long-term profitability
    """

    bets: list[ValueBet] = field(default_factory=list)

    # Portfolio parameters
    total_bankroll: float
    bet_fraction: float = 0.05  # 5% of bankroll per bet (Kelly-based)

    # Statistics
    created_at: datetime = field(default_factory=datetime.now)

    # Metadata
    min_value_ratio: float = 1.15  # Minimum value_ratio to include bet
    min_ev: float = 0.05  # Minimum positive EV threshold

    def calculate_portfolio_ev(self) -> float:
        """
        Calculate total portfolio Expected Value.

        This is the KEY metric: Even if most bets lose,
        the total EV of the portfolio determines long-term profitability.
        """
        if not self.bets:
            return 0.0

        total_ev = sum(bet.expected_value * bet.recommended_stake for bet in self.bets)
        return total_ev

    def get_expected_outcomes(self, win_rate: float) -> dict[str, Any]:
        """
        Calculate expected outcomes based on assumed win rate.

        This demonstrates the "multiple failures, one success" model:
        - If win_rate = 20% (5 events succeed on average)
        - And we have 20 bets
        - Then ~4 succeed, ~16 lose

        Args:
            win_rate: Expected win rate for value bets (typically low)

        Returns:
            Dictionary with expected results
        """
        n_bets = len(self.bets)
        expected_wins = n_bets * win_rate
        expected_losses = n_bets * (1 - win_rate)

        # Calculate returns
        wins = [b for b in self.bets if b.market_odds > 1]  # All value bets could win
        losses = [b for b in self.bets]

        total_potential_wins = sum(b.market_odds * b.recommended_stake for b in wins)
        total_staked = sum(b.recommended_stake for b in self.bets)

        # Expected outcome
        expected_profit = (expected_wins * total_potential_wins / max(n_bets, 1)) - total_staked

        return {
            "total_bets": n_bets,
            "expected_wins": expected_wins,
            "expected_losses": expected_losses,
            "win_rate": win_rate,
            "total_staked": total_staked,
            "expected_profit": expected_profit,
            "roi": expected_profit / total_staked if total_staked > 0 else 0,
        }

    def get_risk_analysis(self) -> dict[str, Any]:
        """
        Analyze portfolio risk using probability theory.

        Based on Power Law: Few big wins > Many small losses
        """
        if not self.bets:
            return {"risk_level": "none"}

        # Sort by value
        sorted_bets = sorted(self.bets, key=lambda x: x.value_ratio, reverse=True)

        # Calculate loss scenarios
        total_staked = sum(b.recommended_stake for b in self.bets)
        max_loss = total_staked  # If ALL bets lose

        # Calculate potential wins
        top_values = sorted_bets[:3]  # Top 3 value bets
        best_case_wins = sum(b.market_odds * b.recommended_stake for b in top_values)
        best_case_profit = best_case_wins - total_staked

        # Risk classification
        if best_case_profit > total_staked * 3:
            risk_level = "HIGH_POTENTIAL"
        elif best_case_profit > total_staked:
            risk_level = "MODERATE_POTENTIAL"
        else:
            risk_level = "LOW_POTENTIAL"

        return {
            "risk_level": risk_level,
            "max_loss": max_loss,
            "best_case_profit": best_case_profit,
            "best_case_roi": best_case_profit / total_staked if total_staked > 0 else 0,
            "top_value_bets": [b.outcome for b in top_values],
            "concentration_risk": len(top_values) / len(self.bets) if self.bets else 0,
        }


class ValueBettingEngine:
    """
    Core engine implementing the Value Betting Philosophy.

    DIFFERENT FROM TRADITIONAL APPROACH:
    ┌─────────────────────────────────────────────────────────────────┐
    │  TRADITIONAL (❌)          │  VALUE BETTING (✅ SPAF)          │
    ├─────────────────────────────────────────────────────────────────┤
    │  Bet on lowest odds        │  Bet on highest EV                │
    │  (most likely to win)      │  (best expected return)           │
    │                             │                                   │
    │  High win rate             │  Low win rate, high EV            │
    │  Low returns per bet       │  High returns when winning        │
    │  Many small wins           │  Few big wins cover losses        │
    │  Guaranteed long-term loss │  Mathematical long-term edge     │
    └─────────────────────────────────────────────────────────────────┘

    Core Formula:
    EV = P(win) × (Odds - 1) - P(lose) × 1
    Value exists when: Market_Odds > Fair_Odds (EV > 0)

    Example:
    - Market offers 8.0 odds for an outcome we assess at 15% probability
    - Fair odds = 1/0.15 = 6.67
    - Value Ratio = 8.0 / 6.67 = 1.20 (> 1.0 = VALUE!)
    - EV = 0.15 × 7 - 0.85 × 1 = 0.20 per unit (positive!)

    Even with only 15% win rate, this bet is profitable in the long run.
    The key: PLACE MANY SUCH BETS, and the positive EV compounds.

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
        Initialize the Value Betting Engine.

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
        Calculate comprehensive value metrics for a betting opportunity.

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
        # EV = P(win) × (Odds - 1) - P(lose) × 1
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

    def identify_value_bets(
        self,
        market_odds: dict[str, float],
        assessed_probabilities: dict[str, float],
        flow_confidences: Optional[dict[str, float]] = None,
        intelligence_confidences: Optional[dict[str, float]] = None,
    ) -> list[ValueBet]:
        """
        Identify value betting opportunities from market odds and assessments.

        This is the CORE METHOD of the Value Betting Philosophy:
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
            List of ValueBet recommendations, sorted by value (highest first)
        """
        flow_confidences = flow_confidences or {k: 0.5 for k in market_odds}
        intelligence_confidences = intelligence_confidences or {k: 0.5 for k in market_odds}

        value_bets = []

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

            # Calculate recommended stake (using Kelly)
            recommended_stake = metrics.get_stake_fraction(
                bankroll=1000,  # Would be passed from portfolio
                fraction_type="half_kelly"
            )

            # Combined confidence
            combined_conf = (flow_conf + intel_conf) / 2

            bet = ValueBet(
                outcome=outcome,
                market="1X2",  # Default market
                match_id="unknown",
                market_odds=odds,
                assessed_probability=prob,
                expected_value=metrics.expected_value,
                value_classification=metrics.value_classification,
                recommended_stake=recommended_stake,
                kelly_fraction=metrics.kelly_fraction,
                flow_confidence=flow_conf,
                intelligence_confidence=intel_conf,
                combined_confidence=combined_conf,
            )

            value_bets.append(bet)

        # Sort by value ratio (HIGHEST VALUE FIRST, not highest probability!)
        value_bets.sort(key=lambda x: x.value_ratio, reverse=True)

        return value_bets

    def calculate_portfolio_recommendations(
        self,
        value_bets: list[ValueBet],
        total_bankroll: float,
        max_bets_per_event: int = 3,
    ) -> ValuePortfolio:
        """
        Create a value betting portfolio implementing the "multiple trials" philosophy.

        Key Principle:
        - We want DIVERSIFIED value bets
        - Each bet has positive EV individually
        - Combined, they form a portfolio with positive expected return
        - Even if many lose, the winners cover all losses + profit

        Args:
            value_bets: List of identified value bets
            total_bankroll: Total available bankroll
            max_bets_per_event: Maximum bets per match/event

        Returns:
            ValuePortfolio with optimized bet allocation
        """
        # Group by match
        match_bets = {}
        for bet in value_bets:
            if bet.match_id not in match_bets:
                match_bets[bet.match_id] = []
            if len(match_bets[bet.match_id]) < max_bets_per_event:
                match_bets[bet.match_id].append(bet)

        # Flatten back
        selected_bets = []
        for bets in match_bets.values():
            selected_bets.extend(bets)

        # Calculate stakes based on value ratio
        total_value = sum(bet.value_ratio for bet in selected_bets)

        for bet in selected_bets:
            # Proportional allocation based on value
            proportion = bet.value_ratio / total_value if total_value > 0 else 0
            base_stake = total_bankroll * self.bet_fraction
            bet.recommended_stake = base_stake * proportion * (bet.value_ratio / 1.2)

        portfolio = ValuePortfolio(
            bets=selected_bets,
            total_bankroll=total_bankroll,
            bet_fraction=self.bet_fraction,
        )

        return portfolio

    def explain_value_philosophy(self) -> str:
        """
        Generate academic explanation of the Value Betting Philosophy.

        Returns:
            Formatted explanation of the probability philosophy
        """
        explanation = """
================================================================================
SPAF VALUE BETTING PHILOSOPHY - Academic Explanation
================================================================================

CORE PRINCIPLE:
┌──────────────────────────────────────────────────────────────────────────────┐
│  We do NOT bet on the outcome most likely to happen (lowest odds).            │
│  We DO bet on outcomes where: Market_Odds > Fair_Odds (Positive EV).         │
│                                                                               │
│  The KEY: Even if we lose 80% of bets, the 20% that win generate            │
│  enough profit to cover all losses AND generate additional profit.           │
└──────────────────────────────────────────────────────────────────────────────┘

MATHEMATICAL FOUNDATION:
────────────────────────────────────────────────────────────────────────────────
Expected Value (EV) = P(win) × (Odds - 1) - P(lose) × 1

Example:
• Market offers 8.0 odds for outcome A
• Our assessment: P(A) = 15% (0.15)
• Implied by market: P(A) = 12.5% (1/8.0)
• Market underestimates → VALUE EXISTS!

EV = 0.15 × 7 - 0.85 × 1 = 1.05 - 0.85 = +0.20 per unit staked

Even winning only 15% of the time, this bet is profitable in the long run!

THE "N TRIALS, 1 SUCCESS" MODEL:
────────────────────────────────────────────────────────────────────────────────
If we place 20 such bets at average odds of 8.0 with 5% of bankroll each:

Expected outcomes (based on 15% true probability):
• Wins: 20 × 15% = 3 bets
• Losses: 20 × 85% = 17 bets

If 3 bets win at 8.0 odds:
• Profit from wins: 3 × 5% × 8.0 = 120% of bankroll
• Loss from 17 bets: 17 × 5% = 85% of bankroll
• Net profit: 120% - 85% = +35% of bankroll!

The power law: Few big wins (at high odds) cover many small losses.

ACADEMIC SUPPORT:
────────────────────────────────────────────────────────────────────────────────
• Kelly Criterion (Kelly, 1956): Maximize log wealth growth
• Value Betting Theory: Exploit market inefficiencies
• Prospect Theory (Kahneman & Tversky, 1979): Risk-seeking in loss domain
• Power Law Distribution: Few extreme wins > many small losses

IMPLEMENTATION IN SPAF:
────────────────────────────────────────────────────────────────────────────────
1. Domain Awareness System → Assesses TRUE probability of events
2. Value Betting Engine → Compares Market_Odds vs Fair_Odds
3. Value Portfolio → Diversifies across multiple value bets
4. Risk Management → Kelly-based stake sizing

KEY METRICS:
• Value Ratio = Market_Odds / Fair_Odds (>1 = value)
• Expected Value (EV) = Positive indicates mathematical edge
• Kelly Fraction = Optimal stake size for long-term growth

⚠️ DISCLAIMER: This framework is for ACADEMIC RESEARCH only.
================================================================================
"""
        return explanation


__all__ = [
    "ValueClassification",
    "OutcomeCategory",
    "ValueMetrics",
    "ValueBet",
    "ValuePortfolio",
    "ValueBettingEngine",
]

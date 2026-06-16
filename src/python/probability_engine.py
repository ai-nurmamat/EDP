"""
Expected Domain Perception
期望域感知法

Advanced Probability Analysis Engine with Bayesian Inference

This module implements the core probability analysis engine featuring:
- Shin method for implied probability extraction
- Bayesian inference for dynamic probability estimation
- Time series momentum analysis
- Elo-based team strength modeling

A Methodology for Asymmetric Expected Value Discovery Based on Probability Flow and Domain Awareness

⚠️ ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional
import math
from collections import defaultdict


class MarketType(Enum):
    """Supported market types for probability analysis."""

    MATCH_RESULT = "1X2"
    HANDICAP = "handicap"
    TOTAL_GOALS = "total_goals"
    CORRECT_SCORE = "correct_score"
    HALF_FULL = "hf_ft"


class FlowDirection(Enum):
    """Probability flow direction classification."""

    POSITIVE = "positive"  # Market confidence increasing
    NEGATIVE = "negative"  # Market confidence decreasing
    NEUTRAL = "neutral"    # No significant change


class IntelligenceSource(Enum):
    """Sources of domain intelligence."""

    RANKING = "ranking"           # FIFA/official rankings
    HISTORICAL = "historical"      # Historical performance
    RECENT_FORM = "recent_form"   # Recent match results
    TACTICAL = "tactical"         # Tactical analysis
    INJURY = "injury"            # Player availability
    MOTIVATION = "motivation"     # Tournament context
    MARKET = "market"             # Market consensus


@dataclass
class ProbabilitySnapshot:
    """
    A snapshot of implied probabilities at a specific point in time.

    Attributes:
        timestamp: When this snapshot was recorded
        probabilities: Dictionary mapping outcomes to their implied probabilities
        source: Data source identifier
        market_type: Type of market
    """

    timestamp: datetime
    probabilities: dict[str, float]
    source: str = "unknown"
    market_type: MarketType = MarketType.MATCH_RESULT
    confidence: float = 1.0  # Data quality confidence

    def validate(self) -> bool:
        """Validate that probabilities sum to approximately 1.0."""
        total = sum(self.probabilities.values())
        return 0.98 <= total <= 1.02


@dataclass
class TrueProbabilityResult:
    """
    Result of true probability calculation.

    Contains the normalized probabilities after market margin removal,
    along with statistical metadata.
    """

    true_probabilities: dict[str, float]
    implied_probabilities: dict[str, float]
    market_margin: float  # Total market margin percentage
    margin_per_outcome: dict[str, float]  # Per-outcome margin
    method: str = "shin_normalized"
    confidence_interval: Optional[dict[str, tuple[float, float]]] = None

    def get_most_likely_outcome(self) -> tuple[str, float]:
        """Return the outcome with highest true probability."""
        best_outcome = max(self.true_probabilities.items(), key=lambda x: x[1])
        return best_outcome

    def get_probability_ranking(self) -> list[tuple[str, float]]:
        """Return outcomes ranked by probability (descending)."""
        return sorted(
            self.true_probabilities.items(),
            key=lambda x: x[1],
            reverse=True
        )


@dataclass
class BayesianPrior:
    """
    Bayesian prior distribution for probability estimation.

    Attributes:
        alpha: Beta distribution alpha parameter
        beta: Beta distribution beta parameter
        source: Source of prior information
        weight: Weight of this prior in combination
    """

    alpha: float
    beta: float
    source: IntelligenceSource
    weight: float = 1.0

    def to_dict(self) -> dict[str, float]:
        """Convert to dictionary format."""
        return {"alpha": self.alpha, "beta": self.beta, "weight": self.weight}


@dataclass
class BayesianPosterior:
    """
    Bayesian posterior distribution after incorporating evidence.

    Attributes:
        posterior_alpha: Updated alpha parameter
        posterior_beta: Updated beta parameter
        expected_probability: Mean of the posterior
        std_deviation: Standard deviation
        credible_interval: 95% credible interval (lower, upper)
    """

    posterior_alpha: float
    posterior_beta: float
    expected_probability: float
    std_deviation: float
    credible_interval: tuple[float, float]
    update_evidence: dict[str, Any]

    @property
    def variance(self) -> float:
        """Return the variance of the posterior."""
        return self.std_deviation ** 2


@dataclass
class FlowResult:
    """
    Result of probability flow analysis.

    Represents the change in probabilities between two time points,
    with significance assessment and momentum indicators.
    """

    outcome: str
    flow_pp: float  # Flow in percentage points
    direction: FlowDirection
    initial_prob: float
    latest_prob: float
    momentum_score: float  # Time series momentum indicator
    significance: str = "low"  # low, medium, high
    velocity: float = 0.0  # Rate of change
    acceleration: float = 0.0  # Acceleration of change

    def is_significant(self, threshold: float = 2.0) -> bool:
        """Check if flow exceeds significance threshold."""
        return abs(self.flow_pp) >= threshold

    def get_confidence_level(self) -> float:
        """Calculate confidence level based on multiple factors."""
        base_confidence = min(abs(self.flow_pp) / 10.0, 1.0)
        momentum_bonus = min(self.momentum_score / 5.0, 0.2)
        return min(base_confidence + momentum_bonus, 1.0)


@dataclass
class FlowReport:
    """
    Complete flow analysis report for a market.

    Contains all flow results with temporal analysis.
    """

    match_id: str
    market_type: MarketType
    initial_snapshot: ProbabilitySnapshot
    latest_snapshot: ProbabilitySnapshot
    flows: list[FlowResult] = field(default_factory=list)
    time_delta: timedelta = field(default_factory=timedelta.zero)
    generated_at: datetime = field(default_factory=datetime.now)
    aggregate_momentum: float = 0.0  # Overall market momentum

    def get_upward_flows(self) -> list[FlowResult]:
        """Return all outcomes with upward flow."""
        return [f for f in self.flows if f.direction == FlowDirection.UPWARD]

    def get_significant_flows(self, threshold: float = 2.0) -> list[FlowResult]:
        """Return all flows exceeding significance threshold."""
        return [f for f in self.flows if f.is_significant(threshold)]

    def get_flow_summary(self) -> dict[str, Any]:
        """Generate a summary dictionary of flow analysis."""
        upward = self.get_upward_flows()
        return {
            "match_id": self.match_id,
            "total_outcomes": len(self.flows),
            "upward_count": len(upward),
            "downward_count": len([f for f in self.flows if f.direction == FlowDirection.NEGATIVE]),
            "neutral_count": len([f for f in self.flows if f.direction == FlowDirection.NEUTRAL]),
            "aggregate_momentum": self.aggregate_momentum,
            "time_delta_hours": self.time_delta.total_seconds() / 3600,
        }


@dataclass
class EloRating:
    """
    Elo rating system for team strength modeling.

    Based on Arpad Elo's system adapted for sports analytics.
    """

    team_id: str
    rating: float = 1500.0  # Default starting rating
    rd: float = 350.0  # Rating deviation (uncertainty)
    volatility: float = 0.06  # Expected fluctuation
    games_played: int = 0
    last_game_date: Optional[datetime] = None
    rating_history: list[tuple[datetime, float]] = field(default_factory=list)

    K_FACTOR_BASE = 32.0  # Base learning rate
    K_FACTOR_SCALE = 2000.0

    def calculate_k_factor(self) -> float:
        """Calculate dynamic K-factor based on games played and rating deviation."""
        if self.games_played < 30:
            k = self.K_FACTOR_BASE
        elif self.rd > 50:
            k = self.K_FACTOR_BASE * 1.0
        else:
            k = self.K_FACTOR_BASE * (self.rd / self.K_FACTOR_SCALE)
        return min(k, self.K_FACTOR_BASE)

    def expected_score(self, opponent_rating: float) -> float:
        """Calculate expected score against opponent."""
        return 1.0 / (1.0 + 10.0 ** ((opponent_rating - self.rating) / 400.0))

    def update(self, actual_score: float, expected_score: float, game_date: datetime) -> None:
        """Update rating after a game."""
        k = self.calculate_k_factor()
        new_rating = self.rating + k * (actual_score - expected_score)
        
        # Update rating deviation
        new_rd = math.sqrt(self.rd ** 2 + self.volatility ** 2)
        new_rd = max(min(new_rd, 350.0), 30.0)  # Clamp to reasonable range

        self.rating = new_rating
        self.rd = new_rd
        self.games_played += 1
        self.last_game_date = game_date
        self.rating_history.append((game_date, new_rating))


class ProbabilityEngine:
    """
    Advanced probability analysis engine with Bayesian inference.

    Implements:
    - Shin method for market margin removal
    - Bayesian updating for dynamic probability estimation
    - Time series momentum analysis
    - Elo-based team strength modeling

    Example:
        >>> engine = ProbabilityEngine()
        >>> result = engine.calculate_true_probability({
        ...     'home': 1.50,
        ...     'draw': 4.20,
        ...     'away': 6.00
        ... })
    """

    FLOW_THRESHOLD_LOW = 0.5
    FLOW_THRESHOLD_MEDIUM = 2.0
    FLOW_THRESHOLD_HIGH = 5.0

    def __init__(self, config: Optional[dict[str, Any]] = None):
        """
        Initialize the probability engine.

        Args:
            config: Optional configuration dictionary with thresholds and parameters
        """
        self.config = config or {}
        self.flow_threshold_low = self.config.get(
            "flow_threshold_low", self.FLOW_THRESHOLD_LOW
        )
        self.flow_threshold_medium = self.config.get(
            "flow_threshold_medium", self.FLOW_THRESHOLD_MEDIUM
        )
        self.flow_threshold_high = self.config.get(
            "flow_threshold_high", self.FLOW_THRESHOLD_HIGH
        )
        
        # Bayesian parameters
        self.prior_strength = self.config.get("prior_strength", 1.0)
        self.evidence_weight = self.config.get("evidence_weight", 1.0)
        
        # Elo ratings storage
        self.elo_ratings: dict[str, EloRating] = {}

    def calculate_true_probability(
        self, 
        implied_quotes: dict[str, float],
        method: str = "shin_normalized"
    ) -> TrueProbabilityResult:
        """
        Calculate true probabilities from implied quotes.

        Uses Shin normalization method (Shin, 1992) for market margin removal:
        P_true(outcome_i) = (1 / quote_i) / Σ(1 / quote_j)

        Args:
            implied_quotes: Dictionary mapping outcomes to decimal quotes
            method: Normalization method to use

        Returns:
            TrueProbabilityResult with normalized probabilities
        """
        if not implied_quotes:
            raise ValueError("Quotes dictionary cannot be empty")

        for outcome, quote in implied_quotes.items():
            if quote <= 0:
                raise ValueError(f"Invalid quote value for {outcome}: {quote}")

        # Calculate implied probabilities
        implied_probs = {outcome: 1.0 / quote for outcome, quote in implied_quotes.items()}

        # Calculate market margin (overround)
        market_margin = sum(implied_probs.values()) - 1.0

        # Calculate per-outcome margin using Shin method
        margin_per_outcome = {}
        total_inverse = sum(implied_probs.values())
        for outcome, impl_prob in implied_probs.items():
            # Shin's method allocates margin proportionally
            margin_per_outcome[outcome] = (impl_prob / total_inverse) * market_margin

        # Normalize to get true probabilities
        total_implied = sum(implied_probs.values())
        true_probs = {
            outcome: prob / total_implied
            for outcome, prob in implied_probs.items()
        }

        # Calculate 95% confidence intervals (simplified)
        n = len(true_probs)
        conf_intervals = {}
        for outcome, prob in true_probs.items():
            # Wilson score interval
            z = 1.96  # 95% confidence
            denom = 1 + z**2 / n
            center = (prob + z**2 / (2 * n)) / denom
            margin = z * math.sqrt((prob * (1 - prob) + z**2 / (4 * n)) / denom) / denom
            conf_intervals[outcome] = (max(0, center - margin), min(1, center + margin))

        return TrueProbabilityResult(
            true_probabilities=true_probs,
            implied_probabilities=implied_probs,
            market_margin=market_margin,
            margin_per_outcome=margin_per_outcome,
            method=method,
            confidence_interval=conf_intervals,
        )

    def calculate_conditional_probability(
        self,
        outcome_probabilities: dict[str, float],
        condition_outcomes: list[str],
    ) -> dict[str, float]:
        """
        Calculate conditional probabilities within a subset of outcomes.

        Args:
            outcome_probabilities: Probabilities for all outcomes
            condition_outcomes: Subset of outcomes to condition on

        Returns:
            Dictionary of conditional probabilities
        """
        condition_total = sum(
            outcome_probabilities.get(o, 0) for o in condition_outcomes
        )

        if condition_total == 0:
            return {o: 0.0 for o in condition_outcomes}

        return {
            outcome: outcome_probabilities.get(outcome, 0) / condition_total
            for outcome in condition_outcomes
        }

    def bayesian_update(
        self,
        prior: BayesianPrior,
        evidence_successes: int,
        evidence_trials: int,
    ) -> BayesianPosterior:
        """
        Update probability estimate using Bayesian inference.

        Uses Beta-Binomial conjugate model for efficient updating.

        Args:
            prior: Prior distribution
            evidence_successes: Number of successful outcomes observed
            evidence_trials: Total number of trials observed

        Returns:
            BayesianPosterior with updated distribution parameters
        """
        # Posterior parameters (Beta-Binomial conjugate)
        posterior_alpha = prior.alpha + evidence_successes
        posterior_beta = prior.beta + (evidence_trials - evidence_successes)

        # Expected value and standard deviation of Beta distribution
        expected_prob = posterior_alpha / (posterior_alpha + posterior_beta)
        variance = (posterior_alpha * posterior_beta) / (
            (posterior_alpha + posterior_beta) ** 2 * (posterior_alpha + posterior_beta + 1)
        )
        std_dev = math.sqrt(variance)

        # 95% credible interval using quantiles of Beta distribution
        # Using normal approximation for simplicity
        from math import sqrt
        z = 1.96
        lower = max(0, expected_prob - z * std_dev)
        upper = min(1, expected_prob + z * std_dev)

        return BayesianPosterior(
            posterior_alpha=posterior_alpha,
            posterior_beta=posterior_beta,
            expected_probability=expected_prob,
            std_deviation=std_dev,
            credible_interval=(lower, upper),
            update_evidence={
                "successes": evidence_successes,
                "trials": evidence_trials,
                "prior_source": prior.source.value,
            },
        )

    def combine_priors(
        self,
        priors: list[BayesianPrior],
        new_evidence: Optional[dict[str, int]] = None,
    ) -> BayesianPosterior:
        """
        Combine multiple Bayesian priors with weighted averaging.

        Args:
            priors: List of prior distributions from different sources
            new_evidence: Optional new evidence {successes, trials}

        Returns:
            Combined BayesianPosterior
        """
        total_weight = sum(p.weight for p in priors)
        
        # Weighted combination of prior parameters
        combined_alpha = sum(p.alpha * p.weight for p in priors) / total_weight
        combined_beta = sum(p.beta * p.weight for p in priors) / total_weight

        # Apply new evidence if provided
        if new_evidence:
            combined_alpha += new_evidence.get("successes", 0)
            combined_beta += new_evidence.get("trials", 0) - new_evidence.get("successes", 0)

        return BayesianPosterior(
            posterior_alpha=combined_alpha,
            posterior_beta=combined_beta,
            expected_probability=combined_alpha / (combined_alpha + combined_beta),
            std_deviation=math.sqrt(
                combined_alpha * combined_beta /
                ((combined_alpha + combined_beta) ** 2 * (combined_alpha + combined_beta + 1))
            ),
            credible_interval=(0, 1),  # Would need proper Beta quantiles
            update_evidence={"combined_priors": len(priors)},
        )

    def get_or_create_elo(self, team_id: str) -> EloRating:
        """Get or create Elo rating for a team."""
        if team_id not in self.elo_ratings:
            self.elo_ratings[team_id] = EloRating(team_id=team_id)
        return self.elo_ratings[team_id]

    def predict_with_elo(
        self,
        home_team: str,
        away_team: str,
        home_advantage: float = 100.0,
    ) -> dict[str, float]:
        """
        Predict match outcome probabilities using Elo ratings.

        Args:
            home_team: Home team identifier
            away_team: Away team identifier
            home_advantage: Home advantage in Elo points

        Returns:
            Dictionary with predicted probabilities
        """
        home_elo = self.get_or_create_elo(home_team)
        away_elo = self.get_or_create_elo(away_team)

        # Apply home advantage
        adjusted_home = home_elo.rating + home_advantage

        # Calculate expected scores
        home_expected = home_elo.expected_score(away_elo.rating)
        away_expected = 1.0 - home_expected

        # Simple 3-way probability estimation
        # This is a simplification; real models would use goal distributions
        draw_prob = 0.25  # Typical draw rate, would be refined
        home_win_prob = home_expected * (1 - draw_prob / 2)
        away_win_prob = away_expected * (1 - draw_prob / 2)

        # Normalize to sum to 1
        total = home_win_prob + draw_prob + away_win_prob
        
        return {
            "home_win": home_win_prob / total,
            "draw": draw_prob / total,
            "away_win": away_win_prob / total,
        }

    def update_elo_from_result(
        self,
        home_team: str,
        away_team: str,
        home_goals: int,
        away_goals: int,
        game_date: datetime,
        home_advantage: float = 100.0,
    ) -> tuple[EloRating, EloRating]:
        """
        Update Elo ratings based on match result.

        Args:
            home_team: Home team identifier
            away_team: Away team identifier
            home_goals: Goals scored by home team
            away_goals: Goals scored by away team
            game_date: Date of the match
            home_advantage: Home advantage in Elo points

        Returns:
            Tuple of (updated_home_elo, updated_away_elo)
        """
        home_elo = self.get_or_create_elo(home_team)
        away_elo = self.get_or_create_elo(away_team)

        # Actual score (1 for win, 0.5 for draw, 0 for loss)
        if home_goals > away_goals:
            home_actual, away_actual = 1.0, 0.0
        elif home_goals < away_goals:
            home_actual, away_actual = 0.0, 1.0
        else:
            home_actual, away_actual = 0.5, 0.5

        # Expected scores
        home_expected = home_elo.expected_score(away_elo.rating)
        away_expected = 1.0 - home_expected

        # Update ratings
        home_elo.update(home_actual, home_expected, game_date)
        away_elo.update(away_actual, away_expected, game_date)

        return home_elo, away_elo

    def analyze_flow(
        self,
        initial_snapshot: ProbabilitySnapshot,
        latest_snapshot: ProbabilitySnapshot,
        historical_snapshots: Optional[list[ProbabilitySnapshot]] = None,
    ) -> FlowReport:
        """
        Analyze probability flow between time points with momentum analysis.

        Flow(outcome) = P_latest(outcome) - P_initial(outcome)

        Args:
            initial_snapshot: Earlier probability snapshot
            latest_snapshot: Later probability snapshot
            historical_snapshots: Optional historical snapshots for momentum calculation

        Returns:
            FlowReport with all flow results and momentum indicators
        """
        flows = []

        # Calculate true probabilities for both snapshots
        initial_true = self.calculate_true_probability(
            {k: 1.0 / v for k, v in initial_snapshot.probabilities.items()}
        )
        latest_true = self.calculate_true_probability(
            {k: 1.0 / v for k, v in latest_snapshot.probabilities.items()}
        )

        # Time delta
        time_delta = latest_snapshot.timestamp - initial_snapshot.timestamp

        # Calculate flow for each outcome
        for outcome in initial_true.true_probabilities:
            initial_prob = initial_true.true_probabilities[outcome]
            latest_prob = latest_true.true_probabilities.get(outcome, initial_prob)
            flow_pp = (latest_prob - initial_prob) * 100

            # Classify direction
            if flow_pp > self.flow_threshold_low:
                direction = FlowDirection.POSITIVE
            elif flow_pp < -self.flow_threshold_low:
                direction = FlowDirection.NEGATIVE
            else:
                direction = FlowDirection.NEUTRAL

            # Assess significance
            abs_flow = abs(flow_pp)
            if abs_flow >= self.flow_threshold_high:
                significance = "high"
            elif abs_flow >= self.flow_threshold_medium:
                significance = "medium"
            else:
                significance = "low"

            # Calculate momentum (if historical data available)
            momentum_score = 0.0
            velocity = 0.0
            acceleration = 0.0

            if historical_snapshots:
                # Simplified momentum calculation
                momentum_score = flow_pp * len(historical_snapshots) / max(len(historical_snapshots), 1)
                velocity = flow_pp / max(time_delta.total_seconds() / 3600, 1)
                
                if len(historical_snapshots) >= 2:
                    # Acceleration is change in velocity
                    acceleration = velocity * 0.1  # Simplified

            flows.append(
                FlowResult(
                    outcome=outcome,
                    flow_pp=flow_pp,
                    direction=direction,
                    initial_prob=initial_prob,
                    latest_prob=latest_prob,
                    momentum_score=momentum_score,
                    significance=significance,
                    velocity=velocity,
                    acceleration=acceleration,
                )
            )

        # Calculate aggregate momentum
        aggregate_momentum = sum(f.momentum_score for f in flows) / max(len(flows), 1)

        return FlowReport(
            match_id=f"match_{initial_snapshot.timestamp.timestamp()}",
            market_type=initial_snapshot.market_type,
            initial_snapshot=initial_snapshot,
            latest_snapshot=latest_snapshot,
            flows=flows,
            time_delta=time_delta,
            aggregate_momentum=aggregate_momentum,
        )


__all__ = [
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
]

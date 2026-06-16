"""
SPAF - Sports Analytics Framework
Domain-Aware Intelligence System

This module implements the comprehensive domain awareness system that integrates
multiple intelligence sources for enhanced probability analysis.

Features:
- Multi-source intelligence integration
- Cross-validation of signals
- Situational awareness scoring
- Temporal context analysis

⚠️ ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional
import math


class IntelligenceWeight(Enum):
    """Intelligence source weights for confidence calculation."""

    CRITICAL = 1.0    # Must have
    HIGH = 0.8        # Strong indicator
    MEDIUM = 0.5      # Moderate indicator
    LOW = 0.3         # Weak indicator


class ConfidenceLevel(Enum):
    """Overall confidence level classification."""

    VERY_HIGH = "very_high"   # Strong multi-source confirmation
    HIGH = "high"            # Good confirmation
    MEDIUM = "medium"        # Some confirmation
    LOW = "low"              # Weak signals
    NEGATIVE = "negative"    # Conflicting signals


@dataclass
class IntelligenceRecord:
    """
    A single intelligence record from a specific source.

    Attributes:
        source: The intelligence source
        timestamp: When the intelligence was gathered
        content: The intelligence content
        confidence: Confidence level (0-1)
        weight: Weight of this source in analysis
        validated: Whether this intelligence has been cross-validated
    """

    source: str
    timestamp: datetime
    content: dict[str, Any]
    confidence: float = 0.5
    weight: float = 1.0
    validated: bool = False

    def is_reliable(self, min_confidence: float = 0.3) -> bool:
        """Check if intelligence meets minimum confidence threshold."""
        return self.confidence >= min_confidence and self.weight >= 0.3


@dataclass
class TeamIntelligence:
    """
    Comprehensive intelligence for a single team.

    Contains all available information about a team's current state.
    """

    team_id: str
    team_name: str
    ranking: Optional[int] = None
    ranking_points: Optional[float] = None
    
    # Form indicators
    recent_results: list[str] = field(default_factory=list)  # W/D/L sequence
    recent_goals_scored: list[int] = field(default_factory=list)
    recent_goals_conceded: list[int] = field(default_factory=list)
    
    # Tactical indicators
    home_advantage: float = 0.0  # Home performance modifier
    away_performance: float = 0.0  # Away performance modifier
    
    # Availability
    key_players_available: int = 0
    key_players_total: int = 0
    injuries_count: int = 0
    
    # Context
    motivation_factor: float = 1.0  # Tournament context
    travel_distance: float = 0.0  # In km
    rest_days: int = 7  # Days since last match
    
    # Intelligence records
    intelligence_history: list[IntelligenceRecord] = field(default_factory=list)

    @property
    def form_score(self) -> float:
        """Calculate team's recent form score (0-1)."""
        if not self.recent_results:
            return 0.5
        
        scores = []
        for result in self.recent_results[-5:]:  # Last 5 matches
            if result == 'W':
                scores.append(1.0)
            elif result == 'D':
                scores.append(0.5)
            else:
                scores.append(0.0)
        
        return sum(scores) / len(scores) if scores else 0.5

    @property
    def attack_strength(self) -> float:
        """Calculate attack strength (0-2, 1 = average)."""
        if not self.recent_goals_scored:
            return 1.0
        recent = self.recent_goals_scored[-5:]
        avg_goals = sum(recent) / len(recent)
        return min(avg_goals / 1.5, 2.0)  # Normalize around 1.5 goals

    @property
    def defense_strength(self) -> float:
        """Calculate defense strength (0-2, 1 = average)."""
        if not self.recent_goals_conceded:
            return 1.0
        recent = self.recent_goals_conceded[-5:]
        avg_conceded = sum(recent) / len(recent)
        return min(2.0 - avg_conceded / 1.5, 2.0)  # Invert: fewer conceded = stronger

    @property
    def availability_ratio(self) -> float:
        """Ratio of available key players."""
        if self.key_players_total == 0:
            return 1.0
        return self.key_players_available / self.key_players_total

    @property
    def fatigue_factor(self) -> float:
        """Calculate fatigue based on rest days (0-1, 1 = fresh)."""
        # More rest = less fatigue
        return min(self.rest_days / 7.0, 1.0)


@dataclass
class MatchIntelligence:
    """
    Comprehensive intelligence for a match.

    Combines team intelligence with match-specific context.
    """

    match_id: str
    home_team: TeamIntelligence
    away_team: TeamIntelligence
    
    # Match context
    competition: str = ""
    round: Optional[str] = None
    importance: float = 1.0  # 1 = normal, >1 = important
    
    # Head to head
    h2h_home_wins: int = 0
    h2h_draws: int = 0
    h2h_away_wins: int = 0
    h2h_recent: list[str] = field(default_factory=list)
    
    # Conditions
    weather: str = "unknown"
    venue_neutral: bool = False
    
    # Intelligence records
    match_intelligence: list[IntelligenceRecord] = field(default_factory=list)
    
    # Timestamp
    gathered_at: datetime = field(default_factory=datetime.now)

    @property
    def h2h_home_win_rate(self) -> float:
        """Calculate head-to-head home win rate."""
        total = self.h2h_home_wins + self.h2h_draws + self.h2h_away_wins
        if total == 0:
            return 0.33  # Default equal probability
        return self.h2h_home_wins / total

    def get_strength_difference(self) -> float:
        """Calculate relative strength difference (-1 to 1)."""
        home_strength = (
            self.home_team.form_score * 0.3 +
            self.home_team.attack_strength * 0.2 +
            self.home_team.defense_strength * 0.2 +
            self.home_team.availability_ratio * 0.2 +
            self.home_team.fatigue_factor * 0.1
        )
        
        away_strength = (
            self.away_team.form_score * 0.25 +
            self.away_team.attack_strength * 0.2 +
            self.away_team.defense_strength * 0.2 +
            self.away_team.availability_ratio * 0.2 +
            self.away_team.fatigue_factor * 0.15
        )
        
        # Apply home advantage
        home_strength += self.home_team.home_advantage * 0.1
        
        # Normalize to -1 to 1 range
        return (home_strength - away_strength) / max(home_strength + away_strength, 1.0)


@dataclass
class DomainAwarenessReport:
    """
    Complete domain awareness report for a match.

    Contains all intelligence integration results and confidence scores.
    """

    match_id: str
    match_intelligence: MatchIntelligence
    confidence_scores: dict[str, float] = field(default_factory=dict)
    intelligence_sources: list[IntelligenceRecord] = field(default_factory=list)
    validation_results: dict[str, bool] = field(default_factory=dict)
    final_confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    recommendations: list[str] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)

    def get_high_confidence_outcomes(self) -> list[str]:
        """Return outcomes with confidence above threshold."""
        return [
            outcome for outcome, conf in self.confidence_scores.items()
            if conf >= 0.7
        ]

    def get_cross_validated_signals(self) -> dict[str, float]:
        """Return signals that are cross-validated by multiple sources."""
        validated = {}
        for outcome, conf in self.confidence_scores.items():
            if self.validation_results.get(outcome, False):
                validated[outcome] = conf * 1.2  # Boost validated signals
        return validated


class DomainAwarenessSystem:
    """
    Comprehensive domain awareness system for sports analytics.

    Integrates multiple intelligence sources to provide validated
    confidence scores for probability analysis.

    Example:
        >>> system = DomainAwarenessSystem()
        >>> report = system.analyze_match(match_intel)
        >>> confidence = report.get_high_confidence_outcomes()
    """

    # Confidence thresholds
    THRESHOLD_VERY_HIGH = 0.85
    THRESHOLD_HIGH = 0.70
    THRESHOLD_MEDIUM = 0.50
    THRESHOLD_LOW = 0.30

    def __init__(self, config: Optional[dict[str, Any]] = None):
        """
        Initialize the domain awareness system.

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}

    def assess_intelligence_reliability(
        self,
        intelligence: IntelligenceRecord,
        context: Optional[dict[str, Any]] = None,
    ) -> float:
        """
        Assess the reliability of a piece of intelligence.

        Considers:
        - Source reputation
        - Freshness (time decay)
        - Cross-validation
        - Historical accuracy

        Args:
            intelligence: The intelligence to assess
            context: Additional context for assessment

        Returns:
            Reliability score (0-1)
        """
        base_confidence = intelligence.confidence

        # Time decay: older intelligence is less reliable
        age = datetime.now() - intelligence.timestamp
        if age > timedelta(hours=48):
            time_factor = 0.7
        elif age > timedelta(hours=24):
            time_factor = 0.85
        elif age > timedelta(hours=6):
            time_factor = 0.95
        else:
            time_factor = 1.0

        # Source weight factor
        source_factor = intelligence.weight

        # Validation bonus
        validation_factor = 1.1 if intelligence.validated else 1.0

        # Combine factors
        reliability = base_confidence * time_factor * source_factor * validation_factor
        return min(reliability, 1.0)

    def calculate_signal_alignment(
        self,
        flow_direction: str,
        intelligence_direction: str,
    ) -> float:
        """
        Calculate alignment between probability flow and intelligence signals.

        Args:
            flow_direction: Direction from flow analysis (upward/downward/stable)
            intelligence_direction: Direction from intelligence (positive/negative/neutral)

        Returns:
            Alignment score (-1 to 1)
        """
        alignment_map = {
            ("upward", "positive"): 1.0,
            ("downward", "negative"): 1.0,
            ("stable", "neutral"): 0.5,
            ("upward", "neutral"): 0.2,
            ("downward", "neutral"): 0.2,
            ("upward", "negative"): -0.5,
            ("downward", "positive"): -0.5,
        }

        return alignment_map.get((flow_direction, intelligence_direction), 0.0)

    def integrate_team_intelligence(
        self,
        team_intel: TeamIntelligence,
        historical_accuracy: Optional[dict[str, float]] = None,
    ) -> dict[str, float]:
        """
        Integrate all team intelligence into probability modifiers.

        Args:
            team_intel: Team intelligence data
            historical_accuracy: Historical accuracy by source

        Returns:
            Dictionary of probability modifiers
        """
        modifiers = {}

        # Form modifier
        form_impact = (team_intel.form_score - 0.5) * 0.15  # ±7.5% max impact
        modifiers["form"] = form_impact

        # Attack modifier
        attack_impact = (team_intel.attack_strength - 1.0) * 0.10
        modifiers["attack"] = attack_impact

        # Defense modifier
        defense_impact = (team_intel.defense_strength - 1.0) * 0.10
        modifiers["defense"] = defense_impact

        # Availability modifier
        availability_impact = (team_intel.availability_ratio - 0.8) * 0.10
        modifiers["availability"] = availability_impact

        # Fatigue modifier
        fatigue_impact = (team_intel.fatigue_factor - 0.5) * 0.05
        modifiers["fatigue"] = fatigue_impact

        # Motivation modifier
        motivation_impact = (team_intel.motivation_factor - 1.0) * 0.08
        modifiers["motivation"] = motivation_impact

        return modifiers

    def cross_validate_signals(
        self,
        signals: dict[str, float],
        min_agreement: float = 0.6,
    ) -> dict[str, bool]:
        """
        Cross-validate signals from multiple sources.

        Args:
            signals: Dictionary of outcome -> signal strength
            min_agreement: Minimum proportion of sources agreeing

        Returns:
            Dictionary of outcome -> validation result
        """
        if not signals:
            return {}

        max_signal = max(abs(s) for s in signals.values())
        if max_signal == 0:
            return {k: False for k in signals.keys()}

        # Normalize signals
        normalized = {k: v / max_signal for k, v in signals.items()}

        # A signal is validated if its normalized strength is above threshold
        # and agrees with the majority direction
        positive_count = sum(1 for v in normalized.values() if v > 0)
        total_count = len(normalized)
        majority_positive = positive_count / total_count >= 0.5

        validation = {}
        for outcome, signal in normalized.items():
            # Validate if above threshold and agrees with majority
            is_above_threshold = abs(signal) >= min_agreement
            agrees_with_majority = (signal > 0) == majority_positive or abs(signal) < 0.3
            validation[outcome] = is_above_threshold and agrees_with_majority

        return validation

    def calculate_confidence(
        self,
        match_intel: MatchIntelligence,
        flow_confidences: dict[str, float],
        intelligence_modifiers: dict[str, dict[str, float]],
    ) -> tuple[dict[str, float], ConfidenceLevel]:
        """
        Calculate final confidence scores for each outcome.

        Combines flow analysis confidence with intelligence confidence.

        Args:
            match_intel: Match intelligence data
            flow_confidences: Confidence from flow analysis
            intelligence_modifiers: Intelligence-based modifiers

        Returns:
            Tuple of (confidence_scores, overall_confidence_level)
        """
        # Combine intelligence modifiers for home/away
        home_modifier = sum(intelligence_modifiers.get("home", {}).values())
        away_modifier = sum(intelligence_modifiers.get("away", {}).values())

        # Calculate intelligence-based confidence
        intelligence_confidence = {
            "home_win": 0.33 + home_modifier,
            "draw": 0.33,
            "away_win": 0.33 + away_modifier,
        }

        # Normalize to sum to 1
        total = sum(intelligence_confidence.values())
        intelligence_confidence = {
            k: v / total for k, v in intelligence_confidence.items()
        }

        # Combine with flow confidence (weighted average)
        flow_weight = 0.6
        intelligence_weight = 0.4

        combined_confidence = {}
        for outcome in flow_confidences:
            flow_conf = flow_confidences.get(outcome, 0.33)
            intel_conf = intelligence_confidence.get(outcome, 0.33)
            combined_confidence[outcome] = (
                flow_weight * flow_conf + intelligence_weight * intel_conf
            )

        # Determine overall confidence level
        avg_confidence = sum(combined_confidence.values()) / len(combined_confidence)
        
        if avg_confidence >= self.THRESHOLD_VERY_HIGH:
            overall = ConfidenceLevel.VERY_HIGH
        elif avg_confidence >= self.THRESHOLD_HIGH:
            overall = ConfidenceLevel.HIGH
        elif avg_confidence >= self.THRESHOLD_MEDIUM:
            overall = ConfidenceLevel.MEDIUM
        elif avg_confidence >= self.THRESHOLD_LOW:
            overall = ConfidenceLevel.LOW
        else:
            overall = ConfidenceLevel.NEGATIVE

        return combined_confidence, overall

    def analyze_match(
        self,
        match_intel: MatchIntelligence,
        flow_confidences: Optional[dict[str, float]] = None,
    ) -> DomainAwarenessReport:
        """
        Perform comprehensive domain awareness analysis for a match.

        Args:
            match_intel: Complete match intelligence
            flow_confidences: Optional confidence from flow analysis

        Returns:
            DomainAwarenessReport with analysis results
        """
        flow_confidences = flow_confidences or {
            "home_win": 0.33,
            "draw": 0.33,
            "away_win": 0.33,
        }

        # Integrate team intelligence
        home_modifiers = self.integrate_team_intelligence(match_intel.home_team)
        away_modifiers = self.integrate_team_intelligence(match_intel.away_team)

        intelligence_modifiers = {
            "home": home_modifiers,
            "away": away_modifiers,
        }

        # Calculate confidence scores
        confidence_scores, overall_level = self.calculate_confidence(
            match_intel,
            flow_confidences,
            intelligence_modifiers,
        )

        # Cross-validate signals
        validation_results = self.cross_validate_signals(confidence_scores)

        # Generate recommendations
        recommendations = []
        if overall_level == ConfidenceLevel.VERY_HIGH:
            recommendations.append("Strong multi-source confirmation detected")
            recommendations.append("High confidence in current signals")
        elif overall_level == ConfidenceLevel.HIGH:
            recommendations.append("Good confirmation from multiple sources")
        elif overall_level == ConfidenceLevel.NEGATIVE:
            recommendations.append("Warning: Conflicting signals detected")
            recommendations.append("Consider additional verification")

        # Strength difference insight
        strength_diff = match_intel.get_strength_difference()
        if abs(strength_diff) > 0.3:
            if strength_diff > 0:
                recommendations.append(f"Home team significantly stronger (delta: {strength_diff:.2f})")
            else:
                recommendations.append(f"Away team significantly stronger (delta: {abs(strength_diff):.2f})")

        return DomainAwarenessReport(
            match_id=match_intel.match_id,
            match_intelligence=match_intel,
            confidence_scores=confidence_scores,
            intelligence_sources=[],
            validation_results=validation_results,
            final_confidence=overall_level,
            recommendations=recommendations,
        )

    def generate_intelligence_summary(
        self,
        report: DomainAwarenessReport,
    ) -> str:
        """
        Generate a human-readable summary of the intelligence analysis.

        Args:
            report: The domain awareness report

        Returns:
            Formatted summary string
        """
        lines = [
            f"Domain Awareness Report for {report.match_id}",
            "=" * 50,
            f"Overall Confidence: {report.final_confidence.value.upper()}",
            "",
            "Confidence Scores:",
        ]

        for outcome, confidence in sorted(
            report.confidence_scores.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            bar = "█" * int(confidence * 20) + "░" * (20 - int(confidence * 20))
            lines.append(f"  {outcome}: {confidence:.1%} |{bar}|")

        lines.append("")
        lines.append("Recommendations:")
        for rec in report.recommendations:
            lines.append(f"  • {rec}")

        return "\n".join(lines)


__all__ = [
    "IntelligenceWeight",
    "ConfidenceLevel",
    "IntelligenceRecord",
    "TeamIntelligence",
    "MatchIntelligence",
    "DomainAwarenessReport",
    "DomainAwarenessSystem",
]

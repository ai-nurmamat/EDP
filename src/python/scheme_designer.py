"""
Expected Domain Perception
期望域感知法

Scheme Design Engine.

This module implements the scheme design engine based on:
- Three Principles (non-negotiable constraints)
- Modern Portfolio Theory adapted for probability analysis (Markowitz, 1952)
- Kelly criterion variant for capital allocation

A Methodology for Asymmetric Expected Value Discovery Based on Probability Flow and Domain Awareness

References:
    Markowitz, H. (1952). "Portfolio Selection."
    The Journal of Finance, 7(1), 77-91.

    Kelly, J.L. (1956). "A New Interpretation of Information Rate."
    The Bell System Technical Journal, 35(4), 917-926.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from .probability_engine import FlowDirection, MarketType
from .flow_analyzer import AmplificationResult, AmplificationReport


class RiskLevel(Enum):
    """Risk classification for scheme layers."""

    CONSERVATIVE = "conservative"  # High probability, low return
    BALANCED = "balanced"  # Medium probability, medium return
    AGGRESSIVE = "aggressive"  # Low probability, high return
    EXTREME = "extreme"  # Very low probability, very high return


class ValidationResult(Enum):
    """Result of scheme validation."""

    VALID = "valid"
    INVALID = "invalid"
    WARNING = "warning"


@dataclass
class SchemeLeg:
    """
    A single leg (selection) in a scheme.

    Each leg represents one selection from one match.
    """

    match_id: str
    market_type: MarketType
    selection: str
    odds: float
    flow_direction: FlowDirection
    amplification_score: float = 0.0
    confidence: float = 1.0

    def has_positive_flow(self) -> bool:
        """Check if this leg has positive probability flow."""
        return self.flow_direction == FlowDirection.POSITIVE


@dataclass
class Scheme:
    """
    A complete scheme (ticket) with multiple legs.

    Represents a single multi-leg investment configuration.
    """

    legs: list[SchemeLeg]
    combination_type: str  # e.g., "2-fold", "3-fold", "M-fold-N"
    multiplier: int = 1
    stake_per_combination: float = 2.0
    risk_level: RiskLevel = RiskLevel.BALANCED
    validation_errors: list[str] = field(default_factory=list)

    @property
    def num_combinations(self) -> int:
        """Calculate number of combinations for M-fold-N scheme."""
        # Simplified: for standard combinations, it's 1
        # For M-fold-N, calculate combinations
        if "串" in self.combination_type:
            # Parse Chinese format like "3串4"
            parts = self.combination_type.replace("串", " ").split()
            if len(parts) == 2:
                m = int(parts[0])
                n = int(parts[1])
                # Calculate combinations based on M-fold-N rules
                return self._calculate_m_fold_n_combinations(m, n)
        return 1

    def _calculate_m_fold_n_combinations(self, m: int, n: int) -> int:
        """Calculate number of combinations for M-fold-N scheme."""
        # This is a simplified implementation
        # Real implementation would use combinatorial formulas
        from math import comb

        if n == 1:
            return 1
        # Sum of combinations from minimum hits to m
        total = 0
        min_hits = m - n + 1  # Simplified assumption
        for k in range(min_hits, m + 1):
            total += comb(m, k)
        return max(total, 1)

    @property
    def total_cost(self) -> float:
        """Calculate total cost of this scheme."""
        return self.num_combinations * self.stake_per_combination * self.multiplier

    @property
    def combined_odds(self) -> float:
        """Calculate combined odds for all legs."""
        result = 1.0
        for leg in self.legs:
            result *= leg.odds
        return result

    @property
    def potential_return(self) -> float:
        """Calculate potential return (excluding stake)."""
        return self.total_cost * (self.combined_odds - 1)

    def has_positive_flow_legs_only(self) -> bool:
        """Check if all legs have positive flow (Principle 1)."""
        return all(leg.has_positive_flow() for leg in self.legs)

    def provides_meaningful_return(self, min_multiplier: float = 3.0) -> bool:
        """Check if scheme provides meaningful return (Principle 2)."""
        return self.combined_odds >= min_multiplier


@dataclass
class SchemeBundle:
    """
    A bundle of schemes with budget allocation.

    Contains multiple schemes across different risk levels.
    """

    schemes: list[Scheme]
    total_budget: float
    allocated_budget: float = 0.0
    generated_at: datetime = field(default_factory=datetime.now)

    @property
    def remaining_budget(self) -> float:
        """Calculate remaining unallocated budget."""
        return self.total_budget - self.allocated_budget

    @property
    def total_potential_return(self) -> float:
        """Calculate total potential return across all schemes."""
        return sum(s.potential_return for s in self.schemes)

    def get_schemes_by_risk(self, risk_level: RiskLevel) -> list[Scheme]:
        """Get all schemes of a specific risk level."""
        return [s for s in self.schemes if s.risk_level == risk_level]


class SchemeDesigner:
    """
    Scheme design engine implementing the Three Principles.

    The Three Principles (non-negotiable):
    1. Respect Probability Flow - All legs must have positive flow
    2. Respect Asymmetric Returns - Minimum 3x return potential
    3. Respect Rules - Comply with all betting rules

    Example:
        >>> designer = SchemeDesigner()
        >>> bundle = designer.generate_schemes(
        ...     amplification_report=report,
        ...     budget=100,
        ...     match_data=matches
        ... )
    """

    # Rule constants
    MAX_SELECTION_DEPTH_NO_SCORE = 8
    MAX_SELECTION_DEPTH_WITH_SCORE = 4
    MAX_SELECTION_DEPTH_WITH_HTFT = 4
    MAX_SELECTION_DEPTH_WITH_TOTAL = 6
    MAX_MULTIPLIER = 99
    MAX_INVESTMENT_AMOUNT = 20000
    MIN_INVESTMENT = 2.0
    MIN_RETURN_MULTIPLIER = 3.0

    # Budget allocation by risk level
    BUDGET_ALLOCATION = {
        RiskLevel.CONSERVATIVE: 0.20,
        RiskLevel.BALANCED: 0.45,
        RiskLevel.AGGRESSIVE: 0.25,
        RiskLevel.EXTREME: 0.10,
    }

    def __init__(self, config: Optional[dict] = None):
        """
        Initialize the scheme designer.

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}

    def validate_scheme(self, scheme: Scheme) -> tuple[ValidationResult, list[str]]:
        """
        Validate a scheme against all rules and principles.

        Args:
            scheme: The scheme to validate

        Returns:
            Tuple of (ValidationResult, list of error messages)
        """
        errors = []

        # Principle 1: All legs must have positive flow
        if not scheme.has_positive_flow_legs_only():
            negative_legs = [
                leg.selection for leg in scheme.legs if not leg.has_positive_flow()
            ]
            errors.append(
                f"Principle 1 violation: Negative flow legs: {negative_legs}"
            )

        # Principle 2: Meaningful return
        if not scheme.provides_meaningful_return(self.MIN_RETURN_MULTIPLIER):
            errors.append(
                f"Principle 2 violation: Combined odds {scheme.combined_odds:.2f} "
                f"below minimum {self.MIN_RETURN_MULTIPLIER}"
            )

        # Rule: Same match different markets cannot combine
        match_markets: dict[str, set] = {}
        for leg in scheme.legs:
            if leg.match_id not in match_markets:
                match_markets[leg.match_id] = set()
            if leg.market_type in match_markets[leg.match_id]:
                errors.append(
                    f"Rule violation: Multiple legs from same match {leg.match_id}"
                )
            match_markets[leg.match_id].add(leg.market_type)

        # Rule: Selection depth limits
        has_score = any(
            leg.market_type == MarketType.CORRECT_SCORE for leg in scheme.legs
        )
        has_htft = any(
            leg.market_type == MarketType.HALF_TIME_FULL_TIME for leg in scheme.legs
        )
        max_depth = self.MAX_PARLAY_DEPTH_NO_SCORE
        if has_score or has_htft:
            max_depth = self.MAX_SELECTION_DEPTH_WITH_SCORE

        if len(scheme.legs) > max_depth:
            errors.append(
                f"Rule violation: Selection depth {len(scheme.legs)} exceeds max {max_depth}"
            )

        # Rule: Multiplier limit
        if scheme.multiplier > self.MAX_MULTIPLIER:
            errors.append(
                f"Rule violation: Multiplier {scheme.multiplier} exceeds max {self.MAX_MULTIPLIER}"
            )

        # Rule: Investment amount limit
        if scheme.total_cost > self.MAX_INVESTMENT_AMOUNT:
            errors.append(
                f"Rule violation: Investment amount {scheme.total_cost} exceeds max {self.MAX_INVESTMENT_AMOUNT}"
            )

        # Rule: Minimum investment
        if scheme.stake_per_combination < self.MIN_INVESTMENT:
            errors.append(
                f"Rule violation: Investment {scheme.stake_per_combination} below minimum {self.MIN_INVESTMENT}"
            )

        if errors:
            return (ValidationResult.INVALID, errors)
        return (ValidationResult.VALID, [])

    def _classify_risk_level(self, combined_odds: float) -> RiskLevel:
        """Classify risk level based on combined odds."""
        if combined_odds < 5:
            return RiskLevel.CONSERVATIVE
        elif combined_odds < 20:
            return RiskLevel.BALANCED
        elif combined_odds < 100:
            return RiskLevel.AGGRESSIVE
        else:
            return RiskLevel.EXTREME

    def generate_schemes(
        self,
        amplification_report: AmplificationReport,
        budget: float,
        match_data: dict,
        max_schemes: int = 10,
    ) -> SchemeBundle:
        """
        Generate optimized schemes within budget.

        This is a simplified implementation. A full implementation would:
        1. Enumerate all valid leg combinations
        2. Score each combination by amplification
        3. Apply budget optimization
        4. Ensure diversification across matches and markets

        Args:
            amplification_report: Amplification analysis results
            budget: Total budget to allocate
            match_data: Match information dictionary
            max_schemes: Maximum number of schemes to generate

        Returns:
            SchemeBundle with optimized schemes
        """
        schemes = []
        reliable_amps = amplification_report.get_reliable_amplifications()

        # Sort by amplification score (descending)
        reliable_amps.sort(key=lambda a: a.amplification_score, reverse=True)

        # Generate schemes based on top amplification results
        # This is a simplified example - real implementation would be more sophisticated
        allocated = 0.0

        for i, amp in enumerate(reliable_amps[:max_schemes]):
            # Create a simple single-leg scheme for demonstration
            leg = SchemeLeg(
                match_id=amplification_report.match_id,
                market_type=amplification_report.flow_report.market_type,
                selection=amp.outcome,
                odds=3.0,  # Placeholder - would come from match_data
                flow_direction=FlowDirection.POSITIVE,
                amplification_score=amp.amplification_score,
                confidence=amp.confidence,
            )

            scheme = Scheme(
                legs=[leg],
                combination_type="单关",  # Single outcome selection
                multiplier=1,
                stake_per_combination=10.0,
                risk_level=self._classify_risk_level(3.0),
            )

            # Validate
            result, errors = self.validate_scheme(scheme)
            if result == ValidationResult.VALID:
                schemes.append(scheme)
                allocated += scheme.total_cost

        return SchemeBundle(
            schemes=schemes,
            total_budget=budget,
            allocated_budget=allocated,
        )

    def optimize_budget_allocation(
        self, bundle: SchemeBundle
    ) -> SchemeBundle:
        """
        Optimize budget allocation across schemes.

        Uses Kelly criterion variant to adjust stakes based on signal strength.

        Args:
            bundle: Current scheme bundle

        Returns:
            Optimized scheme bundle
        """
        total_score = sum(
            max(s.legs[0].amplification_score, 0.1) if s.legs else 0.1
            for s in bundle.schemes
        )

        for scheme in bundle.schemes:
            if scheme.legs:
                # Proportional allocation based on amplification score
                score = max(scheme.legs[0].amplification_score, 0.1)
                proportion = score / total_score
                target_budget = bundle.total_budget * proportion

                # Adjust stake
                scheme.stake_per_combination = min(
                    target_budget / scheme.num_combinations,
                    50.0,  # Max per combination
                )
                scheme.stake_per_combination = max(
                    scheme.stake_per_combination,
                    self.MIN_INVESTMENT,
                )

        # Recalculate allocated budget
        bundle.allocated_budget = sum(s.total_cost for s in bundle.schemes)

        return bundle


__all__ = [
    "RiskLevel",
    "ValidationResult",
    "SchemeLeg",
    "Scheme",
    "SchemeBundle",
    "SchemeDesigner",
]

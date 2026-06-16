"""
SPAF - Sports Analytics Framework
Analysis Strategy Engine.

This module implements the analysis strategy engine based on:
- Three Principles (non-negotiable constraints)
- Modern Portfolio Theory adapted for sports analytics (Markowitz, 1952)
- Kelly criterion variant for resource allocation

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
from .flow_amplification import AmplificationResult, AmplificationReport


class RiskLevel(Enum):
    """Risk classification for strategy layers."""

    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"
    EXTREME = "extreme"


class ValidationResult(Enum):
    """Result of strategy validation."""

    VALID = "valid"
    INVALID = "invalid"
    WARNING = "warning"


@dataclass
class StrategySelection:
    """
    A single selection in a strategy.

    Each selection represents one choice from one match.
    """

    match_id: str
    market_type: MarketType
    selection: str
    quote: float
    flow_direction: FlowDirection
    amplification_score: float = 0.0
    confidence: float = 1.0

    def has_upward_flow(self) -> bool:
        """Check if this selection has upward probability flow."""
        return self.flow_direction == FlowDirection.UPWARD


@dataclass
class Strategy:
    """
    A complete analysis strategy.

    Represents a combination of selections for analytical purposes.
    """

    selections: list[StrategySelection]
    combination_type: str
    multiplier: int = 1
    allocation_per_combination: float = 2.0
    risk_level: RiskLevel = RiskLevel.BALANCED
    validation_errors: list[str] = field(default_factory=list)

    @property
    def num_combinations(self) -> int:
        """Calculate number of combinations for M-fold-N combinations."""
        if "combo" in self.combination_type.lower():
            parts = self.combination_type.replace("-", " ").split()
            if len(parts) >= 2:
                try:
                    m = int(parts[0])
                    n = int(parts[1])
                    return self._calculate_combinations(m, n)
                except ValueError:
                    pass
        return 1

    def _calculate_combinations(self, m: int, n: int) -> int:
        """Calculate number of combinations."""
        from math import comb

        if n == 1:
            return 1
        total = 0
        min_hits = m - n + 1
        for k in range(min_hits, m + 1):
            total += comb(m, k)
        return max(total, 1)

    @property
    def total_allocation(self) -> float:
        """Calculate total allocation for this strategy."""
        return self.num_combinations * self.allocation_per_combination * self.multiplier

    @property
    def combined_quote(self) -> float:
        """Calculate combined quote for all selections."""
        result = 1.0
        for sel in self.selections:
            result *= sel.quote
        return result

    @property
    def potential_multiplier(self) -> float:
        """Calculate potential multiplier."""
        return self.combined_quote

    def has_upward_flow_selections_only(self) -> bool:
        """Check if all selections have upward flow."""
        return all(sel.has_upward_flow() for sel in self.selections)

    def provides_meaningful_multiplier(self, min_multiplier: float = 3.0) -> bool:
        """Check if strategy provides meaningful multiplier."""
        return self.combined_quote >= min_multiplier


@dataclass
class StrategyBundle:
    """
    A bundle of strategies with budget allocation.

    Contains multiple strategies across different risk levels.
    """

    strategies: list[Strategy]
    total_budget: float
    allocated_budget: float = 0.0
    generated_at: datetime = field(default_factory=datetime.now)

    @property
    def remaining_budget(self) -> float:
        """Calculate remaining unallocated budget."""
        return self.total_budget - self.allocated_budget

    def get_strategies_by_risk(self, risk_level: RiskLevel) -> list[Strategy]:
        """Get all strategies of a specific risk level."""
        return [s for s in self.strategies if s.risk_level == risk_level]


class StrategyEngine:
    """
    Strategy design engine implementing the Three Principles.

    The Three Principles (non-negotiable):
    1. Respect Probability Flow - All selections must have upward flow
    2. Respect Asymmetric Returns - Minimum 3x multiplier potential
    3. Respect Rules - Comply with all analysis constraints
    """

    MAX_COMBINATION_DEPTH_NO_SCORE = 8
    MAX_COMBINATION_DEPTH_WITH_SCORE = 4
    MAX_COMBINATION_DEPTH_WITH_HTFT = 4
    MAX_COMBINATION_DEPTH_WITH_TOTAL = 6
    MAX_MULTIPLIER = 99
    MAX_ALLOCATION = 20000
    MIN_ALLOCATION = 2.0
    MIN_MULTIPLIER_THRESHOLD = 3.0

    BUDGET_ALLOCATION = {
        RiskLevel.CONSERVATIVE: 0.20,
        RiskLevel.BALANCED: 0.45,
        RiskLevel.AGGRESSIVE: 0.25,
        RiskLevel.EXTREME: 0.10,
    }

    def __init__(self, config: Optional[dict] = None):
        """Initialize the strategy engine."""
        self.config = config or {}

    def validate_strategy(self, strategy: Strategy) -> tuple[ValidationResult, list[str]]:
        """Validate a strategy against all rules and principles."""
        errors = []

        if not strategy.has_upward_flow_selections_only():
            errors.append("Principle 1 violation: Selections must have upward flow")

        if not strategy.provides_meaningful_multiplier(self.MIN_MULTIPLIER_THRESHOLD):
            errors.append(
                f"Principle 2 violation: Combined quote {strategy.combined_quote:.2f} "
                f"below minimum {self.MIN_MULTIPLIER_THRESHOLD}"
            )

        match_markets: dict[str, set] = {}
        for sel in strategy.selections:
            if sel.match_id not in match_markets:
                match_markets[sel.match_id] = set()
            if sel.market_type in match_markets[sel.match_id]:
                errors.append(
                    f"Rule violation: Multiple selections from same match {sel.match_id}"
                )
            match_markets[sel.match_id].add(sel.market_type)

        has_score = any(
            sel.market_type == MarketType.CORRECT_SCORE for sel in strategy.selections
        )
        has_htft = any(
            sel.market_type == MarketType.HALF_FULL for sel in strategy.selections
        )
        max_depth = self.MAX_COMBINATION_DEPTH_NO_SCORE
        if has_score or has_htft:
            max_depth = self.MAX_COMBINATION_DEPTH_WITH_SCORE

        if len(strategy.selections) > max_depth:
            errors.append(
                f"Rule violation: Combination depth {len(strategy.selections)} exceeds max {max_depth}"
            )

        if strategy.multiplier > self.MAX_MULTIPLIER:
            errors.append(
                f"Rule violation: Multiplier {strategy.multiplier} exceeds max {self.MAX_MULTIPLIER}"
            )

        if strategy.total_allocation > self.MAX_ALLOCATION:
            errors.append(
                f"Rule violation: Total allocation {strategy.total_allocation} exceeds max {self.MAX_ALLOCATION}"
            )

        if strategy.allocation_per_combination < self.MIN_ALLOCATION:
            errors.append(
                f"Rule violation: Allocation {strategy.allocation_per_combination} below minimum {self.MIN_ALLOCATION}"
            )

        if errors:
            return (ValidationResult.INVALID, errors)
        return (ValidationResult.VALID, [])

    def _classify_risk_level(self, combined_quote: float) -> RiskLevel:
        """Classify risk level based on combined quote."""
        if combined_quote < 5:
            return RiskLevel.CONSERVATIVE
        elif combined_quote < 20:
            return RiskLevel.BALANCED
        elif combined_quote < 100:
            return RiskLevel.AGGRESSIVE
        else:
            return RiskLevel.EXTREME

    def generate_strategies(
        self,
        amplification_report: AmplificationReport,
        budget: float,
        match_data: dict,
        max_strategies: int = 10,
    ) -> StrategyBundle:
        """Generate optimized strategies within budget."""
        strategies = []
        reliable_amps = amplification_report.get_reliable_amplifications()
        reliable_amps.sort(key=lambda a: a.amplification_score, reverse=True)

        allocated = 0.0

        for amp in reliable_amps[:max_strategies]:
            selection = StrategySelection(
                match_id=amplification_report.match_id,
                market_type=MarketType.MATCH_RESULT,
                selection=amp.outcome,
                quote=3.0,
                flow_direction=FlowDirection.UPWARD,
                amplification_score=amp.amplification_score,
                confidence=amp.confidence,
            )

            strategy = Strategy(
                selections=[selection],
                combination_type="single",
                multiplier=1,
                allocation_per_combination=10.0,
                risk_level=self._classify_risk_level(3.0),
            )

            result, errors = self.validate_strategy(strategy)
            if result == ValidationResult.VALID:
                strategies.append(strategy)
                allocated += strategy.total_allocation

        return StrategyBundle(
            strategies=strategies,
            total_budget=budget,
            allocated_budget=allocated,
        )

    def optimize_budget_allocation(
        self, bundle: StrategyBundle
    ) -> StrategyBundle:
        """Optimize budget allocation across strategies."""
        total_score = sum(
            max(s.selections[0].amplification_score, 0.1) if s.selections else 0.1
            for s in bundle.strategies
        )

        for strategy in bundle.strategies:
            if strategy.selections:
                score = max(strategy.selections[0].amplification_score, 0.1)
                proportion = score / total_score
                target_budget = bundle.total_budget * proportion

                strategy.allocation_per_combination = min(
                    target_budget / strategy.num_combinations,
                    50.0,
                )
                strategy.allocation_per_combination = max(
                    strategy.allocation_per_combination,
                    self.MIN_ALLOCATION,
                )

        bundle.allocated_budget = sum(s.total_allocation for s in bundle.strategies)
        return bundle


__all__ = [
    "RiskLevel",
    "ValidationResult",
    "StrategySelection",
    "Strategy",
    "StrategyBundle",
    "StrategyEngine",
]

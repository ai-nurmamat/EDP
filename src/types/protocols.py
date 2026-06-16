"""
Expected Domain Perception - Type Definitions
期望域感知法 - 类型定义

This module contains type definitions and protocols for Expected Domain Perception.
"""

from __future__ import annotations

from typing import Protocol, TypeVar

T = TypeVar("T")


class ProbabilityCalculator(Protocol):
    """Protocol for probability calculation implementations."""

    def calculate(self, odds: dict[str, float]) -> dict[str, float]:
        """Calculate true probabilities from odds."""
        ...


class FlowAnalysisProvider(Protocol):
    """Protocol for flow analysis implementations."""

    def analyze(
        self, initial: dict[str, float], latest: dict[str, float]
    ) -> dict[str, float]:
        """Analyze probability flow between snapshots."""
        ...


class SchemeGenerator(Protocol):
    """Protocol for scheme generation implementations."""

    def generate(self, budget: float, constraints: dict) -> list:
        """Generate schemes within budget."""
        ...


class Validator(Protocol):
    """Protocol for validation implementations."""

    def validate(self, data: T) -> tuple[bool, list[str]]:
        """Validate data and return result with errors."""
        ...

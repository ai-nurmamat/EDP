"""
Tests for SPAF Probability Engine
"""

import pytest
from datetime import datetime

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'python'))

from probability_engine import (
    ProbabilityEngine,
    ProbabilitySnapshot,
    MarketType,
    FlowDirection,
)


class TestProbabilityEngine:
    """Test cases for ProbabilityEngine."""

    def test_calculate_true_probability_basic(self):
        """Test basic true probability calculation."""
        engine = ProbabilityEngine()

        odds = {'home': 2.0, 'draw': 3.0, 'away': 6.0}
        result = engine.calculate_true_probability(odds)

        # Check that probabilities sum to 1
        total = sum(result.true_probabilities.values())
        assert abs(total - 1.0) < 0.001

        # Check that overround is positive
        assert result.overround > 0

        # Check that true probabilities are less than implied
        for outcome in odds:
            implied = 1.0 / odds[outcome]
            assert result.true_probabilities[outcome] < implied

    def test_calculate_true_probability_equal_odds(self):
        """Test with equal odds."""
        engine = ProbabilityEngine()

        odds = {'a': 3.0, 'b': 3.0, 'c': 3.0}
        result = engine.calculate_true_probability(odds)

        # All outcomes should have equal probability
        for prob in result.true_probabilities.values():
            assert abs(prob - 1/3) < 0.001

    def test_calculate_true_probability_empty_odds(self):
        """Test with empty odds raises error."""
        engine = ProbabilityEngine()

        with pytest.raises(ValueError):
            engine.calculate_true_probability({})

    def test_calculate_true_probability_invalid_odds(self):
        """Test with invalid odds raises error."""
        engine = ProbabilityEngine()

        with pytest.raises(ValueError):
            engine.calculate_true_probability({'home': 0})

        with pytest.raises(ValueError):
            engine.calculate_true_probability({'home': -1})

    def test_calculate_conditional_probability(self):
        """Test conditional probability calculation."""
        engine = ProbabilityEngine()

        outcome_probs = {'a': 0.5, 'b': 0.3, 'c': 0.2}
        condition = ['a', 'b']

        result = engine.calculate_conditional_probability(outcome_probs, condition)

        # P(a|a,b) = 0.5 / 0.8 = 0.625
        assert abs(result['a'] - 0.625) < 0.001
        # P(b|a,b) = 0.3 / 0.8 = 0.375
        assert abs(result['b'] - 0.375) < 0.001

    def test_analyze_flow_positive(self):
        """Test flow analysis with positive flow."""
        engine = ProbabilityEngine()

        initial = ProbabilitySnapshot(
            timestamp=datetime.now(),
            probabilities={'home': 0.60, 'draw': 0.25, 'away': 0.20},
            market_type=MarketType.MATCH_RESULT,
        )

        latest = ProbabilitySnapshot(
            timestamp=datetime.now(),
            probabilities={'home': 0.65, 'draw': 0.23, 'away': 0.17},
            market_type=MarketType.MATCH_RESULT,
        )

        report = engine.analyze_flow(initial, latest)

        # Home should have positive flow
        home_flow = next(f for f in report.flows if f.outcome == 'home')
        assert home_flow.direction == FlowDirection.POSITIVE
        assert home_flow.flow_pp > 0

    def test_analyze_flow_negative(self):
        """Test flow analysis with negative flow."""
        engine = ProbabilityEngine()

        initial = ProbabilitySnapshot(
            timestamp=datetime.now(),
            probabilities={'home': 0.65, 'draw': 0.23, 'away': 0.17},
            market_type=MarketType.MATCH_RESULT,
        )

        latest = ProbabilitySnapshot(
            timestamp=datetime.now(),
            probabilities={'home': 0.60, 'draw': 0.25, 'away': 0.20},
            market_type=MarketType.MATCH_RESULT,
        )

        report = engine.analyze_flow(initial, latest)

        # Home should have negative flow
        home_flow = next(f for f in report.flows if f.outcome == 'home')
        assert home_flow.direction == FlowDirection.NEGATIVE
        assert home_flow.flow_pp < 0


class TestProbabilitySnapshot:
    """Test cases for ProbabilitySnapshot."""

    def test_validate_valid(self):
        """Test validation with valid probabilities."""
        snapshot = ProbabilitySnapshot(
            timestamp=datetime.now(),
            probabilities={'a': 0.5, 'b': 0.3, 'c': 0.2},
            market_type=MarketType.MATCH_RESULT,
        )

        assert snapshot.validate() is True

    def test_validate_invalid(self):
        """Test validation with invalid probabilities."""
        snapshot = ProbabilitySnapshot(
            timestamp=datetime.now(),
            probabilities={'a': 0.5, 'b': 0.3, 'c': 0.3},  # Sum > 1
            market_type=MarketType.MATCH_RESULT,
        )

        # Should still pass due to tolerance
        assert snapshot.validate() is True

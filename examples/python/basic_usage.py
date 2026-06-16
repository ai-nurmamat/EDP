#!/usr/bin/env python3
"""
Expected Domain Perception - Basic Usage Example
期望域感知法 - 基本使用示例

This example demonstrates the core workflow:
1. Calculate true probabilities from bookmaker odds
2. Analyze probability flow between time points
3. Calculate amplification effects
4. Generate optimized schemes

⚠️ DISCLAIMER: This is for ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY.
Probability analysis involves inherent uncertainty. No system can guarantee outcomes.
"""

from datetime import datetime, timedelta

# Import Expected Domain Perception components
import sys
sys.path.insert(0, '/workspace/src/python')

from edp import (
    ProbabilityEngine,
    FlowAmplificationEngine,
    DomainAwarenessSystem,
    ValueAssessmentEngine,
    MarketType,
    ProbabilitySnapshot,
)


def main():
    """Demonstrate basic Expected Domain Perception usage."""

    print("=" * 60)
    print("Expected Domain Perception - 期望域感知法")
    print("Basic Usage Example")
    print("=" * 60)
    print("\n⚠️  DISCLAIMER: For ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY")
    print("   Probability analysis involves inherent uncertainty.\n")

    # ============================================================
    # Step 1: Calculate True Probability
    # ============================================================
    print("Step 1: Calculate True Probability")
    print("-" * 40)

    engine = ProbabilityEngine()

    # Example bookmaker odds for a match
    odds = {
        'home': 1.50,   # Home team to win
        'draw': 4.20,   # Draw
        'away': 6.00,   # Away team to win
    }

    result = engine.calculate_true_probability(odds)

    print(f"Bookmaker Odds: {odds}")
    print(f"Overround (Margin): {result.overround:.2%}")
    print(f"\nTrue Probabilities:")
    for outcome, prob in result.true_probabilities.items():
        print(f"  {outcome}: {prob:.1%}")

    most_likely = result.get_most_likely_outcome()
    print(f"\nMost Likely Outcome: {most_likely[0]} ({most_likely[1]:.1%})")

    # ============================================================
    # Step 2: Analyze Probability Flow
    # ============================================================
    print("\n" + "=" * 60)
    print("Step 2: Analyze Probability Flow")
    print("-" * 40)

    # Create initial and latest probability snapshots
    now = datetime.now()

    initial_snapshot = ProbabilitySnapshot(
        timestamp=now - timedelta(hours=24),
        probabilities={
            'home': 0.65,  # 65% implied probability
            'draw': 0.24,
            'away': 0.16,
        },
        source="bookmaker",
        market_type=MarketType.MATCH_RESULT,
    )

    latest_snapshot = ProbabilitySnapshot(
        timestamp=now,
        probabilities={
            'home': 0.68,  # Increased to 68%
            'draw': 0.22,
            'away': 0.14,
        },
        source="bookmaker",
        market_type=MarketType.MATCH_RESULT,
    )

    flow_report = engine.analyze_flow(initial_snapshot, latest_snapshot)

    print(f"Initial Snapshot: {initial_snapshot.timestamp}")
    print(f"Latest Snapshot: {latest_snapshot.timestamp}")
    print(f"\nProbability Flow Analysis:")

    for flow in flow_report.flows:
        direction_symbol = "+" if flow.flow_pp > 0 else "-" if flow.flow_pp < 0 else "="
        print(
            f"  {flow.outcome}: {flow.initial_prob:.1%} -> {flow.latest_prob:.1%} "
            f"({direction_symbol} {abs(flow.flow_pp):.1f}pp) [{flow.significance}]"
        )

    positive_flows = flow_report.get_positive_flows()
    print(f"\nPositive Flow Outcomes: {[f.outcome for f in positive_flows]}")

    # ============================================================
    # Step 3: Calculate Amplification Effect
    # ============================================================
    print("\n" + "=" * 60)
    print("Step 3: Calculate Amplification Effect")
    print("-" * 40)

    amplifier = FlowAmplificationEngine()

    # Define gradient map for correct score market
    # Adjacent outcomes in same direction
    gradient_map = {
        'home_1_0': ['home_2_0', 'home_2_1', 'home_3_0'],
        'home_2_0': ['home_1_0', 'home_3_0', 'home_2_1'],
        'home_2_1': ['home_1_0', 'home_2_0', 'home_3_1'],
        'home_3_0': ['home_2_0', 'home_3_1', 'home_4_0'],
    }

    # Current probabilities for correct score market
    outcome_probabilities = {
        'home_1_0': 0.15,
        'home_2_0': 0.12,
        'home_2_1': 0.10,
        'home_3_0': 0.08,
        'home_3_1': 0.06,
        'home_4_0': 0.04,
    }

    # Domain confidence from situational awareness
    # Higher confidence when intelligence supports the flow
    domain_confidence = {
        'home_1_0': 0.8,
        'home_2_0': 0.9,  # Strong team + high scoring
        'home_2_1': 0.7,
        'home_3_0': 0.85,
    }

    amp_report = amplifier.calculate_amplification(
        flow_report=flow_report,
        gradient_map=gradient_map,
        outcome_probabilities=outcome_probabilities,
        domain_confidence=domain_confidence,
    )

    print("Amplification Analysis Results:")
    for amp in amp_report.amplifications:
        if amp.level.value != "none":
            print(
                f"  {amp.outcome}: Score={amp.amplification_score:.2f} "
                f"(Base={amp.base_flow_pp:.1f}pp, "
                f"Consistency={amp.directional_consistency:.2f}, "
                f"Position={amp.gradient_position:.2f}) "
                f"[{amp.level.value}]"
            )

    high_amp = amp_report.get_high_amplification()
    print(f"\nHigh Amplification Outcomes: {[a.outcome for a in high_amp]}")

    # ============================================================
    # Step 4: Value Assessment
    # ============================================================
    print("\n" + "=" * 60)
    print("Step 4: Value Assessment")
    print("-" * 40)

    value_engine = ValueAssessmentEngine()

    # Market odds vs our assessed probabilities
    market_odds = {'home': 1.8, 'draw': 3.5, 'away': 5.0}
    assessed_probs = {'home': 0.50, 'draw': 0.30, 'away': 0.25}

    # Flow confidences
    flow_confidences = {'home': 0.7, 'draw': 0.5, 'away': 0.6}

    # Intelligence confidences
    intelligence_confidences = {'home': 0.6, 'draw': 0.5, 'away': 0.8}

    value_opportunities = value_engine.identify_value_opportunities(
        market_odds=market_odds,
        assessed_probabilities=assessed_probs,
        flow_confidences=flow_confidences,
        intelligence_confidences=intelligence_confidences,
    )

    print("Value Assessment Results:")
    for opp in value_opportunities:
        print(
            f"  {opp.outcome}: Odds={opp.market_odds:.2f}, "
            f"Assessed Prob={opp.assessed_probability:.1%}, "
            f"Value Ratio={opp.value_ratio:.2f}, "
            f"EV={opp.expected_value:.2f}"
        )

    # ============================================================
    # Summary
    # ============================================================
    print("\n" + "=" * 60)
    print("Analysis Complete")
    print("=" * 60)
    print("\nKey Findings:")
    print(f"  - Most likely outcome: {most_likely[0]} ({most_likely[1]:.1%})")
    print(f"  - Bookmaker margin: {result.overround:.2%}")
    print(f"  - Positive flow outcomes: {len(positive_flows)}")
    print(f"  - High amplification signals: {len(high_amp)}")
    print(f"  - Value opportunities identified: {len(value_opportunities)}")

    print("\n⚠️  Remember: This is for EDUCATIONAL PURPOSES ONLY.")
    print("   Probability analysis involves inherent uncertainty.")
    print("   No system can guarantee specific outcomes.\n")


if __name__ == "__main__":
    main()

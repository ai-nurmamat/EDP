#!/usr/bin/env python3
"""
SPAF Framework - Basic Usage Example

This example demonstrates the core workflow:
1. Calculate true probabilities from market quotes
2. Analyze probability flow between time points
3. Calculate amplification effects
4. Generate optimized analysis strategies

⚠️ DISCLAIMER: This is for ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY.
"""

from datetime import datetime, timedelta

import sys
sys.path.insert(0, '/workspace/src/python')

from spaf import (
    ProbabilityEngine,
    FlowAmplificationEngine,
    StrategyEngine,
    DomainAwarenessSystem,
    MarketType,
    ProbabilitySnapshot,
    TeamIntelligence,
    MatchIntelligence,
)


def main():
    """Demonstrate basic SPAF framework usage."""

    print("=" * 60)
    print("SPAF - Sports Analytics Framework")
    print("Basic Usage Example")
    print("=" * 60)
    print("\n⚠️  DISCLAIMER: For ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY")
    print("   This framework is intended for statistical analysis.\n")

    # ============================================================
    # Step 1: Calculate True Probability
    # ============================================================
    print("Step 1: Calculate True Probability")
    print("-" * 40)

    engine = ProbabilityEngine()

    market_quotes = {
        'home': 1.50,
        'draw': 4.20,
        'away': 6.00,
    }

    result = engine.calculate_true_probability(market_quotes)

    print(f"Market Quotes: {market_quotes}")
    print(f"Market Margin: {result.market_margin:.2%}")
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

    now = datetime.now()

    initial_snapshot = ProbabilitySnapshot(
        timestamp=now - timedelta(hours=24),
        probabilities={
            'home': 0.65,
            'draw': 0.24,
            'away': 0.16,
        },
        source="market_data",
        market_type=MarketType.MATCH_RESULT,
    )

    latest_snapshot = ProbabilitySnapshot(
        timestamp=now,
        probabilities={
            'home': 0.68,
            'draw': 0.22,
            'away': 0.14,
        },
        source="market_data",
        market_type=MarketType.MATCH_RESULT,
    )

    flow_report = engine.analyze_flow(initial_snapshot, latest_snapshot)

    print(f"Initial Snapshot: {initial_snapshot.timestamp}")
    print(f"Latest Snapshot: {latest_snapshot.timestamp}")
    print(f"\nProbability Flow Analysis:")

    for flow in flow_report.flows:
        direction_symbol = "↑" if flow.flow_pp > 0 else "↓" if flow.flow_pp < 0 else "→"
        print(
            f"  {flow.outcome}: {flow.initial_prob:.1%} → {flow.latest_prob:.1%} "
            f"({direction_symbol} {flow.flow_pp:+.1f}pp) [{flow.significance}]"
        )

    upward_flows = flow_report.get_upward_flows()
    print(f"\nUpward Flow Outcomes: {[f.outcome for f in upward_flows]}")

    # ============================================================
    # Step 3: Calculate Amplification Effect
    # ============================================================
    print("\n" + "=" * 60)
    print("Step 3: Calculate Amplification Effect")
    print("-" * 40)

    amplifier = FlowAmplificationEngine()

    gradient_graph = type('GradientGraph', (), {
        'get_adjacent_outcomes': lambda self, x: {
            'home': ['draw'],
            'draw': ['home', 'away'],
            'away': ['draw'],
        }.get(x, []),
        'nodes': ['home', 'draw', 'away'],
        'edges': [],
    })()

    outcome_probabilities = {
        'home': 0.63,
        'draw': 0.23,
        'away': 0.14,
    }

    amp_report = amplifier.calculate_amplification(
        flow_report=flow_report,
        outcome_probabilities=outcome_probabilities,
        gradient_graph=gradient_graph,
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
    # Step 4: Domain Awareness Analysis
    # ============================================================
    print("\n" + "=" * 60)
    print("Step 4: Domain Awareness Analysis")
    print("-" * 40)

    awareness = DomainAwarenessSystem()

    home_team = TeamIntelligence(
        team_id='team_a',
        team_name='Team A',
        ranking=10,
        recent_results=['W', 'W', 'D', 'W', 'L'],
        recent_goals_scored=[2, 3, 1, 4, 1],
        recent_goals_conceded=[0, 1, 1, 0, 2],
        home_advantage=0.15,
        key_players_available=10,
        key_players_total=11,
        rest_days=7,
    )

    away_team = TeamIntelligence(
        team_id='team_b',
        team_name='Team B',
        ranking=35,
        recent_results=['L', 'D', 'L', 'W', 'D'],
        recent_goals_scored=[0, 1, 1, 2, 1],
        recent_goals_conceded=[2, 1, 3, 0, 1],
        away_performance=-0.05,
        key_players_available=9,
        key_players_total=11,
        rest_days=3,
    )

    match_intel = MatchIntelligence(
        match_id='example_match_001',
        home_team=home_team,
        away_team=away_team,
        competition='International Friendly',
        h2h_home_wins=8,
        h2h_draws=5,
        h2h_away_wins=3,
    )

    flow_confidences = {
        'home_win': 0.63,
        'draw': 0.23,
        'away_win': 0.14,
    }

    domain_report = awareness.analyze_match(match_intel, flow_confidences)

    print(f"Overall Confidence: {domain_report.final_confidence.value.upper()}")
    print("\nConfidence Scores:")
    for outcome, confidence in domain_report.confidence_scores.items():
        print(f"  {outcome}: {confidence:.1%}")

    print("\nRecommendations:")
    for rec in domain_report.recommendations:
        print(f"  • {rec}")

    # ============================================================
    # Step 5: Generate Strategies
    # ============================================================
    print("\n" + "=" * 60)
    print("Step 5: Generate Analysis Strategies")
    print("-" * 40)

    strategy_engine = StrategyEngine()

    match_data = {
        'match_id': 'example_match_001',
        'home_team': 'Team A',
        'away_team': 'Team B',
    }

    bundle = strategy_engine.generate_strategies(
        amplification_report=amp_report,
        budget=100,
        match_data=match_data,
        max_strategies=5,
    )

    print(f"Total Budget: ¥{bundle.total_budget}")
    print(f"Allocated Budget: ¥{bundle.allocated_budget:.2f}")
    print(f"Number of Strategies: {len(bundle.strategies)}")

    for i, strategy in enumerate(bundle.strategies, 1):
        print(f"\n  Strategy {i}:")
        print(f"    Type: {strategy.combination_type}")
        print(f"    Risk Level: {strategy.risk_level.value}")
        print(f"    Selections: {[sel.selection for sel in strategy.selections]}")
        print(f"    Combined Quote: {strategy.combined_quote:.2f}x")
        print(f"    Allocation: ¥{strategy.allocation_per_combination:.2f}")
        print(f"    Total Allocation: ¥{strategy.total_allocation:.2f}")

    # ============================================================
    # Summary
    # ============================================================
    print("\n" + "=" * 60)
    print("Analysis Complete")
    print("=" * 60)
    print("\nKey Findings:")
    print(f"  • Most likely outcome: {most_likely[0]} ({most_likely[1]:.1%})")
    print(f"  • Market margin: {result.market_margin:.2%}")
    print(f"  • Upward flow outcomes: {len(upward_flows)}")
    print(f"  • High amplification signals: {len(high_amp)}")
    print(f"  • Domain confidence level: {domain_report.final_confidence.value.upper()}")
    print(f"  • Generated strategies: {len(bundle.strategies)}")

    print("\n⚠️  Remember: This is for EDUCATIONAL PURPOSES ONLY.")
    print("   Statistical analysis does not guarantee future results.\n")


if __name__ == "__main__":
    main()

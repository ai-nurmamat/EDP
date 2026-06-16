#!/usr/bin/env node
/**
 * Expected Domain Perception - Basic Usage Example (TypeScript/JavaScript)
 *
 * This example demonstrates the core workflow:
 * 1. Calculate true probabilities from bookmaker odds
 * 2. Analyze probability flow between time points
 * 3. Calculate amplification effects
 * 4. Generate optimized schemes
 *
 * ⚠️ DISCLAIMER: This is for ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY.
 * Sports prediction involves real financial risk. No system can guarantee profits.
 */

import {
  ProbabilityEngine,
  FlowAnalyzer,
  SchemeDesigner,
  MarketType,
  FlowDirection,
  RiskLevel,
  AmplificationLevel,
} from '../src/js/index';

function main(): void {
  console.log('='.repeat(60));
  console.log('Expected Domain Perception - 期望域感知法');
  console.log('Basic Usage Example (TypeScript/JavaScript)');
  console.log('='.repeat(60));
  console.log('\n⚠️  DISCLAIMER: For ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY');
  console.log('   Sports prediction involves real financial risk.\n');

  // ============================================================
  // Step 1: Calculate True Probability
  // ============================================================
  console.log('Step 1: Calculate True Probability');
  console.log('-'.repeat(40));

  const engine = new ProbabilityEngine();

  // Example bookmaker odds for a match
  const odds = {
    home: 1.50,
    draw: 4.20,
    away: 6.00,
  };

  const result = engine.calculateTrueProbability(odds);

  console.log(`Bookmaker Odds: ${JSON.stringify(odds)}`);
  console.log(`Overround (Margin): ${(result.overround * 100).toFixed(2)}%`);
  console.log('\nTrue Probabilities:');
  for (const [outcome, prob] of Object.entries(result.trueProbabilities)) {
    console.log(`  ${outcome}: ${(prob * 100).toFixed(1)}%`);
  }

  // Find most likely outcome
  const entries = Object.entries(result.trueProbabilities);
  const mostLikely = entries.reduce((a, b) => (a[1] > b[1] ? a : b));
  console.log(`\nMost Likely Outcome: ${mostLikely[0]} (${(mostLikely[1] * 100).toFixed(1)}%)`);

  // ============================================================
  // Step 2: Analyze Probability Flow
  // ============================================================
  console.log('\n' + '='.repeat(60));
  console.log('Step 2: Analyze Probability Flow');
  console.log('-'.repeat(40));

  const now = new Date();
  const yesterday = new Date(now.getTime() - 24 * 60 * 60 * 1000);

  const initialSnapshot = {
    timestamp: yesterday,
    probabilities: {
      home: 0.65,
      draw: 0.24,
      away: 0.16,
    },
    source: 'bookmaker',
    marketType: MarketType.MATCH_RESULT,
  };

  const latestSnapshot = {
    timestamp: now,
    probabilities: {
      home: 0.68,
      draw: 0.22,
      away: 0.14,
    },
    source: 'bookmaker',
    marketType: MarketType.MATCH_RESULT,
  };

  const flowReport = engine.analyzeFlow(initialSnapshot, latestSnapshot);

  console.log(`Initial Snapshot: ${initialSnapshot.timestamp.toISOString()}`);
  console.log(`Latest Snapshot: ${latestSnapshot.timestamp.toISOString()}`);
  console.log('\nProbability Flow Analysis:');

  for (const flow of flowReport.flows) {
    const directionSymbol = flow.flowPp > 0 ? '↑' : flow.flowPp < 0 ? '↓' : '→';
    console.log(
      `  ${flow.outcome}: ${(flow.initialProb * 100).toFixed(1)}% → ` +
        `${(flow.latestProb * 100).toFixed(1)}% ` +
        `(${directionSymbol} ${flow.flowPp >= 0 ? '+' : ''}${flow.flowPp.toFixed(1)}pp) ` +
        `[${flow.significance}]`
    );
  }

  const positiveFlows = flowReport.flows.filter(
    (f) => f.direction === FlowDirection.POSITIVE
  );
  console.log(
    `\nPositive Flow Outcomes: ${positiveFlows.map((f) => f.outcome).join(', ')}`
  );

  // ============================================================
  // Step 3: Calculate Amplification Effect
  // ============================================================
  console.log('\n' + '='.repeat(60));
  console.log('Step 3: Calculate Amplification Effect');
  console.log('-'.repeat(40));

  const analyzer = new FlowAnalyzer();

  // Define gradient map for correct score market
  const gradientMap: Record<string, string[]> = {
    home_1_0: ['home_2_0', 'home_2_1', 'home_3_0'],
    home_2_0: ['home_1_0', 'home_3_0', 'home_2_1'],
    home_2_1: ['home_1_0', 'home_2_0', 'home_3_1'],
    home_3_0: ['home_2_0', 'home_3_1', 'home_4_0'],
  };

  // Current probabilities for correct score market
  const outcomeProbabilities: Record<string, number> = {
    home_1_0: 0.15,
    home_2_0: 0.12,
    home_2_1: 0.10,
    home_3_0: 0.08,
    home_3_1: 0.06,
    home_4_0: 0.04,
  };

  // Domain confidence from situational awareness
  const domainConfidence: Record<string, number> = {
    home_1_0: 0.8,
    home_2_0: 0.9,
    home_2_1: 0.7,
    home_3_0: 0.85,
  };

  const ampReport = analyzer.calculateAmplification(
    flowReport,
    gradientMap,
    outcomeProbabilities,
    domainConfidence
  );

  console.log('Amplification Analysis Results:');
  for (const amp of ampReport.amplifications) {
    if (amp.level !== AmplificationLevel.NONE) {
      console.log(
        `  ${amp.outcome}: Score=${amp.amplificationScore.toFixed(2)} ` +
          `(Base=${amp.baseFlowPp.toFixed(1)}pp, ` +
          `Consistency=${amp.directionalConsistency.toFixed(2)}, ` +
          `Position=${amp.gradientPosition.toFixed(2)}) ` +
          `[${amp.level}]`
      );
    }
  }

  const highAmp = ampReport.amplifications.filter(
    (a) => a.level === AmplificationLevel.HIGH || a.level === AmplificationLevel.VERY_HIGH
  );
  console.log(`\nHigh Amplification Outcomes: ${highAmp.map((a) => a.outcome).join(', ')}`);

  // ============================================================
  // Step 4: Generate Schemes
  // ============================================================
  console.log('\n' + '='.repeat(60));
  console.log('Step 4: Generate Optimized Schemes');
  console.log('-'.repeat(40));

  const designer = new SchemeDesigner();

  const matchData = {
    matchId: 'example_match_001',
    homeTeam: 'Team A',
    awayTeam: 'Team B',
  };

  const bundle = designer.generateSchemes(ampReport, 100, matchData, 5);

  console.log(`Total Budget: ¥${bundle.totalBudget}`);
  console.log(`Allocated Budget: ¥${bundle.allocatedBudget.toFixed(2)}`);
  console.log(`Number of Schemes: ${bundle.schemes.length}`);

  for (let i = 0; i < bundle.schemes.length; i++) {
    const scheme = bundle.schemes[i];
    const combinedOdds = scheme.legs.reduce((acc, leg) => acc * leg.odds, 1);
    const totalCost = scheme.stakePerCombination * scheme.multiplier;
    const potentialReturn = totalCost * (combinedOdds - 1);

    console.log(`\n  Scheme ${i + 1}:`);
    console.log(`    Type: ${scheme.combinationType}`);
    console.log(`    Risk Level: ${scheme.riskLevel}`);
    console.log(`    Legs: ${scheme.legs.map((l) => l.selection).join(', ')}`);
    console.log(`    Combined Odds: ${combinedOdds.toFixed(2)}x`);
    console.log(`    Stake: ¥${scheme.stakePerCombination.toFixed(2)}`);
    console.log(`    Total Cost: ¥${totalCost.toFixed(2)}`);
    console.log(`    Potential Return: ¥${potentialReturn.toFixed(2)}`);
  }

  // ============================================================
  // Summary
  // ============================================================
  console.log('\n' + '='.repeat(60));
  console.log('Analysis Complete');
  console.log('='.repeat(60));
  console.log('\nKey Findings:');
  console.log(`  • Most likely outcome: ${mostLikely[0]} (${(mostLikely[1] * 100).toFixed(1)}%)`);
  console.log(`  • Bookmaker margin: ${(result.overround * 100).toFixed(2)}%`);
  console.log(`  • Positive flow outcomes: ${positiveFlows.length}`);
  console.log(`  • High amplification signals: ${highAmp.length}`);
  console.log(`  • Generated schemes: ${bundle.schemes.length}`);

  console.log('\n⚠️  Remember: This is for EDUCATIONAL PURPOSES ONLY.');
  console.log('   No system can guarantee profits in sports prediction.');
  console.log('   Always gamble responsibly.\n');
}

// Run the example
main();

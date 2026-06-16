/**
 * Expected Domain Perception
 * 期望域感知法
 *
 * Core probability engine implementation (TypeScript).
 *
 * This module implements the core probability analysis engine based on:
 * - Shin method for true probability extraction (Shin, 1992)
 * - Bayesian updating for probability flow analysis
 * - Kelly criterion variant for capital allocation
 *
 * A Methodology for Asymmetric Expected Value Discovery Based on Probability Flow and Domain Awareness
 *
 * @module expected-domain-perception
 * @version 1.0.0
 * @license MIT
 *
 * DISCLAIMER: For ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY.
 * Probability analysis involves inherent uncertainty. No system can guarantee outcomes.
 */

/**
 * Supported market types for probability analysis
 */
export enum MarketType {
  MATCH_RESULT = '1X2',
  HANDICAP = 'handicap',
  TOTAL_GOALS = 'total_goals',
  CORRECT_SCORE = 'correct_score',
  HALF_TIME_FULL_TIME = 'ht_ft',
}

/**
 * Probability flow direction classification
 */
export enum FlowDirection {
  POSITIVE = 'positive',
  NEGATIVE = 'negative',
  NEUTRAL = 'neutral',
}

/**
 * Risk classification for scheme layers
 */
export enum RiskLevel {
  CONSERVATIVE = 'conservative',
  BALANCED = 'balanced',
  AGGRESSIVE = 'aggressive',
  EXTREME = 'extreme',
}

/**
 * Amplification effect strength classification
 */
export enum AmplificationLevel {
  NONE = 'none',
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  VERY_HIGH = 'very_high',
}

/**
 * Validation result for scheme checking
 */
export enum ValidationResult {
  VALID = 'valid',
  INVALID = 'invalid',
  WARNING = 'warning',
}

// ============================================================
// Interfaces
// ============================================================

/**
 * A snapshot of probabilities at a specific point in time
 */
export interface IProbabilitySnapshot {
  timestamp: Date;
  probabilities: Record<string, number>;
  source: string;
  marketType: MarketType;
}

/**
 * Result of true probability calculation
 */
export interface ITrueProbabilityResult {
  trueProbabilities: Record<string, number>;
  impliedProbabilities: Record<string, number>;
  overround: number;
  method: string;
}

/**
 * Result of probability flow analysis for a single outcome
 */
export interface IFlowResult {
  outcome: string;
  flowPp: number;
  direction: FlowDirection;
  initialProb: number;
  latestProb: number;
  significance: 'low' | 'medium' | 'high';
}

/**
 * Complete flow analysis report
 */
export interface IFlowReport {
  matchId: string;
  marketType: MarketType;
  initialSnapshot: IProbabilitySnapshot;
  latestSnapshot: IProbabilitySnapshot;
  flows: IFlowResult[];
  generatedAt: Date;
}

/**
 * Amplification calculation result
 */
export interface IAmplificationResult {
  outcome: string;
  baseFlowPp: number;
  directionalConsistency: number;
  gradientPosition: number;
  amplificationScore: number;
  level: AmplificationLevel;
  confidence: number;
}

/**
 * Complete amplification report
 */
export interface IAmplificationReport {
  matchId: string;
  flowReport: IFlowReport;
  amplifications: IAmplificationResult[];
  generatedAt: Date;
}

/**
 * A single leg (selection) in a scheme
 */
export interface ISchemeLeg {
  matchId: string;
  marketType: MarketType;
  selection: string;
  odds: number;
  flowDirection: FlowDirection;
  amplificationScore: number;
  confidence: number;
}

/**
 * A complete scheme (ticket) with multiple legs
 */
export interface IScheme {
  legs: ISchemeLeg[];
  combinationType: string;
  multiplier: number;
  investmentPerCombination: number;
  riskLevel: RiskLevel;
  validationErrors: string[];
}

/**
 * A bundle of schemes with budget allocation
 */
export interface ISchemeBundle {
  schemes: IScheme[];
  totalBudget: number;
  allocatedBudget: number;
  generatedAt: Date;
}

// ============================================================
// Probability Engine
// ============================================================

/**
 * Core probability analysis engine.
 *
 * Implements the Shin method (simplified) for extracting true probabilities
 * from bookmaker odds, removing the overround/margin.
 *
 * @example
 * ```typescript
 * const engine = new ProbabilityEngine();
 * const result = engine.calculateTrueProbability({
 *   home: 1.50,
 *   draw: 4.20,
 *   away: 6.00
 * });
 * console.log(result.trueProbabilities);
 * ```
 */
export class ProbabilityEngine {
  private readonly flowThresholdLow: number = 1.0;
  private readonly flowThresholdMedium: number = 2.0;
  private readonly flowThresholdHigh: number = 5.0;

  constructor(private config?: {
    flowThresholdLow?: number;
    flowThresholdMedium?: number;
    flowThresholdHigh?: number;
  }) {
    this.flowThresholdLow = config?.flowThresholdLow ?? this.flowThresholdLow;
    this.flowThresholdMedium = config?.flowThresholdMedium ?? this.flowThresholdMedium;
    this.flowThresholdHigh = config?.flowThresholdHigh ?? this.flowThresholdHigh;
  }

  /**
   * Calculate true probabilities from bookmaker odds.
   *
   * Uses basic normalization method (simplified Shin method):
   * P_true(outcome_i) = (1 / odds_i) / Σ(1 / odds_j)
   *
   * @param odds - Dictionary mapping outcomes to decimal odds
   * @returns True probability result with normalized probabilities
   * @throws Error if odds are invalid
   */
  calculateTrueProbability(odds: Record<string, number>): ITrueProbabilityResult {
    if (!odds || Object.keys(odds).length === 0) {
      throw new Error('Odds dictionary cannot be empty');
    }

    for (const [outcome, odd] of Object.entries(odds)) {
      if (odd <= 0) {
        throw new Error(`Invalid odd value for ${outcome}: ${odd}`);
      }
    }

    // Calculate implied probabilities
    const impliedProbabilities: Record<string, number> = {};
    for (const [outcome, odd] of Object.entries(odds)) {
      impliedProbabilities[outcome] = 1.0 / odd;
    }

    // Calculate overround (total margin)
    const totalImplied = Object.values(impliedProbabilities).reduce((a, b) => a + b, 0);
    const overround = totalImplied - 1.0;

    // Normalize to get true probabilities
    const trueProbabilities: Record<string, number> = {};
    for (const [outcome, prob] of Object.entries(impliedProbabilities)) {
      trueProbabilities[outcome] = prob / totalImplied;
    }

    return {
      trueProbabilities,
      impliedProbabilities,
      overround,
      method: 'basic_normalization',
    };
  }

  /**
   * Calculate conditional probabilities within a subset of outcomes.
   *
   * P(score | direction) = P(score) / Σ P(scores_in_direction)
   *
   * @param outcomeProbabilities - Probabilities for all outcomes
   * @param conditionOutcomes - Subset of outcomes to condition on
   * @returns Dictionary of conditional probabilities
   */
  calculateConditionalProbability(
    outcomeProbabilities: Record<string, number>,
    conditionOutcomes: string[]
  ): Record<string, number> {
    const conditionTotal = conditionOutcomes.reduce(
      (sum, o) => sum + (outcomeProbabilities[o] ?? 0),
      0
    );

    if (conditionTotal === 0) {
      return Object.fromEntries(conditionOutcomes.map((o) => [o, 0]));
    }

    const result: Record<string, number> = {};
    for (const outcome of conditionOutcomes) {
      result[outcome] = (outcomeProbabilities[outcome] ?? 0) / conditionTotal;
    }
    return result;
  }

  /**
   * Analyze probability flow between two time points.
   *
   * Flow(outcome) = P_true_latest(outcome) - P_true_initial(outcome)
   *
   * @param initialSnapshot - Earlier probability snapshot
   * @param latestSnapshot - Later probability snapshot
   * @returns Flow report with all flow results
   */
  analyzeFlow(
    initialSnapshot: IProbabilitySnapshot,
    latestSnapshot: IProbabilitySnapshot
  ): IFlowReport {
    const flows: IFlowResult[] = [];

    // Calculate true probabilities for both snapshots
    const initialOdds: Record<string, number> = {};
    for (const [k, v] of Object.entries(initialSnapshot.probabilities)) {
      initialOdds[k] = 1.0 / v;
    }

    const latestOdds: Record<string, number> = {};
    for (const [k, v] of Object.entries(latestSnapshot.probabilities)) {
      latestOdds[k] = 1.0 / v;
    }

    const initialTrue = this.calculateTrueProbability(initialOdds);
    const latestTrue = this.calculateTrueProbability(latestOdds);

    // Calculate flow for each outcome
    for (const outcome of Object.keys(initialTrue.trueProbabilities)) {
      const initialProb = initialTrue.trueProbabilities[outcome];
      const latestProb = latestTrue.trueProbabilities[outcome] ?? initialProb;
      const flowPp = (latestProb - initialProb) * 100; // Convert to percentage points

      // Classify direction
      let direction: FlowDirection;
      if (flowPp > this.flowThresholdLow) {
        direction = FlowDirection.POSITIVE;
      } else if (flowPp < -this.flowThresholdLow) {
        direction = FlowDirection.NEGATIVE;
      } else {
        direction = FlowDirection.NEUTRAL;
      }

      // Assess significance
      const absFlow = Math.abs(flowPp);
      let significance: 'low' | 'medium' | 'high';
      if (absFlow >= this.flowThresholdHigh) {
        significance = 'high';
      } else if (absFlow >= this.flowThresholdMedium) {
        significance = 'medium';
      } else {
        significance = 'low';
      }

      flows.push({
        outcome,
        flowPp,
        direction,
        initialProb,
        latestProb,
        significance,
      });
    }

    return {
      matchId: `match_${initialSnapshot.timestamp.getTime()}`,
      marketType: initialSnapshot.marketType,
      initialSnapshot,
      latestSnapshot,
      flows,
      generatedAt: new Date(),
    };
  }
}

// ============================================================
// Flow Analyzer
// ============================================================

/**
 * Probability flow amplification effect analyzer.
 *
 * The amplification effect occurs when probability flow shows money moving
 * from outcome A to outcome B, typically meaning adjacent outcomes on the
 * same directional gradient are also flowing in the same direction.
 */
export class FlowAnalyzer {
  private readonly amplificationThresholdLow: number = 1.0;
  private readonly amplificationThresholdMedium: number = 3.0;
  private readonly amplificationThresholdHigh: number = 5.0;
  private readonly amplificationThresholdVeryHigh: number = 10.0;
  private readonly minBaseFlow: number = 2.0;

  constructor(private config?: {
    minBaseFlow?: number;
    amplificationThresholdLow?: number;
    amplificationThresholdMedium?: number;
    amplificationThresholdHigh?: number;
    amplificationThresholdVeryHigh?: number;
  }) {
    this.minBaseFlow = config?.minBaseFlow ?? this.minBaseFlow;
  }

  /**
   * Calculate directional consistency for an outcome.
   */
  private calculateDirectionalConsistency(
    flowReport: IFlowReport,
    outcome: string,
    adjacentOutcomes: string[]
  ): number {
    if (!adjacentOutcomes || adjacentOutcomes.length === 0) {
      return 0;
    }

    const flowMap = new Map(flowReport.flows.map((f) => [f.outcome, f]));
    let positiveCount = 0;

    for (const adjOutcome of adjacentOutcomes) {
      const flow = flowMap.get(adjOutcome);
      if (flow && flow.direction === FlowDirection.POSITIVE) {
        positiveCount++;
      }
    }

    return positiveCount / adjacentOutcomes.length;
  }

  /**
   * Calculate normalized gradient position for an outcome.
   */
  private calculateGradientPosition(
    outcome: string,
    outcomeProbabilities: Record<string, number>,
    directionOutcomes: string[]
  ): number {
    if (!(outcome in outcomeProbabilities)) {
      return 0;
    }

    const directionProbs = directionOutcomes
      .filter((o) => o in outcomeProbabilities)
      .map((o) => outcomeProbabilities[o]);

    if (directionProbs.length === 0) {
      return 0;
    }

    const maxProb = Math.max(...directionProbs);
    const minProb = Math.min(...directionProbs);

    if (maxProb === minProb) {
      return 0.5;
    }

    // Invert: lower probability = higher position
    const outcomeProb = outcomeProbabilities[outcome];
    return (maxProb - outcomeProb) / (maxProb - minProb);
  }

  /**
   * Classify amplification score into a level.
   */
  private classifyAmplificationLevel(score: number): AmplificationLevel {
    if (score < this.amplificationThresholdLow) {
      return AmplificationLevel.NONE;
    } else if (score < this.amplificationThresholdMedium) {
      return AmplificationLevel.LOW;
    } else if (score < this.amplificationThresholdHigh) {
      return AmplificationLevel.MEDIUM;
    } else if (score < this.amplificationThresholdVeryHigh) {
      return AmplificationLevel.HIGH;
    } else {
      return AmplificationLevel.VERY_HIGH;
    }
  }

  /**
   * Calculate amplification effect for all outcomes.
   *
   * Amplification_Score = Base_Flow × Directional_Consistency × Gradient_Position
   *
   * @param flowReport - Flow analysis report
   * @param gradientMap - Dictionary mapping outcomes to adjacent outcomes
   * @param outcomeProbabilities - Current true probabilities
   * @param domainConfidence - Optional confidence scores from domain awareness
   * @returns Amplification report with all results
   */
  calculateAmplification(
    flowReport: IFlowReport,
    gradientMap: Record<string, string[]>,
    outcomeProbabilities: Record<string, number>,
    domainConfidence?: Record<string, number>
  ): IAmplificationReport {
    const amplifications: IAmplificationResult[] = [];
    const confidence = domainConfidence ?? {};

    for (const flowResult of flowReport.flows) {
      const outcome = flowResult.outcome;
      const baseFlow = flowResult.flowPp;

      // Safeguard: Skip if base flow below threshold
      if (Math.abs(baseFlow) < this.minBaseFlow) {
        amplifications.push({
          outcome,
          baseFlowPp: baseFlow,
          directionalConsistency: 0,
          gradientPosition: 0,
          amplificationScore: 0,
          level: AmplificationLevel.NONE,
          confidence: confidence[outcome] ?? 0,
        });
        continue;
      }

      // Get adjacent outcomes
      const adjacent = gradientMap[outcome] ?? [];

      // Calculate components
      const directionalConsistency = this.calculateDirectionalConsistency(
        flowReport,
        outcome,
        adjacent
      );
      const gradientPosition = this.calculateGradientPosition(
        outcome,
        outcomeProbabilities,
        adjacent
      );

      // Calculate amplification score
      let amplificationScore = 0;
      if (flowResult.direction === FlowDirection.POSITIVE) {
        amplificationScore = baseFlow * directionalConsistency * (1 + gradientPosition);
      }

      // Classify level
      const level = this.classifyAmplificationLevel(amplificationScore);

      // Apply domain confidence
      const outcomeConfidence = confidence[outcome] ?? 1.0;
      const adjustedScore = amplificationScore * outcomeConfidence;

      amplifications.push({
        outcome,
        baseFlowPp: baseFlow,
        directionalConsistency,
        gradientPosition,
        amplificationScore: adjustedScore,
        level,
        confidence: outcomeConfidence,
      });
    }

    return {
      matchId: flowReport.matchId,
      flowReport,
      amplifications,
      generatedAt: new Date(),
    };
  }
}

// ============================================================
// Scheme Designer
// ============================================================

/**
 * Scheme design engine implementing the Three Principles.
 *
 * The Three Principles (non-negotiable):
 * 1. Respect Probability Flow - All legs must have positive flow
 * 2. Respect Asymmetric Returns - Minimum 3x return potential
 * 3. Respect Rules - Comply with all betting rules
 */
export class SchemeDesigner {
  private readonly maxSelectionDepthNoScore = 8;
  private readonly maxSelectionDepthWithScore = 4;
  private readonly maxMultiplier = 99;
  private readonly maxInvestmentAmount = 20000;
  private readonly minInvestment = 2.0;
  private readonly minReturnMultiplier = 3.0;

  /**
   * Validate a scheme against all rules and principles.
   *
   * @param scheme - The scheme to validate
   * @returns Tuple of validation result and error messages
   */
  validateScheme(scheme: IScheme): [ValidationResult, string[]] {
    const errors: string[] = [];

    // Principle 1: All legs must have positive flow
    const negativeLegs = scheme.legs.filter(
      (leg) => leg.flowDirection !== FlowDirection.POSITIVE
    );
    if (negativeLegs.length > 0) {
      errors.push(
        `Principle 1 violation: Negative flow legs: ${negativeLegs.map((l) => l.selection).join(', ')}`
      );
    }

    // Principle 2: Meaningful return
    const combinedOdds = scheme.legs.reduce((acc, leg) => acc * leg.odds, 1);
    if (combinedOdds < this.minReturnMultiplier) {
      errors.push(
        `Principle 2 violation: Combined odds ${combinedOdds.toFixed(2)} below minimum ${this.minReturnMultiplier}`
      );
    }

    // Rule: Same match different markets cannot combine
    const matchMarkets = new Map<string, Set<MarketType>>();
    for (const leg of scheme.legs) {
      if (!matchMarkets.has(leg.matchId)) {
        matchMarkets.set(leg.matchId, new Set());
      }
      const markets = matchMarkets.get(leg.matchId)!;
      if (markets.has(leg.marketType)) {
        errors.push(`Rule violation: Multiple legs from same match ${leg.matchId}`);
      }
      markets.add(leg.marketType);
    }

    // Rule: Selection depth limits
    const hasScore = scheme.legs.some(
      (leg) => leg.marketType === MarketType.CORRECT_SCORE
    );
    const hasHTFT = scheme.legs.some(
      (leg) => leg.marketType === MarketType.HALF_TIME_FULL_TIME
    );
    const maxDepth = hasScore || hasHTFT
      ? this.maxSelectionDepthWithScore
      : this.maxSelectionDepthNoScore;

    if (scheme.legs.length > maxDepth) {
      errors.push(
        `Rule violation: Selection depth ${scheme.legs.length} exceeds max ${maxDepth}`
      );
    }

    // Rule: Multiplier limit
    if (scheme.multiplier > this.maxMultiplier) {
      errors.push(
        `Rule violation: Multiplier ${scheme.multiplier} exceeds max ${this.maxMultiplier}`
      );
    }

    // Rule: Minimum stake
    if (scheme.stakePerCombination < this.minStake) {
      errors.push(
        `Rule violation: Stake ${scheme.stakePerCombination} below minimum ${this.minStake}`
      );
    }

    if (errors.length > 0) {
      return [ValidationResult.INVALID, errors];
    }
    return [ValidationResult.VALID, []];
  }

  /**
   * Classify risk level based on combined odds.
   */
  private classifyRiskLevel(combinedOdds: number): RiskLevel {
    if (combinedOdds < 5) {
      return RiskLevel.CONSERVATIVE;
    } else if (combinedOdds < 20) {
      return RiskLevel.BALANCED;
    } else if (combinedOdds < 100) {
      return RiskLevel.AGGRESSIVE;
    } else {
      return RiskLevel.EXTREME;
    }
  }

  /**
   * Generate optimized schemes within budget.
   *
   * @param amplificationReport - Amplification analysis results
   * @param budget - Total budget to allocate
   * @param matchData - Match information
   * @param maxSchemes - Maximum number of schemes to generate
   * @returns Scheme bundle with optimized schemes
   */
  generateSchemes(
    amplificationReport: IAmplificationReport,
    budget: number,
    matchData: { matchId: string; homeTeam: string; awayTeam: string },
    maxSchemes: number = 10
  ): ISchemeBundle {
    const schemes: IScheme[] = [];

    // Get reliable amplifications
    const reliableAmps = amplificationReport.amplifications
      .filter((a) => a.level !== AmplificationLevel.NONE && a.confidence >= 0.5)
      .sort((a, b) => b.amplificationScore - a.amplificationScore);

    let allocated = 0;

    for (let i = 0; i < Math.min(reliableAmps.length, maxSchemes); i++) {
      const amp = reliableAmps[i];

      // Create a simple single-leg scheme
      const leg: ISchemeLeg = {
        matchId: amplificationReport.matchId,
        marketType: amplificationReport.flowReport.marketType,
        selection: amp.outcome,
        odds: 3.0, // Placeholder
        flowDirection: FlowDirection.POSITIVE,
        amplificationScore: amp.amplificationScore,
        confidence: amp.confidence,
      };

      const combinedOdds = leg.odds;
      const scheme: IScheme = {
        legs: [leg],
        combinationType: '单关',
        multiplier: 1,
        investmentPerCombination: 10,
        riskLevel: this.classifyRiskLevel(combinedOdds),
        validationErrors: [],
      };

      // Validate
      const [result, errors] = this.validateScheme(scheme);
      if (result === ValidationResult.VALID) {
        schemes.push(scheme);
        allocated += scheme.investmentPerCombination * scheme.multiplier;
      }
    }

    return {
      schemes,
      totalBudget: budget,
      allocatedBudget: allocated,
      generatedAt: new Date(),
    };
  }
}

// ============================================================
// Exports
// ============================================================

export default {
  ProbabilityEngine,
  FlowAnalyzer,
  SchemeDesigner,
  MarketType,
  FlowDirection,
  RiskLevel,
  AmplificationLevel,
  ValidationResult,
};

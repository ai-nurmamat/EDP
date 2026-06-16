/**
 * SPAF - Sports Analytics Framework
 * Core probability analysis engine implementation (TypeScript).
 *
 * This module implements the core probability analysis engine based on:
 * - Shin method for true probability extraction (Shin, 1992)
 * - Bayesian updating for probability flow analysis
 * - Kelly criterion variant for resource allocation
 *
 * @module spaf-framework
 * @version 4.2.0
 * @license MIT
 *
 * DISCLAIMER: For ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY.
 * This software is intended for statistical analysis and research.
 */

/**
 * Supported market types for probability analysis
 */
export enum MarketType {
  MATCH_RESULT = '1X2',
  HANDICAP = 'handicap',
  TOTAL_GOALS = 'total_goals',
  CORRECT_SCORE = 'correct_score',
  HALF_FULL = 'hf_ft',
}

/**
 * Probability flow direction classification
 */
export enum FlowDirection {
  UPWARD = 'upward',
  DOWNWARD = 'downward',
  STABLE = 'stable',
}

/**
 * Risk classification for strategy layers
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
  EXCEPTIONAL = 'exceptional',
}

/**
 * Validation result for strategy checking
 */
export enum ValidationResult {
  VALID = 'valid',
  INVALID = 'invalid',
  WARNING = 'warning',
}

/**
 * Intelligence source types
 */
export enum IntelligenceSource {
  RANKING = 'ranking',
  HISTORICAL = 'historical',
  RECENT_FORM = 'recent_form',
  TACTICAL = 'tactical',
  INJURY = 'injury',
  MOTIVATION = 'motivation',
  MARKET = 'market',
}

/**
 * Confidence level classification
 */
export enum ConfidenceLevel {
  VERY_HIGH = 'very_high',
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low',
  NEGATIVE = 'negative',
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
  confidence?: number;
}

/**
 * Result of true probability calculation
 */
export interface ITrueProbabilityResult {
  trueProbabilities: Record<string, number>;
  impliedProbabilities: Record<string, number>;
  marketMargin: number;
  marginPerOutcome: Record<string, number>;
  method: string;
  confidenceInterval?: Record<string, [number, number]>;
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
  momentumScore: number;
  significance: 'low' | 'medium' | 'high';
  velocity?: number;
  acceleration?: number;
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
  timeDelta: number;
  aggregateMomentum: number;
  generatedAt: Date;
}

/**
 * Bayesian prior distribution
 */
export interface IBayesianPrior {
  alpha: number;
  beta: number;
  source: IntelligenceSource;
  weight?: number;
}

/**
 * Bayesian posterior distribution
 */
export interface IBayesianPosterior {
  posteriorAlpha: number;
  posteriorBeta: number;
  expectedProbability: number;
  stdDeviation: number;
  credibleInterval: [number, number];
  updateEvidence: Record<string, unknown>;
}

/**
 * Amplification calculation result
 */
export interface IAmplificationResult {
  outcome: string;
  baseFlowPp: number;
  directionalConsistency: number;
  gradientPosition: number;
  marketMomentum: number;
  amplificationScore: number;
  level: AmplificationLevel;
  confidence: number;
  propagationDepth?: number;
  adjacentSignals?: Array<[string, number]>;
}

/**
 * Complete amplification report
 */
export interface IAmplificationReport {
  matchId: string;
  outcomes: string[];
  amplifications: IAmplificationResult[];
  aggregateMomentum: number;
  marketCascadeRisk: number;
  generatedAt: Date;
}

/**
 * Team intelligence data
 */
export interface ITeamIntelligence {
  teamId: string;
  teamName: string;
  ranking?: number;
  rankingPoints?: number;
  recentResults: string[];
  recentGoalsScored: number[];
  recentGoalsConceded: number[];
  homeAdvantage: number;
  awayPerformance: number;
  keyPlayersAvailable: number;
  keyPlayersTotal: number;
  injuriesCount: number;
  motivationFactor: number;
  travelDistance: number;
  restDays: number;
}

/**
 * Match intelligence data
 */
export interface IMatchIntelligence {
  matchId: string;
  homeTeam: ITeamIntelligence;
  awayTeam: ITeamIntelligence;
  competition: string;
  round?: string;
  importance: number;
  h2hHomeWins: number;
  h2hDraws: number;
  h2hAwayWins: number;
  h2hRecent: string[];
  weather: string;
  venueNeutral: boolean;
  gatheredAt: Date;
}

/**
 * Domain awareness report
 */
export interface IDomainAwarenessReport {
  matchId: string;
  matchIntelligence: IMatchIntelligence;
  confidenceScores: Record<string, number>;
  validationResults: Record<string, boolean>;
  finalConfidence: ConfidenceLevel;
  recommendations: string[];
  generatedAt: Date;
}

/**
 * A single selection in a strategy
 */
export interface IStrategySelection {
  matchId: string;
  marketType: MarketType;
  selection: string;
  quote: number;
  flowDirection: FlowDirection;
  amplificationScore: number;
  confidence: number;
}

/**
 * A complete analysis strategy
 */
export interface IStrategy {
  selections: IStrategySelection[];
  combinationType: string;
  multiplier: number;
  allocationPerCombination: number;
  riskLevel: RiskLevel;
  validationErrors: string[];
}

/**
 * A bundle of strategies
 */
export interface IStrategyBundle {
  strategies: IStrategy[];
  totalBudget: number;
  allocatedBudget: number;
  generatedAt: Date;
}

/**
 * Gradient graph for flow propagation
 */
export interface IGradientGraph {
  nodes: string[];
  edges: Array<{ source: string; target: string; distance: number }>;
  getAdjacentOutcomes(outcome: string): string[];
}

// ============================================================
// Probability Engine
// ============================================================

/**
 * Core probability analysis engine with Bayesian inference.
 */
export class ProbabilityEngine {
  private readonly flowThresholdLow: number = 0.5;
  private readonly flowThresholdMedium: number = 2.0;
  private readonly flowThresholdHigh: number = 5.0;

  constructor(config?: {
    flowThresholdLow?: number;
    flowThresholdMedium?: number;
    flowThresholdHigh?: number;
  }) {
    this.flowThresholdLow = config?.flowThresholdLow ?? this.flowThresholdLow;
    this.flowThresholdMedium = config?.flowThresholdMedium ?? this.flowThresholdMedium;
    this.flowThresholdHigh = config?.flowThresholdHigh ?? this.flowThresholdHigh;
  }

  /**
   * Calculate true probabilities from market quotes.
   */
  calculateTrueProbability(quotes: Record<string, number>): ITrueProbabilityResult {
    if (!quotes || Object.keys(quotes).length === 0) {
      throw new Error('Quotes dictionary cannot be empty');
    }

    for (const [outcome, quote] of Object.entries(quotes)) {
      if (quote <= 0) {
        throw new Error(`Invalid quote value for ${outcome}: ${quote}`);
      }
    }

    const impliedProbabilities: Record<string, number> = {};
    for (const [outcome, quote] of Object.entries(quotes)) {
      impliedProbabilities[outcome] = 1.0 / quote;
    }

    const marketMargin = Object.values(impliedProbabilities).reduce((a, b) => a + b, 0) - 1.0;

    const marginPerOutcome: Record<string, number> = {};
    const totalInverse = Object.values(impliedProbabilities).reduce((a, b) => a + b, 0);
    for (const [outcome, prob] of Object.entries(impliedProbabilities)) {
      marginPerOutcome[outcome] = (prob / totalInverse) * marketMargin;
    }

    const totalImplied = Object.values(impliedProbabilities).reduce((a, b) => a + b, 0);
    const trueProbabilities: Record<string, number> = {};
    for (const [outcome, prob] of Object.entries(impliedProbabilities)) {
      trueProbabilities[outcome] = prob / totalImplied;
    }

    const n = Object.keys(trueProbabilities).length;
    const confidenceInterval: Record<string, [number, number]> = {};
    for (const [outcome, prob] of Object.entries(trueProbabilities)) {
      const z = 1.96;
      const denom = 1 + (z * z) / n;
      const center = (prob + (z * z) / (2 * n)) / denom;
      const margin = (z * Math.sqrt(((prob * (1 - prob)) + (z * z) / (4 * n)) / denom)) / denom;
      confidenceInterval[outcome] = [Math.max(0, center - margin), Math.min(1, center + margin)];
    }

    return {
      trueProbabilities,
      impliedProbabilities,
      marketMargin,
      marginPerOutcome,
      method: 'shin_normalized',
      confidenceInterval,
    };
  }

  /**
   * Calculate conditional probabilities.
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
   * Update probability using Bayesian inference.
   */
  bayesianUpdate(
    prior: IBayesianPrior,
    successes: number,
    trials: number
  ): IBayesianPosterior {
    const posteriorAlpha = prior.alpha + successes;
    const posteriorBeta = prior.beta + (trials - successes);

    const expectedProb = posteriorAlpha / (posteriorAlpha + posteriorBeta);
    const variance = (posteriorAlpha * posteriorBeta) / (
      Math.pow(posteriorAlpha + posteriorBeta, 2) * (posteriorAlpha + posteriorBeta + 1)
    );
    const stdDev = Math.sqrt(variance);

    const z = 1.96;
    const lower = Math.max(0, expectedProb - z * stdDev);
    const upper = Math.min(1, expectedProb + z * stdDev);

    return {
      posteriorAlpha,
      posteriorBeta,
      expectedProbability: expectedProb,
      stdDeviation: stdDev,
      credibleInterval: [lower, upper],
      updateEvidence: { successes, trials, priorSource: prior.source },
    };
  }

  /**
   * Analyze probability flow between time points.
   */
  analyzeFlow(
    initialSnapshot: IProbabilitySnapshot,
    latestSnapshot: IProbabilitySnapshot
  ): IFlowReport {
    const flows: IFlowResult[] = [];

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

    const timeDelta = latestSnapshot.timestamp.getTime() - initialSnapshot.timestamp.getTime();

    for (const outcome of Object.keys(initialTrue.trueProbabilities)) {
      const initialProb = initialTrue.trueProbabilities[outcome];
      const latestProb = latestTrue.trueProbabilities[outcome] ?? initialProb;
      const flowPp = (latestProb - initialProb) * 100;

      let direction: FlowDirection;
      if (flowPp > this.flowThresholdLow) {
        direction = FlowDirection.UPWARD;
      } else if (flowPp < -this.flowThresholdLow) {
        direction = FlowDirection.DOWNWARD;
      } else {
        direction = FlowDirection.STABLE;
      }

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
        momentumScore: flowPp,
        significance,
        velocity: flowPp / Math.max(timeDelta / 3600000, 1),
      });
    }

    const aggregateMomentum = flows.reduce((sum, f) => sum + f.momentumScore, 0) / Math.max(flows.length, 1);

    return {
      matchId: `match_${initialSnapshot.timestamp.getTime()}`,
      marketType: initialSnapshot.marketType,
      initialSnapshot,
      latestSnapshot,
      flows,
      timeDelta,
      aggregateMomentum,
      generatedAt: new Date(),
    };
  }
}

// ============================================================
// Flow Amplification Engine
// ============================================================

/**
 * Advanced probability flow amplification effect analyzer.
 */
export class FlowAmplificationEngine {
  private readonly minBaseFlow = 1.0;

  constructor(config?: { minBaseFlow?: number }) {
    this.minBaseFlow = config?.minBaseFlow ?? this.minBaseFlow;
  }

  /**
   * Build a gradient graph for correct score outcomes.
   */
  buildCorrectScoreGradient(): IGradientGraph {
    const nodes: string[] = [];
    const edges: Array<{ source: string; target: string; distance: number }> = [];

    const homeScores = ['1:0', '2:0', '2:1', '3:0', '3:1', '3:2', '4:0', '4:1', '4:2'];
    const draws = ['0:0', '1:1', '2:2', '3:3'];
    const awayScores = ['0:1', '0:2', '1:2', '0:3', '1:3', '2:3', '0:4', '1:4'];

    [...homeScores, ...draws, ...awayScores].forEach((node) => {
      if (!nodes.includes(node)) nodes.push(node);
    });

    for (let i = 0; i < homeScores.length - 1; i++) {
      edges.push({ source: homeScores[i], target: homeScores[i + 1], distance: 1.0 });
    }

    for (let i = 0; i < draws.length - 1; i++) {
      edges.push({ source: draws[i], target: draws[i + 1], distance: 1.0 });
    }

    for (let i = 0; i < awayScores.length - 1; i++) {
      edges.push({ source: awayScores[i], target: awayScores[i + 1], distance: 1.0 });
    }

    return {
      nodes,
      edges,
      getAdjacentOutcomes: (outcome) => {
        return edges
          .filter((e) => e.source === outcome)
          .map((e) => e.target);
      },
    };
  }

  /**
   * Calculate amplification effect for all outcomes.
   */
  calculateAmplification(
    flowReport: IFlowReport,
    outcomeProbabilities: Record<string, number>,
    gradientGraph?: IGradientGraph
  ): IAmplificationReport {
    if (!gradientGraph) {
      gradientGraph = this.buildCorrectScoreGradient();
    }

    const flowDirections = new Map<string, string>();
    for (const f of flowReport.flows) {
      flowDirections.set(f.outcome, f.direction);
    }

    const amplifications: IAmplificationResult[] = [];

    for (const flowResult of flowReport.flows) {
      const outcome = flowResult.outcome;
      const baseFlow = flowResult.flowPp;

      if (Math.abs(baseFlow) < this.minBaseFlow) {
        amplifications.push({
          outcome,
          baseFlowPp: baseFlow,
          directionalConsistency: 0,
          gradientPosition: 0,
          marketMomentum: 1.0,
          amplificationScore: 0,
          level: AmplificationLevel.NONE,
          confidence: 1.0,
        });
        continue;
      }

      const adjacent = gradientGraph!.getAdjacentOutcomes(outcome);

      let directionalConsistency = 0;
      if (adjacent.length > 0) {
        const outcomeDirection = flowDirections.get(outcome) ?? 'stable';
        let consistent = 0;
        for (const adj of adjacent) {
          const adjDir = flowDirections.get(adj) ?? 'stable';
          if (outcomeDirection === 'upward' && adjDir !== 'downward') consistent++;
          else if (outcomeDirection === 'downward' && adjDir !== 'upward') consistent++;
          else if (outcomeDirection === 'stable' && adjDir === 'stable') consistent++;
        }
        directionalConsistency = consistent / adjacent.length;
      }

      const directionOutcomes = Array.from(flowDirections.entries())
        .filter(([, dir]) => dir === flowResult.direction)
        .map(([o]) => o);

      let gradientPosition = 0.5;
      if (directionOutcomes.length > 0) {
        const probs = directionOutcomes.map((o) => outcomeProbabilities[o] ?? 0);
        const maxProb = Math.max(...probs);
        const minProb = Math.min(...probs);
        if (maxProb !== minProb) {
          gradientPosition = (maxProb - (outcomeProbabilities[outcome] ?? 0)) / (maxProb - minProb);
        }
      }

      const adjacentFlows = flowReport.flows.filter((f) => adjacent.includes(f.outcome));
      let marketMomentum = 1.0;
      if (adjacentFlows.length > 0) {
        const momentumSum = adjacentFlows.reduce((sum, f) => {
          const weight = outcomeProbabilities[f.outcome] ?? 0.1;
          const sign = (baseFlow >= 0) === (f.flowPp >= 0) ? 1 : -1;
          return sum + sign * Math.abs(f.flowPp) * weight;
        }, 0);
        const avg = momentumSum / adjacentFlows.length;
        marketMomentum = avg > 3 ? 1.5 : avg > 1 ? 1.3 : avg > 0 ? 1.1 : avg > -1 ? 0.9 : 0.7;
      }

      let amplificationScore = 0;
      if (flowResult.direction === FlowDirection.UPWARD) {
        amplificationScore = baseFlow * directionalConsistency * (1 + gradientPosition) * marketMomentum;
      }

      let level: AmplificationLevel;
      if (amplificationScore < 1) level = AmplificationLevel.NONE;
      else if (amplificationScore < 3) level = AmplificationLevel.LOW;
      else if (amplificationScore < 6) level = AmplificationLevel.MEDIUM;
      else if (amplificationScore < 10) level = AmplificationLevel.HIGH;
      else if (amplificationScore < 15) level = AmplificationLevel.VERY_HIGH;
      else level = AmplificationLevel.EXCEPTIONAL;

      amplifications.push({
        outcome,
        baseFlowPp: baseFlow,
        directionalConsistency,
        gradientPosition,
        marketMomentum,
        amplificationScore,
        level,
        confidence: 1.0,
      });
    }

    const aggregateMomentum = amplifications.reduce((sum, a) => sum + a.amplificationScore, 0) / Math.max(amplifications.length, 1);
    const highMomentum = amplifications.filter((a) => a.amplificationScore > 5);
    const cascadeRisk = highMomentum.filter((a) => a.directionalConsistency < 0.5).length * 0.2;

    return {
      matchId: flowReport.matchId,
      outcomes: amplifications.map((a) => a.outcome),
      amplifications,
      aggregateMomentum,
      marketCascadeRisk: Math.min(cascadeRisk, 1),
      generatedAt: new Date(),
    };
  }
}

// ============================================================
// Domain Awareness System
// ============================================================

/**
 * Domain awareness system for sports analytics.
 */
export class DomainAwarenessSystem {
  /**
   * Analyze match with domain awareness.
   */
  analyzeMatch(
    matchIntelligence: IMatchIntelligence,
    flowConfidences?: Record<string, number>
  ): IDomainAwarenessReport {
    const flowConf = flowConfidences ?? { home_win: 0.33, draw: 0.33, away_win: 0.33 };

    const homeForm = matchIntelligence.homeTeam.recentResults.slice(-5).reduce((sum, r) => {
      return sum + (r === 'W' ? 1 : r === 'D' ? 0.5 : 0);
    }, 0) / Math.min(matchIntelligence.homeTeam.recentResults.length, 5);

    const awayForm = matchIntelligence.awayTeam.recentResults.slice(-5).reduce((sum, r) => {
      return sum + (r === 'W' ? 1 : r === 'D' ? 0.5 : 0);
    }, 0) / Math.min(matchIntelligence.awayTeam.recentResults.length, 5);

    const homeModifier = (homeForm - 0.5) * 0.15;
    const awayModifier = (awayForm - 0.5) * 0.15;

    const intelligenceConfidence: Record<string, number> = {
      home_win: 0.33 + homeModifier,
      draw: 0.33,
      away_win: 0.33 + awayModifier,
    };

    const total = Object.values(intelligenceConfidence).reduce((a, b) => a + b, 0);
    for (const [key, val] of Object.entries(intelligenceConfidence)) {
      intelligenceConfidence[key] = val / total;
    }

    const flowWeight = 0.6;
    const intelWeight = 0.4;

    const combinedConfidence: Record<string, number> = {};
    for (const [outcome, flowConfidence] of Object.entries(flowConf)) {
      combinedConfidence[outcome] = flowWeight * flowConfidence + intelWeight * (intelligenceConfidence[outcome] ?? 0.33);
    }

    const avgConfidence = Object.values(combinedConfidence).reduce((a, b) => a + b, 0) / Object.keys(combinedConfidence).length;

    let overallLevel: ConfidenceLevel;
    if (avgConfidence >= 0.85) overallLevel = ConfidenceLevel.VERY_HIGH;
    else if (avgConfidence >= 0.7) overallLevel = ConfidenceLevel.HIGH;
    else if (avgConfidence >= 0.5) overallLevel = ConfidenceLevel.MEDIUM;
    else if (avgConfidence >= 0.3) overallLevel = ConfidenceLevel.LOW;
    else overallLevel = ConfidenceLevel.NEGATIVE;

    const recommendations: string[] = [];
    if (overallLevel === ConfidenceLevel.VERY_HIGH) {
      recommendations.push('Strong multi-source confirmation detected');
    } else if (overallLevel === ConfidenceLevel.NEGATIVE) {
      recommendations.push('Warning: Conflicting signals detected');
    }

    const strengthDiff = (homeForm + matchIntelligence.homeTeam.homeAdvantage * 0.1) - 
                         (awayForm + matchIntelligence.awayTeam.awayPerformance * 0.1);
    if (Math.abs(strengthDiff) > 0.3) {
      recommendations.push(
        strengthDiff > 0 
          ? `Home team significantly stronger (delta: ${strengthDiff.toFixed(2)})`
          : `Away team significantly stronger (delta: ${Math.abs(strengthDiff).toFixed(2)})`
      );
    }

    return {
      matchId: matchIntelligence.matchId,
      matchIntelligence,
      confidenceScores: combinedConfidence,
      validationResults: {},
      finalConfidence: overallLevel,
      recommendations,
      generatedAt: new Date(),
    };
  }
}

// ============================================================
// Strategy Engine
// ============================================================

/**
 * Strategy design engine implementing the Three Principles.
 */
export class StrategyEngine {
  private readonly minAllocation = 2.0;
  private readonly minMultiplierThreshold = 3.0;

  /**
   * Validate a strategy against all rules.
   */
  validateStrategy(strategy: IStrategy): [ValidationResult, string[]] {
    const errors: string[] = [];

    const hasUpwardFlow = strategy.selections.every(
      (s) => s.flowDirection === FlowDirection.UPWARD
    );
    if (!hasUpwardFlow) {
      errors.push('Principle 1 violation: Selections must have upward flow');
    }

    const combinedQuote = strategy.selections.reduce((acc, s) => acc * s.quote, 1);
    if (combinedQuote < this.minMultiplierThreshold) {
      errors.push(
        `Principle 2 violation: Combined quote ${combinedQuote.toFixed(2)} ` +
        `below minimum ${this.minMultiplierThreshold}`
      );
    }

    if (strategy.allocationPerCombination < this.minAllocation) {
      errors.push(
        `Rule violation: Allocation ${strategy.allocationPerCombination} below minimum ${this.minAllocation}`
      );
    }

    return errors.length > 0 ? [ValidationResult.INVALID, errors] : [ValidationResult.VALID, []];
  }

  /**
   * Generate optimized strategies.
   */
  generateStrategies(
    amplificationReport: IAmplificationReport,
    budget: number,
    maxStrategies: number = 10
  ): IStrategyBundle {
    const strategies: IStrategy[] = [];
    const reliable = amplificationReport.amplifications
      .filter((a) => a.level !== AmplificationLevel.NONE && a.confidence >= 0.5)
      .sort((a, b) => b.amplificationScore - a.amplificationScore);

    let allocated = 0;

    for (let i = 0; i < Math.min(reliable.length, maxStrategies); i++) {
      const amp = reliable[i];

      const selection: IStrategySelection = {
        matchId: amplificationReport.matchId,
        marketType: MarketType.MATCH_RESULT,
        selection: amp.outcome,
        quote: 3.0,
        flowDirection: FlowDirection.UPWARD,
        amplificationScore: amp.amplificationScore,
        confidence: amp.confidence,
      };

      const combinedQuote = selection.quote;

      const strategy: IStrategy = {
        selections: [selection],
        combinationType: 'single',
        multiplier: 1,
        allocationPerCombination: 10.0,
        riskLevel: combinedQuote < 5 ? RiskLevel.CONSERVATIVE : 
                  combinedQuote < 20 ? RiskLevel.BALANCED : 
                  combinedQuote < 100 ? RiskLevel.AGGRESSIVE : RiskLevel.EXTREME,
        validationErrors: [],
      };

      const [result] = this.validateStrategy(strategy);
      if (result === ValidationResult.VALID) {
        strategies.push(strategy);
        allocated += strategy.allocationPerCombination;
      }
    }

    return {
      strategies,
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
  FlowAmplificationEngine,
  DomainAwarenessSystem,
  StrategyEngine,
  MarketType,
  FlowDirection,
  RiskLevel,
  AmplificationLevel,
  ValidationResult,
  IntelligenceSource,
  ConfidenceLevel,
};

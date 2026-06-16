# EDP — Expectation Domain Perception Method

> **A Multi-Source Intelligence Fusion and Probabilistic Situation Awareness Framework**

---

## 1. Overview

**Expectation Domain Perception Method (EDP)** is an academic computational framework for **probabilistic analysis and statistical research**. It integrates four cooperative analytical layers which, starting from raw market quotes, propagate information through Bayesian inference and time-series momentum analysis, ultimately producing multi-source-fused situation assessments and resource allocation plans.

The design of this framework rests on the following foundational principles:

1. **Axiomatic probability foundation** — All computations strictly adhere to the Kolmogorov axioms of probability;
2. **Bayesian evidence accumulation** — Sequential processing of information from independent sources via conjugate-prior analytical posterior updates;
3. **Time-series momentum analysis** — Detection of probability-mass flow through the outcome space, following the momentum paradigm of Moskowitz et al. (2012);
4. **Multi-source intelligence fusion** — Combination of weighted linear opinion pools, log-odds opinion pools, and DeGroot consensus dynamics;
5. **Information cascade detection** — Identification of potential herding effects and evidential redundancy;
6. **Optimal capital allocation** — Constrained resource allocation combining the Kelly Criterion with Markowitz portfolio theory.

⚠️ **This framework is for academic research and educational purposes only. Historical probability patterns do not guarantee future outcomes. This framework does not constitute investment advice or decision-making recommendation of any kind.**

---

## 2. Five-Layer Stacked Analytical Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  Layer 5 · Resource Allocation                                │
│  Kelly Criterion · Markowitz Portfolio Theory · Three Principles │
├──────────────────────────────────────────────────────────────┤
│  Layer 4 · Domain Awareness                                   │
│  Multi-Source Intelligence Fusion · Evidence Combination      │
│  Consensus Dynamics · Anomaly Detection · Cascade Detection   │
├──────────────────────────────────────────────────────────────┤
│  Layer 3 · Flow Amplification                                 │
│  Base Flow → Directional Consistency → Gradient Position      │
│  Market Momentum → Amplification Score                        │
├──────────────────────────────────────────────────────────────┤
│  Layer 2 · Bayesian Inference                                 │
│  Beta-Binomial Conjugacy · Shin Marginal Decomposition        │
│  Glicko-2 Rating System · Credible Intervals                  │
├──────────────────────────────────────────────────────────────┤
│  Layer 1 · Probability Analysis                               │
│  Market Quotes → Shin Normalization → True Probabilities      │
│  Conditional Probabilities → Flow Analysis                    │
├──────────────────────────────────────────────────────────────┤
│  Layer 0 · Data Acquisition                                   │
│  Snapshot Collection · Quality Validation · Standard Interface│
└──────────────────────────────────────────────────────────────┘
```

---

## 3. Mathematical Foundations

### 3.1 Shin Normalization — Extraction of True Probabilities

Market quotes embed a profit margin ("overround") and therefore cannot be directly interpreted as probabilities. The model proposed by Shin (1992) posits that the margin is proportional to the presence of "insider traders," allowing one to invert the relationship to recover "true probabilities."

**Formal problem statement**: Given quotes *q₁, q₂, …, qN* for *N* outcomes, where *qᵢ > 1* in decimal odds.

**Implied probabilities**: πᵢ = 1/qᵢ. The market overround is:

> Σᵢ₌₁ᴺ πᵢ − 1 > 0

**Shin iterative scheme** for the recovery of true probabilities *p*:

> pᵢᵏ⁺¹ = (πᵢ − zᵏ √pᵢᵏ) / (1 − zᵏ Σⱼ √pⱼᵏ)

where *z* is the estimated insider-trade proportion; the iteration terminates when |pᵢᵏ⁺¹ − pᵢᵏ| < ε.

**Reference**: Shin, H.S. (1992). *Prices of State-Contingent Claims with Insider Traders*. Economic Journal, 102(411), 426–435.

### 3.2 Beta-Binomial Conjugate Bayesian Inference

For Bernoulli trials, the Beta distribution provides a conjugate prior family:

- **Prior**: Beta(α₀, β₀)
- **Observation**: *k* successes in *n* trials
- **Posterior**: Beta(α₀ + k, β₀ + n − k)

**Posterior mean**:

> E[p | evidence] = (α₀ + k) / (α₀ + β₀ + n)

**95% Credible interval** via the normal approximation:

> CI₉₅ = p̂ ± 1.96 × √(p̂(1 − p̂)/(n_eff + 1))

**Reference**: Gelman, A., Carlin, J.B., Stern, H.S., & Rubin, D.B. (2013). *Bayesian Data Analysis*, 3rd ed. Chapman & Hall/CRC.

### 3.3 Glicko-2 Rating System

An advancement over the Elo system, introducing rating deviation (RD) and volatility (σ) for more robust dynamic strength modeling.

**Core update equations** (in Glicko-2 scale: μ, φ, σ):

> E(μ, μⱼ, φⱼ) = 1 / (1 + exp(−g(φⱼ)(μ − μⱼ)))

> g(φ) = 1 / √(1 + 3φ²/π²)

> ν = [ Σⱼ g(φⱼ)² E(1 − E) ]⁻¹

> Δ = ν · Σⱼ g(φⱼ) (sⱼ − E)

where ν is the estimated variance and Δ the improvement deviation.

**Reference**: Glickman, M.E. (1999). *Parameter Estimation in Large Dynamic Paired Comparison Systems*. Applied Statistics, 48(3), 377–394.

### 3.4 Probability Flow Analysis

**Definition** (within a time interval Δt):

> Flowᵢ = pᵢ(t + Δt) − pᵢ(t)

**Time-series momentum score** (Moskowitz et al., 2012):

> momentum_score = Σ_t w_t · flow_t,  where Σ_t w_t = 1

**Velocity and acceleration**:

> vᵢ = d(Flowᵢ) / dt,   aᵢ = d²(Flowᵢ) / dt²

**Significance thresholds**: |flow| < 0.5% stable; 0.5%–2% low; 2%–5% medium; ≥5% high.

### 3.5 Flow Amplification Score

The amplification score for outcome *i* combines four factors:

> AmpScoreᵢ = BaseFlowᵢ × DirConsistᵢ × (1 + GradientPosᵢ) × MarketMomentum

- **Directional consistency** *DirConsistᵢ*: fraction of adjacent outcomes whose flow is aligned with the target outcome
- **Gradient position** *GradientPosᵢ*: normalized probability level — lower-probability outcomes carry higher amplification potential
- **Market momentum** *MarketMomentum*: mean momentum across all outcomes

### 3.6 Multi-Source Intelligence Fusion

A **hybrid fusion strategy** is adopted — a weighted combination of linear and log-odds opinion pools:

**Linear opinion pool** (Cooke, 1991):

> p_linear = Σᵢ wᵢ · pᵢ,  where Σᵢ wᵢ = 1

**Log-odds opinion pool** (Genest & Zidek, 1986):

> logit(p_logodds) = Σᵢ wᵢ · logit(pᵢ)

**Hybrid estimate**:

> p_fused = α · p_linear + (1 − α) · p_logodds,  α ∈ [0, 1]

**Source weights** are three-dimensional:

> wᵢ = reliabilityᵢ × confidenceᵢ × temporal_decayᵢ

> temporal_decayᵢ = 2^(−Δtᵢ / t½)

**Consensus score** (based on dispersion of source estimates):

> Consensus = 1 − min(σ_observed / σ_max, 1.0)

where σ_max = 0.5 is the theoretical maximum standard deviation for a Bernoulli(p=0.5) distribution.

### 3.7 Kelly-Optimal Capital Allocation

The Kelly Criterion maximizes the expected log-wealth growth rate:

> f* = (p · b − q) / b = (p(b + 1) − 1) / b

where *p* is the win probability, *b* the net decimal odds (quote − 1), and *q = 1 − p*.

**Fractional Kelly** (framework default: quarter-Kelly, 1/4):

> f = κ · f*,  κ ∈ (0, 1]

This controls volatility at the expense of a reduced expected growth rate.

**Three Principles of Allocation**:
1. **Signal Alignment** — Only allocate to outcomes with positive probability-flow signals
2. **Asymmetric Potential** — Require positive expectation (odds × probability > 1)
3. **Risk Diversification** — Cap concentration ≤ 20% and maintain diversification ratio

---

## 4. Core Engines

### 4.1 ProbabilityEngine

| Module | Theoretical Basis | Output |
|--------|-------------------|--------|
| True probability calculation | Shin normalization / iterative method | p_true, margin, CI |
| Conditional probability | Bayesian conditional definition | p(A \| B) |
| Bayesian update | Beta-Binomial conjugate model | posterior α, β, CI |
| Prior fusion | Log-odds / linear pool | combined posterior |
| Glicko-2 ratings | Glickman (1999) | μ, RD, σ |
| Flow analysis | Time-series momentum | flow_velocity, acceleration |

### 4.2 FlowAnalyzer

| Module | Theoretical Basis | Output |
|--------|-------------------|--------|
| Base flow | Differenced time series | Δp, v, a |
| Directional consistency | Adjacency-structure scoring | 0–1 consistency coefficient |
| Gradient position | Inverse mapping on probability simplex | 0–1 amplification potential |
| Market momentum | Weighted aggregate momentum | aggregate_momentum |
| Cascade risk | Information cascade theory | Risk level tagging |

### 4.3 DomainAwarenessEngine

| Module | Theoretical Basis | Output |
|--------|-------------------|--------|
| Evidence preprocessing | Source reliability rating (STANAG 2511 adaptation) | w_i, normalized weights |
| Linear pool fusion | Cooke (1991) opinion pool | p_linear |
| Log-odds pool fusion | Genest & Zidek (1986) | p_logodds |
| Bayesian accumulation | Pearl (1988) sequential updating | posterior log-odds |
| Consensus analysis | Variance-dispersion transform | consensus_score |
| Anomaly detection | Z-score thresholding | anomaly list |
| Cascade detection | Information cascade theory (Bikhchandani 1992) | potential_cascade flag |
| Situation assessment | Stability classifier | aggregate_probability, confidence, status |

### 4.4 AllocationEngine

| Module | Theoretical Basis | Output |
|--------|-------------------|--------|
| Validity check | Three allocation principles | valid / warning / invalid |
| Kelly allocation | Kelly (1956) information-rate criterion | fraction, amount |
| Risk stratification | Probability-odds mapping | conservative / balanced / aggressive / extreme |
| Markowitz rebalancing | Concentration cap + diversification ratio | optimized allocation |
| Portfolio statistics | Expected value / risk contribution | portfolio_EV, diversification_ratio |

---

## 5. Implementation Specifications

### 5.1 Technical Stack

| Aspect | Technology |
|--------|------------|
| Programming Languages | Python 3.10+, TypeScript 5.0+ |
| Type Safety | Full type annotations (dataclass, Enum) |
| Numerical Precision | IEEE 754 double-precision |
| Convergence Criterion | ε = 1e-10 (Shin iterations) |
| Iteration Cap | 100 iterations |

### 5.2 Code Quality and Validation

- **Linting**: Static syntax and style verification
- **Formatting**: Standard style unification
- **Type checking**: MyPy static type verification
- **Test framework**: pytest (Python) / Jest (TypeScript)

---

## 6. Key References

| Theory / Method | Citation |
|-----------------|----------|
| Shin Normalization | Shin, H.S. (1992). *Prices of State-Contingent Claims with Insider Traders*. Economic Journal, 102(411), 426–435. |
| Bayesian Inference | Gelman, A., Carlin, J.B., Stern, H.S., & Rubin, D.B. (2013). *Bayesian Data Analysis*, 3rd ed. Chapman & Hall/CRC. |
| Time-Series Momentum | Moskowitz, T.J., Ooi, Y.H., & Pedersen, L.H. (2012). *Time Series Momentum*. Journal of Financial Economics, 104(2), 228–250. |
| Glicko-2 Rating | Glickman, M.E. (1999). *Parameter Estimation in Large Dynamic Paired Comparison Systems*. Applied Statistics, 48(3), 377–394. |
| Elo Rating System | Elo, A.E. (1978). *The Rating of Chessplayers, Past and Present*. Arco. |
| Information Cascades | Banerjee, A.V. (1992). *A Simple Model of Herd Behavior*. Quarterly Journal of Economics, 107(3), 797–817. |
| | Bikhchandani, S., Hirshleifer, D., & Welch, I. (1992). *A Theory of Fads, Fashion, Custom, and Cultural Change as Information Cascades*. JPE, 100(5), 992–1026. |
| Probability Distribution Fusion | Genest, C., & Zidek, J.V. (1986). *Combining Probability Distributions: A Critique and an Annotated Bibliography*. Statistical Science, 1(1), 114–135. |
| Consensus Dynamics | DeGroot, M.H. (1974). *Reaching a Consensus*. JASA, 69(345), 118–121. |
| Expert Uncertainty | Cooke, R.M. (1991). *Experts in Uncertainty*. Oxford University Press. |
| Kelly Criterion | Kelly, J.L. (1956). *A New Interpretation of Information Rate*. Bell System Technical Journal, 35(4), 917–926. |
| | MacLean, L.C., Thorp, E.O., & Ziemba, W.T. (2010). *The Kelly Capital Growth Investment Criterion*. World Scientific. |
| Portfolio Theory | Markowitz, H.M. (1952). *Portfolio Selection*. Journal of Finance, 7(1), 77–91. |
| Universal Portfolios | Cover, T.M. (1991). *Universal Portfolios*. Mathematical Finance, 1(1), 1–29. |
| Prospect Theory | Kahneman, D., & Tversky, A. (1979). *Prospect Theory: An Analysis of Decision Under Risk*. Econometrica, 47(2), 263–291. |
| Bayesian Networks | Pearl, J. (1988). *Probabilistic Reasoning in Intelligent Systems*. Morgan Kaufmann. |
| Information Theory | Cover, T.M., & Thomas, J.A. (2006). *Elements of Information Theory*, 2nd ed. Wiley. |

---

## 7. Usage Examples

### 7.1 Python Interface

```python
from edp import (
    ProbabilityEngine,
    FlowAnalyzer,
    DomainAwarenessEngine,
    AllocationEngine,
)

# ── Initialize engines ─────────────────────────────────
prob_engine = ProbabilityEngine()
flow_engine = FlowAnalyzer()
domain_engine = DomainAwarenessEngine()
alloc_engine = AllocationEngine()

# ── 1. Compute true probabilities from market quotes ──
result = prob_engine.calculate_true_probability({
    "home": 1.50, "draw": 4.20, "away": 6.00
})

# Fields: true_probabilities, margin, confidence_interval, method

# ── 2. Probability flow analysis (time series) ─────────
flow_report = prob_engine.analyze_flow(
    initial_snapshot=snapshot_t0,
    latest_snapshot=snapshot_t1,
    historical_snapshots=history,
)

# Fields: flows (per-outcome flow / velocity / acceleration / significance),
#         aggregate_momentum, time_delta

# ── 3. Flow amplification scoring ─────────────────────
amp_report = flow_engine.calculate_amplification(
    flow_report,
    gradient_map={"home": ["draw"], "away": ["draw"]},
    outcome_probs=result.true_probabilities,
)

# ── 4. Domain awareness · multi-source fusion ──────────
from edp import EvidenceSource, SourceReliability, EvidenceType

sources = [
    EvidenceSource(
        source_id="model_01",
        source_type=EvidenceType.ANALYTICAL,
        reliability=SourceReliability.B,   # usually reliable
        timestamp=datetime.now(),
        content={"probability": 0.62},
        confidence=0.80,
    ),
    EvidenceSource(
        source_id="market_quote",
        source_type=EvidenceType.OBSERVATIONAL,
        reliability=SourceReliability.A,   # completely reliable
        timestamp=datetime.now(),
        content={"probability": result.true_probabilities["home"]},
        confidence=0.95,
    ),
    # ... additional intelligence sources
]

assessment = domain_engine.assess_situation(
    sources,
    prior_probability=0.5,
    fusion_method="hybrid",
)

# Fields: aggregate_probability, confidence, consensus_score,
#         stability_status, anomalies, variance

# ── 5. Capital allocation (Kelly + Markowitz) ─────────
from edp import AllocationLeg

candidates = [
    AllocationLeg(
        identifier="outcome_home",
        probability=assessment.aggregate_probability,
        odds=1.50,
        signal_score=flow_report.flows[0].momentum_score,
        confidence=assessment.confidence,
        flow_direction="upward",
    ),
    # ...
]

bundle = alloc_engine.generate_allocation(
    budget=1000.0,
    candidates=candidates,
)

bundle = alloc_engine.optimize_portfolio(
    bundle, target_diversification=0.6
)
```

### 7.2 TypeScript Interface

```typescript
import {
  ProbabilityEngine,
  FlowAnalyzer,
} from 'edp-framework';

const engine = new ProbabilityEngine();

const result = engine.calculateTrueProbability({
  home: 1.50, draw: 4.20, away: 6.00
});
```

---

## 8. Disclaimer

**This framework is for academic research and educational purposes only.**

- This framework does not constitute any investment advice or decision-making recommendation;
- Any decisions made using this framework are the sole responsibility of the user;
- The authors are not responsible for any losses incurred through the use of this framework;
- Please comply with laws and regulations in your jurisdiction.

---

## 9. License

MIT License — See the *LICENSE* file in the repository root for details.

---

*Providing academic research support through structured analysis, rigorous probability theory, and domain-wide cognition — for academic research purposes only.*

*© 2026 — For Academic Research and Educational Purposes Only.*

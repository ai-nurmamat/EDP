# 🎯 Expected Domain Perception

> **A Methodology for Asymmetric Expected Value Discovery Based on Probability Flow and Domain Awareness**
>
> **基于概率流向与全域感知的非对称期望值优势发现方法论**

![Version](https://img.shields.io/badge/Version-1.0-blue)
![Status](https://img.shields.io/badge/Status-Production--Ready-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0%2B-blue)

---

## ⚠️ Risk Disclaimer

> **This framework is for ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY.**
>
> - Sports analytics involves **real financial risk**. Historical probability patterns do **NOT guarantee** future results.
> - All sports analytics activities have **negative expected value (EV)** by design (bookmaker margin). No system can mathematically overcome this fact.
> - **NEVER invest money you cannot afford to lose.** Sports analytics should be treated as entertainment, not investment.
> - The author makes **NO WARRANTIES** regarding the accuracy, completeness, or profitability of any analysis produced by this framework.
> - Users bear full responsibility for their own decisions and must comply with **local laws and regulations**.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Probability Philosophy](#probability-philosophy-we-dont-research-most-likely-we-identify-value)
- [Design Philosophy](#design-philosophy-ooda-loop--loop-engineering--dag-execution)
- [Data Acquisition Layer](#data-acquisition-layer)
- [Probability Analysis Engine](#probability-analysis-engine)
- [Probability Flow Amplification Effect](#probability-flow-amplification-effect)
- [Domain Awareness System](#domain-awareness-system)
- [Value Assessment Engine](#value-assessment-engine)
- [Scheme Design Engine](#scheme-design-engine)
- [Rule Compliance Layer](#rule-compliance-layer)
- [Output Generation](#output-generation)
- [Academic Foundation](#academic-foundation)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [MCP Integration](#mcp-integration)
- [Skill Integration](#skill-integration)
- [Contributing](#contributing)
- [License](#license)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Output Generation Layer                   │
│  Scheme Summary → Narrative Generation → Quality Checklist  │
├─────────────────────────────────────────────────────────────┤
│                    Scheme Design Engine                      │
│  Risk Stratification → Parlay Construction → Budget Alloc   │
├─────────────────────────────────────────────────────────────┤
│                    Flow Amplification Engine                 │
│  Base Flow → Directional Consistency → Gradient Position    │
├─────────────────────────────────────────────────────────────┤
│                    Domain Awareness System                   │
│  Match Intelligence ← Probability Flow ← Market Consensus   │
├─────────────────────────────────────────────────────────────┤
│                    Probability Analysis Engine               │
│  True Probability → Conditional Prob → Flow Analysis        │
├─────────────────────────────────────────────────────────────┤
│                    Data Acquisition Layer                    │
│  Visual Extraction ← Web Scraping ← API Integration         │
└─────────────────────────────────────────────────────────────┘
```

The system employs a **Directed Acyclic Graph (DAG) pipeline architecture**, where each layer produces structured data for downstream consumption. Core design principles derive from three methodologies:

1. **OODA Loop** (Boyd, 1987) — Observe-Orient-Decide-Act, with iterative refinement embedded in each layer
2. **Loop Engineering** — Continuous signal quality calibration through feedback loops
3. **DAG Execution** — Stateful graph execution model similar to LangGraph, with standardized protocols between nodes

### Design Principles (Non-Negotiable)

| Principle | Description |
|-----------|-------------|
| **Data Agnostic** | Input sources abstracted behind unified interfaces; pipeline can connect to any probability data source |
| **Implementation Agnostic** | Probability extraction can use any vision recognition, OCR engine, or manual input |
| **Rule Aware** | All output schemes must pass rule validation before presentation |
| **Domain First** | Situational awareness guides but never overrides probability signals |

---

## Probability Philosophy: We Don't Research Most Likely, We Identify VALUE

### Core Philosophy

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  We do NOT research: On the most likely outcome (lowest odds)                │
│  We DO assess: Where Market_Odds > Fair_Odds (Positive Expected Value)     │
│                                                                               │
│  Key Insight: Even if 80% of opportunities fail, the 20% that succeed can │
│               cover ALL losses AND generate profit                           │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Contrast with Traditional Approach

| Traditional (❌) | Expected Domain Perception (✅) |
|-----------------|-------------------------------|
| Research lowest odds | Identify highest EV |
| High success rate | Low success rate, high returns |
| Many small wins | Few big wins cover many small failures |
| Negative mathematical expectation | Mathematical long-term edge |

### Mathematical Foundation

**Expected Value (EV) Formula**:

```
EV = P(success) × (Odds - 1) - P(fail) × 1
```

**Condition for Value**: When Market_Odds > Fair_Odds, EV > 0

**Example**:
- Market offers 8.0 odds for outcome
- Our assessment: True probability P = 15%
- Market implies: P = 12.5% (1/8.0)
- Market underestimates → **VALUE EXISTS!**

```
EV = 0.15 × 7 - 0.85 × 1 = 1.05 - 0.85 = +0.20 per unit allocated

Even with only 15% success rate, this opportunity is profitable in the long run!

### The "N Trials, 1 Success" Model

If we identify 20 opportunities at 5% of bankroll each, average odds 8.0, true probability 15%:

**Expected Outcomes**:
- Successes: 20 × 15% = 3 opportunities
- Failures: 20 × 85% = 17 opportunities

**If 3 succeed**:
- Profit from successes: 3 × 5% × 8.0 = 120% of bankroll
- Loss from 17 failures: 17 × 5% = 85% of bankroll
- **Net Profit: 120% - 85% = +35% of bankroll!**

**Power Law Distribution**: Few big wins (at high odds) cover many small losses.

### Role of Domain Awareness System

Domain Awareness evaluates **"real-world possibility of low-probability events"**:

- Identify teams/events underestimated by the market
- Assess tactics, squad, motivation factors
- Determine if odds deviate from real-world possibility
- **Key Question**: Not "which is most likely to win", but "which is underestimated"

### Value Classification

| Classification | Value Ratio (Market/Fair) | Description |
|---------------|---------------------------|-------------|
| **Exceptional** | ≥ 1.30 | Rare opportunity, market severely underestimates |
| **High** | ≥ 1.20 | Significant value, clear positive EV |
| **Moderate** | ≥ 1.10 | Positive but marginal EV |
| **Fair** | ≥ 1.00 | Market efficiently priced |
| **Poor** | < 1.00 | Negative EV, not recommended |

### Academic Support

| Theory | Literature | Application |
|--------|------------|-------------|
| Kelly Criterion | Kelly (1956) | Maximize log wealth growth |
| Value Assessment Theory | Market Efficiency Research | Identify market inefficiencies |
| Prospect Theory | Kahneman & Tversky (1979) | Risk-seeking in loss domain |
| Power Law Distribution | Extreme Event Statistics | Big wins cover small losses |

---

## Design Philosophy: OODA Loop × Loop Engineering × DAG Execution

### OODA Loop Mapping in Sports Analytics

The OODA Loop was developed by U.S. Air Force Colonel John Boyd (Boyd, 1987, "A Discourse on Winning and Losing"), originally for military decision-making. Its core is a **rapid perceive-orient-decide-act** closed loop.

```
┌──────────────────────────────────────────────────────────┐
│  Observe                                                  │
│  ├─ Probability snapshots (initial vs latest)            │
│  ├─ Match intelligence (rankings, form, injuries, tactics)│
│  └─ Market signals (volume distribution, expert consensus)│
│                                                          │
│  Orient                                                   │
│  ├─ True probability calculation (margin removal)        │
│  ├─ Probability flow calculation (initial→latest delta)  │
│  ├─ Amplification scoring (directional consistency ×     │
│  │                          gradient position)           │
│  └─ Cross-validation (probability vs intelligence vs     │
│                       market consensus)                  │
│                                                          │
│  Decide                                                   │
│  ├─ Three Principles validation (each leg must pass)      │
│  ├─ Scheme construction (stratification + parlay +      │
│  │                       budget allocation)             │
│  └─ Mixed parlay compliance check                       │
│                                                          │
│  Act                                                      │
│  ├─ Generate narrative                                   │
│  ├─ Quality checklist verification                       │
│  └─ Collect feedback → Enter next OODA cycle           │
└──────────────────────────────────────────────────────────┘
```

**Termination Conditions**:
- All available data processed → Output final scheme
- User budget fully allocated → Output final scheme
- Dead loop detection (same data iterated without new signals) → Force stop and report

---

## Data Acquisition Layer

### Visual Information Extraction

Platform screenshots contain structured tabular data (probability history, score matrices, handicap lines). The extraction pipeline follows a **three-stage strategy**:

1. **Type Classification** — Determine image content type (probability table, score matrix, handicap history, etc.)
2. **Structured Extraction** — Extract numerical data while preserving temporal context (initial vs latest)
3. **Validation** — Cross-check extracted data consistency (e.g., probability monotonicity, field completeness)

> **Framework Note**: The extraction backend is pluggable. Any multimodal recognition solution, OCR engine, or manual entry system can serve as an implementation.

### Unified Data Schema

All data sources produce data artifacts conforming to a unified schema:

| Field | Type | Description |
|-------|------|-------------|
| match_id | string | Unique match identifier |
| teams | object | { home, away } team names |
| timestamp | datetime | Data collection timestamp |
| markets.1X2 | time series | Win/Draw/Loss true probabilities (initial→latest) |
| markets.handicap | time series | Handicap line probabilities (e.g., -1, -2, +2) |
| markets.total_goals | time series | Total goals probabilities (0, 1, 2, ..., 7+) |
| markets.correct_score | time series | Correct score probabilities (all score combinations) |

---

## Probability Analysis Engine

### True Probability

Platform probabilities embed bookmaker margin (overround). To extract **true probability**, normalization is required:

```python
P_true(outcome_i) = (1 / odds_i) / Σ(1 / odds_j) × 100%
```

**Mathematical Basis**: If a market offers probability `o_i` for outcome `i`, the implied probability is `1/o_i`. Since `Σ(1/o_j) > 1` (i.e., margin), dividing by the sum yields a normalized probability distribution where all outcomes sum to 100%.

**Academic Support**: This normalization is equivalent to a simplified variant of the **Shin method** (Shin, 1992).

### Conditional Probability

For correct score markets, calculate **directional conditional probability**:

```python
P(score | direction) = P_true(score) / Σ P_true(scores_in_direction)
```

**Question Answered**: "Given the home team wins, what is the probability of each specific score?"

### Probability Flow

Probability flow is the core concept of this framework. It measures the **change** in market true probability distribution over time:

```python
Flow(outcome) = P_true_latest(outcome) - P_true_initial(outcome)
```

| Flow | Meaning |
|------|---------|
| **Positive (inflow)** | Market increasingly favors this outcome |
| **Negative (outflow)** | Market moving away from this outcome |
| **Zero (stable)** | No significant information change |

**Core Insight**: Positive flow indicates informed money (or information) is accumulating toward this outcome. Magnitude (in percentage points, pp) reflects confidence strength.

---

## Probability Flow Amplification Effect

> ⚠️ **This chapter describes the framework's most powerful analytical tool, and also the most risky. Amplification effect is a probability analysis amplifier—it can amplify correct signals, but also incorrect ones. Must be used in conjunction with the Domain Awareness System.**

### Definition of Amplification Effect

When probability flow shows money moving from outcome A to outcome B, it typically means adjacent outcomes on the same directional gradient **are also flowing in the same direction**. This is the **Amplification Effect**.

### Amplification Score Formula

```python
Amplification_Score(outcome) =
    Base_Flow(outcome) × Directional_Consistency × Gradient_Position
```

| Variable | Meaning |
|----------|---------|
| `Base_Flow` | Base probability flow for this outcome (pp) |
| `Directional_Consistency` | Proportion of adjacent outcomes in same direction with positive flow (0~1) |
| `Gradient_Position` | Position in probability gradient (higher probability = greater amplification potential) |

### Amplification Effect Safeguards

**Safeguard 1: Domain Awareness Validation**

Amplification effect must be cross-validated with match intelligence:

| Intelligence Assessment | Flow Direction | Amplification Verdict |
|------------------------|----------------|----------------------|
| Strong team + High offensive efficiency | Positive flow toward big win | **Confirmed** ✅ |
| Strong team + Conservative style | Positive flow toward big win | **Questionable** ⚠️ |
| Weak team + Defensive vulnerabilities | Positive flow toward big win | **Enhanced** ✅✅ |
| No clear intelligence | Positive flow toward big win | **Possible** ✅ (downweighted) |

**Safeguard 2: Base Flow Threshold**

Only enable amplification effect when base flow (Base_Flow) ≥ threshold (recommended 2pp).

**Safeguard 3: Kelly Criterion Variant**

Kelly's core idea—**adjust investment proportion based on signal strength**—is borrowed for scheme design.

---

## Domain Awareness System

### Definition of Situational Awareness

**Domain Awareness** = Complete coverage of all available information sources.

**Situational Awareness** = Real-time understanding of current match context.

### Match Intelligence Integration

| Intelligence Dimension | Data Points | Weight |
|-----------------------|-------------|--------|
| **Strength Indicators** | FIFA ranking, squad value, recent form | High |
| **Tactical Context** | Offensive/defensive style, goals per game, clean sheets | High |
| **Motivational Factors** | Qualification situation, pressure, squad rotation | Medium |
| **Market Consensus** | Volume distribution, expert prediction consistency | Medium |

### Signal Validation Matrix

Each probability flow signal must be cross-validated with match intelligence:

```python
Confidence = Flow_Strength × Intelligence_Support × Market_Consensus
```

| Confidence | Condition | Action |
|------------|-----------|--------|
| **High** | All three dimensions aligned | Full weight in scheme |
| **Medium** | Two dimensions aligned | Downweighted inclusion |
| **Low** | Only one dimension supporting | Only include in high-probability small-amount combinations |
| **Negative** | Dimensional conflict | Exclude or use as contrarian signal |

---

## Value Assessment Engine

### Core Philosophy

The Value Assessment Engine implements Expected Domain Perception's **Core Methodology**:

```
NOT: Research "most likely to happen"
BUT: Assess "underestimated by market"
```

**Key Insight**:
- Low probability events (high odds) ≠ will not happen
- As long as odds are high enough, even low success rate can have **positive Expected Value**
- Few big successes can cover many small failures (Power Law Distribution)

### Expected Value Calculation

```python
EV = P(success) × (Odds - 1) - P(fail) × 1
```

**Condition for Value**: Market_Odds > Fair_Odds (EV > 0)

### Value Ratio

```python
Value_Ratio = Market_Odds / Fair_Odds

Example:
- Market odds = 8.0
- Our assessed probability = 15%
- Fair odds = 1/0.15 = 6.67
- Value Ratio = 8.0 / 6.67 = 1.20 (> 1.0 → VALUE!)
```

### Value Classification

| Classification | Value Ratio | Strategy |
|---------------|-------------|----------|
| **Exceptional** | ≥ 1.30 | Focus, increase allocation |
| **High** | ≥ 1.20 | Priority selection, Kelly allocation |
| **Moderate** | ≥ 1.10 | Optional, cautious allocation |
| **Fair** | ≥ 1.00 | No edge, skip |
| **Poor** | < 1.00 | Negative EV, strictly exclude |

### "N Trials, 1 Success" Portfolio

```python
# 20 opportunities, 5% of bankroll each
# Average odds 8.0, true probability 15%

Expected Results:
- Successes: 20 × 15% = 3 opportunities
- Failures: 20 × 85% = 17 opportunities

Profit Calculation:
- 3 successes profit: 3 × 5% × 8.0 = 120% of bankroll
- 17 failures: 17 × 5% = 85% of bankroll
- Net Profit: 120% - 85% = +35% of bankroll!
```

### Synergy with Domain Awareness System

```
Domain Awareness                    Value Assessment Engine
      │                                     │
      │  Evaluate "real possibility"        │  Determine "if value exists"
      │  Identify underestimated events     │  Calculate Expected Value
      │                                     │
      └──────────────┬──────────────────────┘
                     │
                     ▼
             Positive EV + High Confidence
                  = Value Opportunity Signal
```

---

## Scheme Design Engine

### Three Principles (Non-Negotiable)

All schemes **must** satisfy the following three principles. Any scheme violating any principle **must not be output**:

| # | Principle | Implementation Rules |
|---|-----------|---------------------|
| 1 | **Respect Probability Flow** | Each leg of each ticket must have positive probability flow. Zero-flow legs acceptable only when no positive alternative exists. **Negative-flow legs strictly prohibited.** |
| 2 | **Respect Asymmetric Returns** | Each ticket must provide meaningful return potential. Minimum target: 3x return. Conservative "safe ticket" budget not exceeding 20% of total budget. |
| 3 | **Respect Rules** | Same match different markets cannot parlay. Correct score max 4-fold. Each ticket max 99x multiplier. Each ticket max ¥20,000. |

**Priority of Three Principles**: Principle 1 > Principle 3 > Principle 2.

### Mixed Parlay Complete Rules

#### Basic Rules

| Rule | Description |
|------|-------------|
| **Different matches can mix** | Different markets from different matches **can** parlay |
| **Same match cannot mix** | Different markets from same match **cannot** parlay |
| **Minimum stake** | Each combination minimum ¥2 |
| **Single ticket multiplier cap** | Single ticket maximum 99x |
| **Single ticket amount cap** | Single ticket maximum ¥20,000 |

#### Parlay Depth Limits

| Contains Correct Score/Half-Time | Max Parlay Depth |
|----------------------------------|-----------------|
| No | Max 8-fold |
| Contains Correct Score | Max 4-fold |
| Contains Half-Time | Max 4-fold |
| Contains Total Goals | Max 6-fold |

---

## Rule Compliance Layer

### Validation Pipeline

Each generated ticket must pass the following validation pipeline:

```
For each ticket:
  ✓ 1. No legs from same match different markets
  ✓ 2. Contains correct score/half-time → total parlay depth ≤ 4
  ✓ 3. Each stake × combinations ≤ ¥50 (single physical ticket limit)
  ✓ 4. Each stake ≥ ¥2
  ✓ 5. Multiplier ≤ 99
  ✓ 6. All legs have positive probability flow
  ✓ 7. Ticket provides meaningful upside (non-anchor tickets ≥ 3x)
```

---

## Output Generation

### Multi-Layer Output

| Layer | Audience | Content |
|-------|----------|---------|
| **Analysis Report** | Analysts | Complete probability flow table, signal strength, intelligence cross-validation |
| **Scheme Summary** | Users | Ticket list, cost, expected return, coverage map |
| **Narrative** | Operators | Concise verbal instructions |

### Quality Checklist

Before presentation to users, all schemes must pass each item:

- [ ] All legs have positive probability flow
- [ ] All legs have match intelligence support (or explicitly marked as "pure flow" signal)
- [ ] No rule violations
- [ ] Total cost matches user budget
- [ ] Each ticket cost calculation verified
- [ ] Market diversity coverage
- [ ] Match coverage meets standard
- [ ] No duplicate ticket combinations
- [ ] Narrative unambiguous

---

## Academic Foundation

### Core Theoretical Foundations

| Theory | Literature | Application |
|--------|------------|-------------|
| Shin Odds Decomposition | Shin (1992) | True probability extraction |
| Bayesian Updating | Gelman et al. (2013) | Probability flow interpretation |
| Kelly Criterion | Kelly (1956) | Capital allocation heuristic |
| Time Series Momentum | Moskowitz et al. (2012) | Amplification effect basis |
| Information Cascade | Banerjee (1992) | Herding behavior modeling |
| Prospect Theory | Kahneman & Tversky (1979) | Bias mitigation |
| Modern Portfolio Theory | Markowitz (1952) | Diversification strategy |
| Prediction Market Prices | Wolfers & Zitzewitz (2006) | Probability interpretation basis |
| OODA Loop | Boyd (1987) | Operational architecture |

For complete reference list, see [docs/theory/references.md](docs/theory/references.md)

---

## Quick Start

### Installation

```bash
# Python
pip install spaf-framework

# JavaScript/TypeScript
npm install spaf-framework
```

### Python Example

```python
from spaf import (
    ProbabilityEngine,
    FlowAmplificationEngine,
    DomainAwarenessSystem,
    ValueAssessmentEngine,
)

# Initialize engines
engine = ProbabilityEngine()
amplifier = FlowAmplificationEngine()
awareness = DomainAwarenessSystem()
value_engine = ValueAssessmentEngine()

# Calculate true probability
result = engine.calculate_true_probability({'home': 1.5, 'draw': 4.0, 'away': 6.0})

# Analyze probability flow
flow_report = engine.analyze_flow(initial_snapshot, latest_snapshot)

# Calculate amplification effect
amp_report = amplifier.calculate_amplification(flow_report, outcome_probs)

# Domain awareness analysis
domain_report = awareness.analyze_match(match_intel, flow_confidences)

# Value assessment analysis - Core: Identify positive EV opportunities
value_opportunities = value_engine.identify_value_opportunities(
    market_odds={'home': 1.8, 'draw': 3.5, 'away': 5.0},
    assessed_probabilities={'home': 0.50, 'draw': 0.30, 'away': 0.25},
    flow_confidences={'home': 0.7, 'draw': 0.5, 'away': 0.6},
    intelligence_confidences={'home': 0.6, 'draw': 0.5, 'away': 0.8},
)

# Create value portfolio
portfolio = value_engine.calculate_portfolio_recommendations(
    value_opportunities=value_opportunities,
    total_bankroll=10000,
)
```

### TypeScript Example

```typescript
import { ProbabilityEngine, FlowAnalyzer, SchemeDesigner } from 'spaf-framework';

const engine = new ProbabilityEngine();
const analyzer = new FlowAnalyzer();
const designer = new SchemeDesigner();

const trueProbs = engine.calculateTrueProbability({ home: 1.5, draw: 4.0, away: 6.0 });
const flowReport = analyzer.analyzeFlow(initialProbs, latestProbs);
const schemes = designer.generateSchemes(flowReport, { budget: 100 });
```

For more examples, see the [examples/](examples/) directory.

---

## API Documentation

For complete API documentation, see [docs/api/](docs/api/).

---

## MCP Integration

This framework provides an MCP (Model Context Protocol) server, enabling AI assistants to directly invoke analysis capabilities.

### Configuration

```json
{
  "mcpServers": {
    "spaf": {
      "command": "spaf-mcp-server",
      "args": []
    }
  }
}
```

### Available Tools

- `calculate_true_probability` - Calculate true probability
- `analyze_flow` - Analyze probability flow
- `calculate_amplification` - Calculate amplification effect
- `validate_scheme` - Validate scheme compliance
- `generate_schemes` - Generate optimized schemes

For detailed documentation, see [mcp/README.md](mcp/README.md).

---

## Skill Integration

This framework can be used as an AI Agent Skill, supporting rapid integration into various AI assistants.

For detailed documentation, see [skill/README.md](skill/README.md).

---

## Contributing

We welcome community contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) to learn how to participate.

### Development Environment Setup

```bash
# Clone repository
git clone https://github.com/your-org/spaf-framework.git
cd spaf-framework

# Python development
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# JavaScript development
npm install
npm run build
```

### Running Tests

```bash
# Python tests
pytest tests/python/

# JavaScript tests
npm test
```

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

---

## Disclaimer

**This framework is for ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY.**

- This framework does not constitute any investment advice or prediction advice.
- Any decisions made using this framework are the user's sole responsibility.
- The author is not responsible for any losses incurred through use of this framework.
- Please comply with laws and regulations in your jurisdiction.

---

*Providing marginal advantage through structured analysis, rigorous probability theory, and domain cognition—while acknowledging that in probability analysis, probability itself always has the last laugh.*

*© 2026 — Expected Domain Perception - For Academic Research and Educational Purposes Only.*

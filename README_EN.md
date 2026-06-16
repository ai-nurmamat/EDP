# SPAF - Sports Analytics Framework

## ⚠️ ACADEMIC RESEARCH PURPOSES ONLY

**IMPORTANT NOTICE**: This framework is intended **exclusively for academic research and educational purposes**. It provides statistical analysis tools for studying sports event probabilities and market dynamics.

### Legal Disclaimer
- This software is **not** designed for, nor should it be used for, any form of financial speculation or gambling activities.
- Users must comply with all applicable laws and regulations in their jurisdiction.
- The authors and contributors assume no liability for any misuse of this software.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Core Innovation Features](#core-innovation-features)
3. [Technical Architecture](#technical-architecture)
4. [Installation](#installation)
5. [Quick Start](#quick-start)
6. [Documentation](#documentation)
7. [API Reference](#api-reference)
8. [Development](#development)
9. [Contributing](#contributing)
10. [License](#license)
11. [Academic References](#academic-references)

---

## Introduction

SPAF (Sports Analytics Framework) is a comprehensive, domain-aware, situational-awareness-driven probability analysis system designed for advanced sports analytics research. The framework implements cutting-edge statistical methods and machine learning techniques to analyze sports event probabilities, market dynamics, and information flow patterns.

### Key Features

- **True Probability Calculation**: Extract unbiased probabilities from market quotes using the Shin method
- **Probability Flow Analysis**: Track temporal probability changes with momentum scoring
- **Flow Amplification Effect**: Detect and quantify cascading information propagation effects
- **Domain Awareness System**: Integrate multi-source intelligence for comprehensive situational assessment
- **Strategy Engine**: Generate optimized analysis strategies based on validated principles

---

## Core Innovation Features

### 1. Domain-Aware System

A comprehensive intelligence fusion system that integrates multiple data sources:

- **Multi-source Intelligence Integration**: Combine rankings, historical data, recent form, tactical analysis, injury reports, motivation factors, and market signals
- **Cross-validation Mechanism**: Validate information consistency across different sources
- **Confidence Quantification**: Assign confidence levels to each data point based on reliability
- **Situational Assessment**: Generate holistic match analysis incorporating all available intelligence

### 2. Probability Flow Analysis

An advanced temporal analysis system for tracking probability dynamics:

- **Basic Flow Calculation**: Measure probability changes between time points (basis points)
- **Momentum Scoring**: Evaluate the strength and direction of probability movement
- **Velocity & Acceleration**: Assess the rate and acceleration of probability changes
- **Aggregate Momentum**: Calculate overall market sentiment from individual outcome flows

### 3. Flow Amplification Effect

A novel mechanism for detecting cascading information propagation:

- **Gradient Graph Propagation**: Build and traverse outcome relationship graphs
- **Directional Consistency**: Evaluate signal alignment across adjacent outcomes
- **Cascade Risk Assessment**: Quantify the risk of market-wide information cascades
- **Six-Level Amplification Classification**: From NONE to EXCEPTIONAL signal strength

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Domain Awareness System                  │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────────────┐   │
│  │Ranking  │ │Form Data│ │Injury   │ │H2H Analysis     │   │
│  │Analysis │ │Analysis │ │Reports  │ │Tactical Scouting│   │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────────┬─────────┘   │
└───────┼───────────┼───────────┼────────────────┼─────────────┘
        │           │           │                │
        ▼           ▼           ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                    Probability Engine                        │
│  ┌─────────────────────┐  ┌─────────────────────────────┐   │
│  │  True Probability   │  │      Bayesian Inference     │   │
│  │  Calculation (Shin) │  │  Beta-Binomial Conjugate    │   │
│  └──────────┬──────────┘  └──────────────┬──────────────┘   │
│             │                            │                  │
│             ▼                            ▼                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │            Probability Flow Analysis                │    │
│  │  Momentum | Velocity | Acceleration | Significance │    │
│  └───────────────────────────┬─────────────────────────┘    │
└──────────────────────────────┼───────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               Flow Amplification Engine                     │
│  ┌─────────────────────┐  ┌─────────────────────────────┐   │
│  │  Gradient Graph     │  │     Cascade Risk Model      │   │
│  │  Construction       │  │  6-Level Classification     │   │
│  └─────────────────────┘  └─────────────────────────────┘   │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Strategy Engine                           │
│  ┌─────────────────────┐  ┌─────────────────────────────┐   │
│  │   Validation Rules  │  │    Risk-Adjusted Design    │   │
│  │   (3 Principles)    │  │  MPT + Kelly Optimization   │   │
│  └─────────────────────┘  └─────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Installation

### Python

```bash
pip install spaf-framework
```

### TypeScript/JavaScript

```bash
npm install spaf-framework
```

---

## Quick Start

### Python Example

```python
from spaf import ProbabilityEngine, FlowAmplificationEngine, StrategyEngine

# Initialize engines
engine = ProbabilityEngine()
amplifier = FlowAmplificationEngine()
strategy_engine = StrategyEngine()

# Calculate true probability
result = engine.calculate_true_probability({
    'home': 1.50,
    'draw': 4.20,
    'away': 6.00
})

print(f"Market Margin: {result.market_margin:.2%}")
print(f"True Probabilities: {result.true_probabilities}")
```

### TypeScript Example

```typescript
import { ProbabilityEngine, MarketType } from 'spaf-framework';

const engine = new ProbabilityEngine();

const result = engine.calculateTrueProbability({
    home: 1.50,
    draw: 4.20,
    away: 6.00
});

console.log(`Market Margin: ${result.marketMargin.toFixed(2)}%`);
console.log(`True Probabilities:`, result.trueProbabilities);
```

---

## Documentation

Full documentation is available at:
- [API Reference](docs/api.md)
- [User Guide](docs/user_guide.md)
- [Developer Guide](docs/developer_guide.md)
- [Mathematical Foundations](docs/mathematical_foundations.md)

---

## API Reference

### ProbabilityEngine

```python
calculate_true_probability(quotes: dict) -> TrueProbabilityResult
analyze_flow(initial: ProbabilitySnapshot, latest: ProbabilitySnapshot) -> FlowReport
bayesian_update(prior: BayesianPrior, successes: int, trials: int) -> BayesianPosterior
```

### FlowAmplificationEngine

```python
calculate_amplification(flow_report: FlowReport, probabilities: dict, gradient_graph: GradientGraph) -> AmplificationReport
build_correct_score_gradient() -> GradientGraph
```

### StrategyEngine

```python
generate_strategies(amplification_report: AmplificationReport, budget: float, match_data: dict) -> StrategyBundle
validate_strategy(strategy: Strategy) -> ValidationResult
```

---

## Development

### Setup Development Environment

```bash
git clone https://github.com/spaf-framework/spaf.git
cd spaf

# Python
python -m venv venv
source venv/bin/activate
pip install -e .[dev]

# JavaScript/TypeScript
cd js
npm install
npm run build
```

### Running Tests

```bash
# Python tests
python -m pytest tests/ -v

# JavaScript tests
npm test
```

### Linting

```bash
# Python
flake8 src/ tests/

# JavaScript
npm run lint
```

---

## Contributing

We welcome contributions from the academic community. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Code of Conduct

This project adheres to the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

## License

SPAF is released under the MIT License. See [LICENSE](LICENSE) for details.

### MIT License with Additional Warnings

The MIT license grants broad permissions, but users must understand:

1. **No Warranty**: This software is provided "as is" without warranty of any kind
2. **Academic Use Only**: The software is designed for research purposes
3. **Legal Compliance**: Users are solely responsible for legal compliance
4. **No Liability**: Authors are not liable for any damages or losses

---

## Academic References

The SPAF framework is built upon extensive academic research:

1. **Shin, H. S.** (1992). "Prices of State Contingent Claims with Insider Trading." *Review of Financial Studies*.
2. **Kelly, J. L.** (1956). "A New Interpretation of Information Rate." *Bell System Technical Journal*.
3. **Markowitz, H.** (1952). "Portfolio Selection." *Journal of Finance*.
4. **Elo, A.** (1978). "The Rating of Chessplayers, Past and Present." Arco.
5. **Savage, L. J.** (1954). "The Foundations of Statistics." Wiley.
6. **De Finetti, B.** (1937). "Foresight: Its Logical Laws, Its Subjective Sources." *Annales de l'Institut Henri Poincaré*.
7. **Kahneman, D., & Tversky, A.** (1979). "Prospect Theory: An Analysis of Decision under Risk." *Econometrica*.
8. **Gigerenzer, G., & Selten, R.** (2001). "Bounded Rationality: The Adaptive Toolbox." MIT Press.
9. **Holt, C. A., & Laury, S. K.** (2002). "Risk Aversion and Incentive Effects." *American Economic Review*.
10. **Camerer, C.** (2003). "Behavioral Game Theory: Experiments in Strategic Interaction." Princeton University Press.
11. **Thaler, R. H.** (2015). "Misbehaving: The Making of Behavioral Economics." W.W. Norton.
12. **Barberis, N., & Thaler, R.** (2003). "A Survey of Behavioral Finance." *Handbook of the Economics of Finance*.

---

## Citation

If you use SPAF in your academic research, please cite:

```bibtex
@software{spaf2024,
  author = {SPAF Team},
  title = {SPAF: Sports Analytics Framework},
  year = {2024},
  version = {4.2.0},
  url = {https://github.com/spaf-framework/spaf},
  note = {For academic research purposes only}
}
```

---

**SPAF Team** | Academic Research Framework | v4.2.0

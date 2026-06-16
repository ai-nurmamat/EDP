# Expected Domain Perception Skill

AI Agent Skill for Expected Domain Perception methodology.

## ⚠️ Disclaimer

**This skill is for ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY.**

Sports prediction involves real financial risk. No system can guarantee profits.

## Description

This skill provides AI agents with the ability to analyze sports prediction markets using probability flow analysis, amplification effects, and scheme optimization based on the Three Principles.

## Capabilities

- **True Probability Calculation**: Extract true probabilities from bookmaker odds
- **Probability Flow Analysis**: Analyze market movement and identify positive/negative flows
- **Amplification Effect Calculation**: Identify high-potential outcomes through flow amplification
- **Scheme Generation**: Generate optimized schemes within budget constraints
- **Validation**: Validate schemes against Three Principles and rules

## Usage

### Natural Language Commands

```
"Analyze the odds for this match: home 1.5, draw 4.2, away 6.0"
"What is the probability flow for this market?"
"Generate schemes with a budget of 100"
"Validate this scheme for compliance"
```

### Example Workflow

```
User: I have odds for a match: home 1.5, draw 4.2, away 6.0. 
      The initial probabilities were 65% home, 24% draw, 16% away.
      Now they are 68% home, 22% draw, 14% away.
      Analyze this and suggest schemes with budget 100.

AI: I'll analyze this step by step:

1. First, let me calculate the true probabilities...
   [Calls calculate_true_probability]
   
   True probabilities: Home 63.2%, Draw 22.6%, Away 15.8%
   Bookmaker margin: 5.4%

2. Now analyzing the probability flow...
   [Calls analyze_flow]
   
   Flow Analysis:
   - Home: +3.0pp (positive, high significance) ↑
   - Draw: -2.0pp (negative, medium significance) ↓
   - Away: -2.0pp (negative, medium significance) ↓

3. The positive flow on home indicates market confidence is increasing.
   This is a strong signal for home win.

4. Generating optimized schemes...
   [Calls generate_schemes]
   
   Recommended Schemes:
   - Scheme 1: Home win (single), Stake ¥20, Potential return ¥10
   - Scheme 2: Home win + Over 2.5 goals (2-fold), Stake ¥15, Potential return ¥45

Total allocated: ¥35 of ¥100 budget
Remaining budget: ¥65 for additional diversification

⚠️ Remember: This is for educational purposes only. No system guarantees profits.
```

## Configuration

### Skill Registration

Add to your AI agent's skill configuration:

```json
{
  "skills": [
    {
      "name": "expected-domain-perception",
      "description": "Sports probability analysis framework",
      "version": "1.0.0",
      "entry_point": "edp.skill:analyze",
      "capabilities": [
        "probability_calculation",
        "flow_analysis",
        "amplification_analysis",
        "scheme_generation",
        "validation"
      ]
    }
  ]
}
```

## API Reference

### `analyze(odds: dict, initial_probs: dict, latest_probs: dict, budget: float) -> dict`

Complete analysis workflow.

**Parameters:**
- `odds`: Current bookmaker odds
- `initial_probs`: Initial probability snapshot
- `latest_probs`: Latest probability snapshot
- `budget`: Total budget for schemes

**Returns:**
- Complete analysis report with schemes

---

### `calculate_true_probability(odds: dict) -> dict`

Calculate true probabilities from odds.

---

### `analyze_flow(initial_probs: dict, latest_probs: dict) -> dict`

Analyze probability flow.

---

### `generate_schemes(flow_report: dict, budget: float) -> dict`

Generate optimized schemes.

---

### `validate_scheme(scheme: dict) -> dict`

Validate scheme compliance.

## Three Principles

All generated schemes must satisfy:

1. **Respect Probability Flow**: All legs must have positive flow
2. **Respect Asymmetric Returns**: Minimum 3x return potential
3. **Respect Rules**: Comply with all betting rules

## Installation

```bash
pip install expected-domain-perception-skill
```

## Development

```bash
# Clone repository
git clone https://github.com/your-org/expected-domain-perception.git
cd expected-domain-perception/skill

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

## License

MIT License - See LICENSE file for details.

## Disclaimer

**This skill is for ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY.**

- This skill does not constitute any investment advice or gambling advice.
- Any decisions made using this skill are the user's sole responsibility.
- The author is not responsible for any losses incurred through use of this skill.
- Please comply with laws and regulations in your jurisdiction.

# Expected Domain Perception MCP Server

Model Context Protocol (MCP) server for the Expected Domain Perception framework.

## ⚠️ Disclaimer

**This server is for ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY.**

Sports prediction involves real financial risk. No system can guarantee profits.

## Installation

```bash
pip install expected-domain-perception-mcp
```

## Configuration

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "expected-domain-perception": {
      "command": "edp-mcp-server",
      "args": []
    }
  }
}
```

## Available Tools

### `calculate_true_probability`

Calculate true probabilities from bookmaker odds by removing the overround/margin.

**Parameters:**
- `odds` (object): Dictionary mapping outcomes to decimal odds

**Example:**
```json
{
  "odds": {
    "home": 1.50,
    "draw": 4.20,
    "away": 6.00
  }
}
```

**Returns:**
```json
{
  "true_probabilities": {
    "home": 0.632,
    "draw": 0.226,
    "away": 0.158
  },
  "overround": 0.054
}
```

---

### `analyze_flow`

Analyze probability flow between two time points.

**Parameters:**
- `initial_probabilities` (object): Initial probability snapshot
- `latest_probabilities` (object): Latest probability snapshot
- `market_type` (string, optional): Market type (default: "1X2")

**Returns:**
- Flow report with direction and significance for each outcome

---

### `calculate_amplification`

Calculate amplification effect for probability flows.

**Parameters:**
- `flow_report` (object): Flow analysis report
- `gradient_map` (object): Map of outcomes to adjacent outcomes
- `outcome_probabilities` (object): Current true probabilities
- `domain_confidence` (object, optional): Confidence scores from domain awareness

**Returns:**
- Amplification report with scores and levels

---

### `validate_scheme`

Validate a scheme against Three Principles and rules.

**Parameters:**
- `legs` (array): List of scheme legs
- `multiplier` (integer, optional): Multiplier (default: 1)
- `stake_per_combination` (number, optional): Investment amount (default: 2.0)

**Returns:**
- Validation result with any errors

---

### `generate_schemes`

Generate optimized schemes within budget.

**Parameters:**
- `amplification_report` (object): Amplification report
- `budget` (number): Total budget to allocate
- `match_data` (object): Match information
- `max_schemes` (integer, optional): Maximum schemes to generate (default: 10)

**Returns:**
- Scheme bundle with optimized schemes

## Usage with AI Assistants

Once configured, you can use natural language to interact with Expected Domain Perception:

```
User: Calculate the true probability for odds home 1.5, draw 4.2, away 6.0

AI: I'll calculate the true probabilities by removing the bookmaker margin...

[Calls calculate_true_probability tool]

The true probabilities are:
- Home: 63.2%
- Draw: 22.6%
- Away: 15.8%

The bookmaker margin (overround) is 5.4%.
```

## Development

```bash
# Clone repository
git clone https://github.com/your-org/expected-domain-perception.git
cd expected-domain-perception/mcp

# Install dependencies
pip install -e ".[dev]"

# Run server
python server.py
```

## License

MIT License - See LICENSE file for details.

## Disclaimer

**This server is for ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY.**

- This server does not constitute any investment advice or gambling advice.
- Any decisions made using this server are the user's sole responsibility.
- The author is not responsible for any losses incurred through use of this server.
- Please comply with laws and regulations in your jurisdiction.

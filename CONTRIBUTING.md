# Contributing to Expected Domain Perception

Thank you for your interest in contributing to the Expected Domain Perception methodology!

## ⚠️ Important Notice

**This project is for ACADEMIC RESEARCH AND EDUCATIONAL PURPOSES ONLY.**

Contributions must align with this purpose. We do not accept contributions that:
- Promote or encourage gambling as a way to make money
- Claim to "beat the system" or guarantee profits
- Violate any laws or regulations
- Encourage irresponsible behavior

## How to Contribute

### Reporting Issues

1. Check if the issue already exists
2. Use the issue template
3. Provide clear reproduction steps
4. Include relevant environment details

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Commit with clear messages
7. Push to your branch
8. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/expected-domain-perception.git
cd expected-domain-perception

# Python setup
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -e ".[dev]"

# Node.js setup
npm install

# Run tests
pytest tests/python/
npm test
```

### Code Style

**Python:**
- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use `black` for formatting
- Use `ruff` for linting

**TypeScript:**
- Use strict mode
- Maximum line length: 100 characters
- Use Prettier for formatting

### Testing

- All new code must have tests
- Maintain or improve code coverage
- Run both Python and JavaScript tests

### Documentation

- Update README if needed
- Add docstrings to all public functions
- Update API documentation

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Open an issue for any questions about contributing.

---

Thank you for helping improve Expected Domain Perception! 🎯

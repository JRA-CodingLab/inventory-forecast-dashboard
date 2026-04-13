# Contributing

Thank you for considering contributing to **Inventory Forecast Dashboard**! Here's how to get started.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/<your-username>/inventory-forecast-dashboard.git
   cd inventory-forecast-dashboard
   ```
3. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install pytest httpx
```

### Frontend

```bash
cd frontend
npm install
```

## Running Tests

```bash
# From project root
pytest -v
```

All tests must pass before submitting a pull request.

## Code Style

- **Python**: Follow PEP 8. Use type hints where practical.
- **JavaScript/JSX**: Use consistent formatting. Prefer functional components with hooks.
- **Commits**: Use clear, descriptive commit messages. One logical change per commit.

## Pull Request Process

1. Ensure all tests pass locally
2. Update documentation if you changed APIs or behavior
3. Add entries to `CHANGELOG.md` under an `[Unreleased]` section
4. Submit your PR against the `main` branch
5. Describe what changed and why in the PR description

## Reporting Issues

Open an issue on GitHub with:
- A clear title and description
- Steps to reproduce (if applicable)
- Expected vs actual behavior
- Environment details (OS, Python version, Node version)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

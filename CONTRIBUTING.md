# Contributing to DAVID CIS

Thank you for your interest in contributing!

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/david-cyber-intelligence-system`
3. **Create a branch**: `git checkout -b feature/my-feature`
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Make your changes**
6. **Test** your changes
7. **Push** and open a **Pull Request**

## Project Structure

```
david-cyber-intelligence-system/
├── engines/          # Core analysis engines (malware, osint, pentest, etc.)
├── tracking/         # Flight, ship, satellite, attack map
├── intelligence/     # Threat intel aggregator (OTX, AbuseIPDB, etc.)
├── security/         # CAI engine, WAF, OpenVAS, Cloudflare, local SIEM
├── automation/       # Scheduler + alerting (Telegram, email)
├── bounty/           # Bug bounty platform API
├── core/             # LLM brain, task router, REST API
├── dashboard/        # Web dashboard HTML
├── gui_app.py        # Main Tkinter GUI
├── launcher.py       # Animated splash screen
├── models/           # LLM model files (.gguf)
├── data/             # SQLite databases, cached IOCs
└── config/           # Configuration files
```

## Adding a New Engine

1. Create `engines/my_engine.py` with a class `MyEngine`
2. Add an `analyze(target, **kwargs) -> dict` method
3. Register in `core/task_router.py`
4. Add a GUI tab in `gui_app.py`
5. Document in `README.md`

## Code Style

- Python 3.10+
- PEP 8 formatting
- Type hints where practical
- Docstrings for all public methods
- `loguru` for logging (not `print`)

## Reporting Bugs

Open a GitHub Issue with:
- OS and Python version
- Steps to reproduce
- Error output / traceback
- Expected vs actual behavior

## Security Disclosure

For security vulnerabilities, **do not open a public issue**.
Email: `david@nexuzytech.com`

## License

This is a proprietary project. Contributions are accepted under a Contributor License Agreement (CLA).
By submitting a PR, you agree your code may be included under the project's license.

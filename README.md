![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![GitHub stars](https://img.shields.io/github/stars/dsoles-eth/dev-secrets-scanner)

# Dev Secrets Scanner

**Dev Secrets Scanner** (`dev-secrets-scanner`) is a lightweight, high-performance CLI tool designed to secure your codebase before deployment. By scanning local repositories for exposed secrets, API keys, and sensitive credentials, it empowers backend developers and DevSecOps engineers to enforce pre-commit security and harden local environments. Built with Python, `click`, and efficient regex patterns, it integrates seamlessly into your development lifecycle to prevent credential leakage at the source.

## Features

- **🔍 Comprehensive Scanning**: Automatically traverses local directories to detect hardcoded secrets and API keys.
- **🛡️ Pattern & Hash Verification**: Combines keyword detection with hash verification to minimize false positives.
- **⚡ CI/CD Ready**: Provides structured exit codes and machine-readable outputs for seamless pipeline integration.
- **⚙️ Configurable Exclusions**: Easily manage ignore lists via YAML or TOML configuration files.
- **📄 Flexible Reporting**: Export scan results as JSON or Markdown for documentation and sharing.
- **🐍 Pure Python**: Zero native dependencies; lightweight installation via PyPI.

## Installation

Ensure you have Python 3.9 or higher installed. You can install the package directly from PyPI:

```bash
pip install dev-secrets-scanner
```

*Requirements:*
- Python 3.9+
- Click
- PyYAML
- TOML

## Quick Start

Run a basic scan on your current directory and output the results in Markdown format:

```bash
dev-secrets-scanner scan . --format md
```

**Output Example:**
```text
Scan complete. Found 2 potential secrets.
Results saved to: scan_report.md
```

## Usage

### Basic Scan
Scan the current directory for sensitive patterns.

```bash
dev-secrets-scanner scan --output-format json
```

### Scan with Exclusions
Use a configuration file to skip specific directories or file types.

```bash
# config.yaml
paths_to_ignore:
  - "vendor"
  - "node_modules"
  - ".git"

file_extensions:
  - ".log"
  - ".tmp"

# Run scan
dev-secrets-scanner scan ./src -c config.yaml
```

### CI/CD Integration
Set the exit code based on findings to fail builds automatically.

```bash
# If secrets are found, exit code is 1 (failure)
dev-secrets-scanner scan . --fail-on-secrets
echo $?
```

### Custom Output Paths
Specify where to save your report.

```bash
dev-secrets-scanner scan . --output ./reports/secrets-report.json --output-format json
```

## Architecture

The project is modular to ensure maintainability and ease of extension. Key modules include:

| Module | Description |
| :--- | :--- |
| **`cli_interface`** | Handles command-line argument parsing and user interaction flows. |
| **`scanner_core`** | Orchestrates the scanning process across specified directories and file types. |
| **`pattern_matcher`** | Detects common patterns and keywords indicative of exposed credentials. |
| **`hash_checker`** | Verifies against known sensitive string hashes to reduce false positives. |
| **`exclusion_handler`** | Manages ignore lists and configuration of sensitive file types to skip. |
| **`reporter`** | Formats scan results into JSON or Markdown for consumption. |
| **`ci_integration`** | Provides structured exit codes and output for CI/CD pipeline integration. |

## Contributing

We welcome contributions from the community! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

Please ensure your code follows the existing style and passes all unit tests before submission.

## License
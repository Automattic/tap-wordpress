# tap-wordpress

[![CI](https://github.com/your-org/tap-wordpress/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/tap-wordpress/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/your-org/tap-wordpress/branch/main/graph/badge.svg)](https://codecov.io/gh/your-org/tap-wordpress)
[![PyPI version](https://badge.fury.io/py/tap-wordpress.svg)](https://badge.fury.io/py/tap-wordpress)
[![Python versions](https://img.shields.io/pypi/pyversions/tap-wordpress.svg)](https://pypi.org/project/tap-wordpress/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A [Singer](https://www.singer.io/) tap for extracting data from WordPress REST API, built with the [Meltano Singer SDK](https://sdk.meltano.com/).

## Quick Start

1. **Install the tap**
   ```bash
   pipx install tap-wordpress
   ```

2. **Create a config file**
   ```json
   {
     "base_url": "https://your-wordpress-site.com",
     "per_page": 100
   }
   ```

3. **Run discovery to see available streams**
   ```bash
   tap-wordpress --config config.json --discover
   ```

4. **Extract data**
   ```bash
   tap-wordpress --config config.json --catalog catalog.json
   ```

## Features

- ✅ **Complete WordPress REST API coverage** - Extract all major WordPress entities
- ✅ **Incremental sync** - Efficient updates for posts, pages, comments, and media
- ✅ **No authentication required** - Works with public WordPress REST API endpoints
- ✅ **Production ready** - Comprehensive error handling, logging, and retry logic
- ✅ **Singer compliant** - Full Singer specification compliance with state management
- ✅ **Meltano native** - Built with Meltano SDK for seamless integration

## Supported Streams

| Stream | Incremental | Description |
|--------|------------|-------------|
| `posts` | ✅ | Blog posts with content, metadata, and relationships |
| `pages` | ✅ | WordPress pages with hierarchy and content |
| `comments` | ✅ | Comments on posts and pages with threading |
| `media` | ✅ | Media library items (images, files, etc.) |
| `users` | ❌ | User profiles, roles, and capabilities |
| `categories` | ❌ | Post categories with hierarchical structure |
| `tags` | ❌ | Post tags and taxonomies |

## Installation

### Using pipx (recommended)
```bash
pipx install tap-wordpress
```

### Using pip
```bash
pip install tap-wordpress
```

### From source
```bash
git clone https://github.com/your-org/tap-wordpress.git
cd tap-wordpress
pip install -e .
```

## Configuration

### Required Settings

| Setting | Description |
|---------|-------------|
| `base_url` | WordPress site base URL (e.g., `https://example.com`) |

### Optional Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `start_date` | `null` | Start date for incremental sync (ISO 8601) |
| `per_page` | `100` | Number of records to fetch per page |
| `timeout` | `30` | Request timeout in seconds |

### Configuration Examples

**Basic configuration** (WordPress.org)
```json
{
  "base_url": "https://wordpress.org"
}
```

**With custom settings**
```json
{
  "base_url": "https://your-wordpress-site.com",
  "per_page": 50,
  "start_date": "2023-01-01T00:00:00Z"
}
```

## Usage

### Standalone CLI

```bash
# Discover available streams
tap-wordpress --config config.json --discover > catalog.json

# Extract data to stdout
tap-wordpress --config config.json --catalog catalog.json

# Extract with state management
tap-wordpress --config config.json --catalog catalog.json --state state.json
```

### With Meltano

1. **Add to your Meltano project**
   ```bash
   cd your-meltano-project
   meltano add extractor tap-wordpress
   ```

2. **Configure the tap**
   ```bash
   meltano config tap-wordpress set base_url "https://your-wordpress-site.com"
   meltano config tap-wordpress set per_page 50
   ```

3. **Test the connection**
   ```bash
   meltano invoke tap-wordpress --discover
   ```

4. **Run data extraction**
   ```bash
   meltano run tap-wordpress target-jsonl
   ```

### Example Meltano Configuration

```yaml
# meltano.yml
plugins:
  extractors:
  - name: tap-wordpress
    variant: meltanolabs
    pip_url: tap-wordpress
    config:
      base_url: https://wordpress.org
      per_page: 50
    select:
    - posts.*
    - pages.*
    - categories.*
```

## WordPress Compatibility

This tap works with:
- ✅ **WordPress 4.7+** (when REST API was added to core)
- ✅ **WordPress.com** hosted sites
- ✅ **Self-hosted WordPress** installations
- ✅ **WordPress Multisite** networks
- ✅ **Headless WordPress** setups

## Development

### Prerequisites
- Python 3.8+
- [Poetry](https://python-poetry.org/) for dependency management

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/your-org/tap-wordpress.git
cd tap-wordpress

# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=tap_wordpress --cov-report=term-missing

# Run specific test file
poetry run pytest tests/test_streams.py -v

# Run tests against live WordPress.org API
poetry run pytest tests/test_integration.py -v
```

### Code Quality

```bash
# Format code with Black
poetry run black tap_wordpress tests

# Lint with flake8
poetry run flake8 tap_wordpress tests

# Type checking with mypy
poetry run mypy tap_wordpress

# Run all quality checks
poetry run pre-commit run --all-files
```

### Testing Against Live APIs

The test suite includes integration tests that run against live WordPress APIs:

```bash
# Test against WordPress.org (public API)
poetry run python -m tap_wordpress.tap --config config.json.example --discover

# Test data extraction
poetry run python -m tap_wordpress.tap --config config.json.example --catalog catalog.json
```

## Troubleshooting

### Common Issues

1. **403 Forbidden Error**
   - Check if the WordPress site has REST API enabled
   - Verify the base_url is correct
   - Some WordPress sites may restrict public API access

2. **Rate Limiting**
   - Reduce `per_page` setting
   - Increase `timeout` setting
   - The tap includes automatic retry logic

3. **SSL Certificate Issues**
   - Ensure the WordPress site has a valid SSL certificate
   - For development, you may need to handle self-signed certificates

### Getting Help

- 📖 **Documentation**: [Singer.io](https://www.singer.io/)
- 🛠️ **Meltano SDK**: [SDK Documentation](https://sdk.meltano.com/)
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-org/tap-wordpress/issues)
- 💬 **Community**: [Meltano Slack](https://meltano.com/slack)

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `poetry run pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with the [Meltano Singer SDK](https://sdk.meltano.com/)
- Inspired by the WordPress REST API and the Singer ecosystem
- Thanks to all contributors and the Meltano community
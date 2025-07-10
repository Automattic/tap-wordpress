# Quick Start Guide

This guide will help you get started with `tap-wordpress` quickly.

## Installation

Install the tap using pipx (recommended) or pip:

```bash
pipx install tap-wordpress
# or
pip install tap-wordpress
```

## Basic Usage

### 1. Create a Configuration File

Create a `config.json` file with your WordPress site URL:

```json
{
  "base_url": "https://your-wordpress-site.com"
}
```

For custom settings:

```json
{
  "base_url": "https://your-wordpress-site.com",
  "per_page": 50,
  "start_date": "2023-01-01T00:00:00Z"
}
```

### 2. Discover Available Streams

Run the discovery command to see what data is available:

```bash
tap-wordpress --config config.json --discover
```

This will output a catalog of all available streams and their schemas.

### 3. Generate a Catalog File

Save the discovery output to use for data extraction:

```bash
tap-wordpress --config config.json --discover > catalog.json
```

### 4. Extract Data

Run the tap to extract data:

```bash
tap-wordpress --config config.json --catalog catalog.json
```

The data will be output in Singer format to stdout.

## Example: Extract WordPress.org Data

Here's a complete example using the public WordPress.org API:

```bash
# 1. Create config for WordPress.org
echo '{"base_url": "https://wordpress.org", "per_page": 10}' > config.json

# 2. Discover streams
tap-wordpress --config config.json --discover > catalog.json

# 3. Extract categories data (modify catalog.json to select only categories)
tap-wordpress --config config.json --catalog catalog.json
```

## Using with Meltano

### 1. Add to Meltano Project

```bash
meltano add extractor tap-wordpress
```

### 2. Configure

```bash
meltano config tap-wordpress set base_url "https://your-wordpress-site.com"
meltano config tap-wordpress set per_page 50
```

### 3. Test

```bash
meltano invoke tap-wordpress --discover
```

### 4. Run

```bash
meltano run tap-wordpress target-jsonl
```

## Common Configuration Options

| Setting | Description | Example |
|---------|-------------|---------|
| `base_url` | WordPress site URL (required) | `"https://example.com"` |
| `per_page` | Records per page (default: 100) | `50` |
| `start_date` | Start date for incremental sync | `"2023-01-01T00:00:00Z"` |
| `timeout` | Request timeout in seconds | `30` |

## Available Streams

- `posts` - Blog posts (incremental)
- `pages` - WordPress pages (incremental)
- `comments` - Comments (incremental)
- `media` - Media library items (incremental)
- `users` - User accounts (full table)
- `categories` - Post categories (full table)
- `tags` - Post tags (full table)

## Troubleshooting

### 403 Forbidden Error

- Ensure the WordPress REST API is enabled
- Verify the base_url is correct
- Some WordPress sites may restrict public API access

### No Data Returned

- Check if the WordPress site has content
- Verify the base_url is correct
- Try reducing `per_page` setting

### Rate Limiting

- Reduce `per_page` to make smaller requests
- Increase `timeout` setting
- The tap includes automatic retry logic

## Next Steps

- See the [README](README.md) for detailed documentation
- Check out [WordPress REST API documentation](https://developer.wordpress.org/rest-api/)
- Join the [Meltano community](https://meltano.com/slack) for support
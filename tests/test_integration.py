"""Integration tests for tap-wordpress."""

import pytest
from unittest.mock import Mock, patch

from tap_wordpress.tap import TapWordPress


class TestIntegration:
    """Integration tests for the WordPress tap."""

    @pytest.fixture
    def tap_config(self):
        """Sample tap configuration."""
        return {
            "base_url": "https://techcrunch.com",
            "per_page": 5,
            "timeout": 30,
        }

    def test_tap_initialization(self, tap_config):
        """Test tap initialization."""
        tap = TapWordPress(config=tap_config)
        assert tap.name == "tap-wordpress"
        assert tap.config["base_url"] == "https://techcrunch.com"
        assert tap.config["per_page"] == 5

    def test_discover_streams(self, tap_config):
        """Test stream discovery."""
        tap = TapWordPress(config=tap_config)
        streams = tap.discover_streams()
        
        assert len(streams) == 7
        stream_names = [stream.name for stream in streams]
        expected_streams = [
            "posts", "pages", "users", "categories", 
            "tags", "comments", "media"
        ]
        for expected_stream in expected_streams:
            assert expected_stream in stream_names

    def test_stream_schemas(self, tap_config):
        """Test that all streams have valid schemas."""
        tap = TapWordPress(config=tap_config)
        streams = tap.discover_streams()
        
        for stream in streams:
            schema = stream.schema
            assert isinstance(schema, dict)
            assert "properties" in schema
            assert isinstance(schema["properties"], dict)
            assert len(schema["properties"]) > 0

    def test_stream_primary_keys(self, tap_config):
        """Test that all streams have primary keys."""
        tap = TapWordPress(config=tap_config)
        streams = tap.discover_streams()
        
        for stream in streams:
            assert stream.primary_keys is not None
            assert len(stream.primary_keys) > 0
            assert "id" in stream.primary_keys

    def test_incremental_streams(self, tap_config):
        """Test incremental stream configuration."""
        tap = TapWordPress(config=tap_config)
        streams = tap.discover_streams()
        
        incremental_streams = [
            stream for stream in streams 
            if stream.replication_key is not None
        ]
        
        # Posts, pages, comments, and media should be incremental
        incremental_names = [stream.name for stream in incremental_streams]
        expected_incremental = ["posts", "pages", "comments", "media"]
        
        for expected in expected_incremental:
            assert expected in incremental_names

    def test_stream_url_construction(self, tap_config):
        """Test URL construction for streams."""
        tap = TapWordPress(config=tap_config)
        streams = tap.discover_streams()
        
        # Test posts stream URL construction
        posts_stream = next(stream for stream in streams if stream.name == "posts")
        expected_base = "https://techcrunch.com/wp-json/wp/v2/"
        assert posts_stream.url_base == expected_base
        
        # Test URL parameters
        with patch.object(posts_stream, 'get_starting_timestamp', return_value=None):
            params = posts_stream.get_url_params(context=None, next_page_token=None)
            assert params["per_page"] == 5

    def test_config_validation(self):
        """Test configuration validation."""
        # Test with missing base_url
        from singer_sdk.exceptions import ConfigValidationError
        with pytest.raises(ConfigValidationError, match="base_url.*required"):
            tap = TapWordPress(config={})

    def test_authentication_config(self, tap_config):
        """Test authentication configuration."""
        # Test with username/password
        auth_config = tap_config.copy()
        auth_config.update({
            "username": "testuser",
            "password": "testpass"
        })
        
        tap = TapWordPress(config=auth_config)
        streams = tap.discover_streams()
        posts_stream = next(stream for stream in streams if stream.name == "posts")
        
        assert posts_stream.config["username"] == "testuser"
        assert posts_stream.config["password"] == "testpass"

    def test_stream_records_jsonpath(self, tap_config):
        """Test that streams have correct JSONPath for records."""
        tap = TapWordPress(config=tap_config)
        streams = tap.discover_streams()
        
        for stream in streams:
            # All WordPress API endpoints return arrays of objects
            assert stream.records_jsonpath == "$[*]"
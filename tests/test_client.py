"""Tests for WordPress client functionality."""

import pytest
from unittest.mock import Mock, patch

from tap_wordpress.client import WordPressStream


class TestWordPressClient:
    """Test WordPress client functionality."""

    @pytest.fixture
    def mock_tap(self):
        """Mock tap instance."""
        tap = Mock()
        tap.config = {
            "base_url": "https://techcrunch.com",
            "per_page": 10,
            "timeout": 30,
        }
        tap.plugin_version = "0.1.0"
        return tap

    @pytest.fixture
    def stream(self, mock_tap):
        """Create a test stream instance."""

        class TestStream(WordPressStream):
            name = "test"
            path = "test"
            primary_keys = ["id"]
            records_jsonpath = "$[*]"
            schema = {"properties": {"id": {"type": "integer"}}}

        return TestStream(mock_tap)

    def test_url_base_missing_config(self, mock_tap):
        """Test URL base construction with missing config."""
        mock_tap.config = {}

        class TestStream(WordPressStream):
            name = "test"
            path = "test"
            primary_keys = ["id"]
            records_jsonpath = "$[*]"
            schema = {"properties": {"id": {"type": "integer"}}}

        stream = TestStream(mock_tap)

        with pytest.raises(ValueError, match="base_url is required"):
            _ = stream.url_base

    def test_url_base_various_formats(self, mock_tap):
        """Test URL base construction with various input formats."""
        test_cases = [
            ("https://example.com", "https://example.com/wp-json/wp/v2/"),
            ("https://example.com/", "https://example.com/wp-json/wp/v2/"),
            ("https://example.com/wp-json/", "https://example.com/wp-json/wp/v2/"),
            (
                "https://example.com/wp-json/wp/v2/",
                "https://example.com/wp-json/wp/v2/",
            ),
        ]

        for base_url, expected in test_cases:
            mock_tap.config["base_url"] = base_url

            class TestStream(WordPressStream):
                name = "test"
                path = "test"
                primary_keys = ["id"]
                records_jsonpath = "$[*]"
                schema = {"properties": {"id": {"type": "integer"}}}

            stream = TestStream(mock_tap)
            assert stream.url_base == expected

    def test_get_url_params_with_replication_key(self, mock_tap):
        """Test URL parameters with replication key."""

        class TestStreamWithReplication(WordPressStream):
            name = "test"
            path = "test"
            primary_keys = ["id"]
            replication_key = "modified"
            records_jsonpath = "$[*]"
            schema = {"properties": {"id": {"type": "integer"}}}

        stream = TestStreamWithReplication(mock_tap)

        with patch.object(stream, "get_starting_timestamp") as mock_get_timestamp:
            from datetime import datetime

            mock_timestamp = datetime(2023, 1, 1, 12, 0, 0)
            mock_get_timestamp.return_value = mock_timestamp

            params = stream.get_url_params(context=None, next_page_token=None)
            assert params["per_page"] == 10
            assert params["after"] == "2023-01-01T12:00:00"

    def test_prepare_request_payload(self, stream):
        """Test request payload preparation."""
        payload = stream.prepare_request_payload(context=None, next_page_token=None)
        assert payload is None

    @patch("tap_wordpress.client.extract_jsonpath")
    def test_parse_response_with_jsonpath(self, mock_extract_jsonpath, stream):
        """Test response parsing with JSONPath."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": [{"id": 1}, {"id": 2}]}

        mock_extract_jsonpath.return_value = [{"id": 1}, {"id": 2}]

        records = list(stream.parse_response(mock_response))
        assert len(records) == 2
        assert records[0]["id"] == 1
        assert records[1]["id"] == 2

        # Verify extract_jsonpath was called with correct parameters
        mock_extract_jsonpath.assert_called_once_with(
            stream.records_jsonpath, input=mock_response.json()
        )

    def test_basic_config(self, mock_tap):
        """Test basic configuration."""
        mock_tap.config.update({"base_url": "https://wordpress.org", "per_page": 50})

        class TestStream(WordPressStream):
            name = "test"
            path = "test"
            primary_keys = ["id"]
            records_jsonpath = "$[*]"
            schema = {"properties": {"id": {"type": "integer"}}}

        stream = TestStream(mock_tap)

        # Test that config is accessible
        assert stream.config["base_url"] == "https://wordpress.org"
        assert stream.config["per_page"] == 50

    def test_pagination_logic(self, mock_tap):
        """Test pagination logic."""

        class TestStream(WordPressStream):
            name = "test"
            path = "test"
            primary_keys = ["id"]
            records_jsonpath = "$[*]"
            schema = {"properties": {"id": {"type": "integer"}}}

        stream = TestStream(mock_tap)

        # Test pagination with headers
        mock_response1 = Mock()
        mock_response1.headers = {"X-WP-TotalPages": "3"}

        # First page
        next_token = stream.get_next_page_token(mock_response1, None)
        assert next_token == 2

        # Second page
        next_token = stream.get_next_page_token(mock_response1, 2)
        assert next_token == 3

        # Last page
        next_token = stream.get_next_page_token(mock_response1, 3)
        assert next_token is None

"""Tests for WordPress streams."""

import pytest
from unittest.mock import Mock, patch
import requests

from tap_wordpress.streams import (
    PostsStream,
    PagesStream,
    UsersStream,
    CategoriesStream,
    TagsStream,
    CommentsStream,
    MediaStream,
)


class TestWordPressStreams:
    """Test WordPress stream classes."""

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

    def test_posts_stream_init(self, mock_tap):
        """Test PostsStream initialization."""
        stream = PostsStream(mock_tap)
        assert stream.name == "posts"
        assert stream.path == "posts"
        assert stream.primary_keys == ["id"]
        assert stream.replication_key == "modified"

    def test_pages_stream_init(self, mock_tap):
        """Test PagesStream initialization."""
        stream = PagesStream(mock_tap)
        assert stream.name == "pages"
        assert stream.path == "pages"
        assert stream.primary_keys == ["id"]
        assert stream.replication_key == "modified"

    def test_users_stream_init(self, mock_tap):
        """Test UsersStream initialization."""
        stream = UsersStream(mock_tap)
        assert stream.name == "users"
        assert stream.path == "users"
        assert stream.primary_keys == ["id"]
        assert stream.replication_key is None

    def test_categories_stream_init(self, mock_tap):
        """Test CategoriesStream initialization."""
        stream = CategoriesStream(mock_tap)
        assert stream.name == "categories"
        assert stream.path == "categories"
        assert stream.primary_keys == ["id"]

    def test_tags_stream_init(self, mock_tap):
        """Test TagsStream initialization."""
        stream = TagsStream(mock_tap)
        assert stream.name == "tags"
        assert stream.path == "tags"
        assert stream.primary_keys == ["id"]

    def test_comments_stream_init(self, mock_tap):
        """Test CommentsStream initialization."""
        stream = CommentsStream(mock_tap)
        assert stream.name == "comments"
        assert stream.path == "comments"
        assert stream.primary_keys == ["id"]
        assert stream.replication_key == "date"

    def test_media_stream_init(self, mock_tap):
        """Test MediaStream initialization."""
        stream = MediaStream(mock_tap)
        assert stream.name == "media"
        assert stream.path == "media"
        assert stream.primary_keys == ["id"]
        assert stream.replication_key == "modified"

    def test_url_base_construction(self, mock_tap):
        """Test URL base construction."""
        stream = PostsStream(mock_tap)
        expected_url = "https://techcrunch.com/wp-json/wp/v2/"
        assert stream.url_base == expected_url

    def test_url_base_with_trailing_slash(self, mock_tap):
        """Test URL base construction with trailing slash."""
        mock_tap.config["base_url"] = "https://techcrunch.com/"
        stream = PostsStream(mock_tap)
        expected_url = "https://techcrunch.com/wp-json/wp/v2/"
        assert stream.url_base == expected_url

    def test_url_base_with_wp_json_path(self, mock_tap):
        """Test URL base construction with wp-json path."""
        mock_tap.config["base_url"] = "https://techcrunch.com/wp-json/"
        stream = PostsStream(mock_tap)
        expected_url = "https://techcrunch.com/wp-json/wp/v2/"
        assert stream.url_base == expected_url

    def test_get_url_params(self, mock_tap):
        """Test URL parameter generation."""
        stream = PostsStream(mock_tap)
        with patch.object(stream, 'get_starting_timestamp', return_value=None):
            params = stream.get_url_params(context=None, next_page_token=None)
            assert params["per_page"] == 10
            assert "page" not in params

    def test_get_url_params_with_pagination(self, mock_tap):
        """Test URL parameter generation with pagination."""
        stream = PostsStream(mock_tap)
        with patch.object(stream, 'get_starting_timestamp', return_value=None):
            params = stream.get_url_params(context=None, next_page_token=2)
            assert params["per_page"] == 10
            assert params["page"] == 2

    def test_get_next_page_token(self, mock_tap):
        """Test next page token generation."""
        stream = PostsStream(mock_tap)
        
        # Mock response with pagination headers
        mock_response = Mock()
        mock_response.headers = {"X-WP-TotalPages": "3"}
        
        # First page
        next_token = stream.get_next_page_token(mock_response, None)
        assert next_token == 2
        
        # Second page
        next_token = stream.get_next_page_token(mock_response, 2)
        assert next_token == 3
        
        # Last page
        next_token = stream.get_next_page_token(mock_response, 3)
        assert next_token is None

    def test_get_next_page_token_no_header(self, mock_tap):
        """Test next page token generation without pagination header."""
        stream = PostsStream(mock_tap)
        
        # Mock response without pagination headers
        mock_response = Mock()
        mock_response.headers = {}
        
        next_token = stream.get_next_page_token(mock_response, None)
        assert next_token is None

    def test_http_headers(self, mock_tap):
        """Test HTTP headers."""
        mock_tap.name = "tap-wordpress"
        stream = PostsStream(mock_tap)
        headers = stream.http_headers
        assert "User-Agent" in headers
        assert "tap-wordpress" in headers["User-Agent"]

    @patch('tap_wordpress.client.extract_jsonpath')
    def test_parse_response(self, mock_extract_jsonpath, mock_tap):
        """Test response parsing."""
        stream = PostsStream(mock_tap)
        
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = [
            {"id": 1, "title": {"rendered": "Test Post"}},
            {"id": 2, "title": {"rendered": "Another Post"}},
        ]
        
        # Mock extract_jsonpath to return the response data
        mock_extract_jsonpath.return_value = mock_response.json()
        
        records = list(stream.parse_response(mock_response))
        assert len(records) == 2
        assert records[0]["id"] == 1
        assert records[1]["id"] == 2
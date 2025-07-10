"""WordPress tap class."""

from __future__ import annotations

from typing import List

from singer_sdk import Tap
from singer_sdk import typing as th

from tap_wordpress.streams import (
    PostsStream,
    PagesStream,
    UsersStream,
    CategoriesStream,
    TagsStream,
    CommentsStream,
    MediaStream,
)

STREAM_TYPES = [
    PostsStream,
    PagesStream,
    UsersStream,
    CategoriesStream,
    TagsStream,
    CommentsStream,
    MediaStream,
]


class TapWordPress(Tap):
    """WordPress tap class."""

    name = "tap-wordpress"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "base_url",
            th.StringType,
            required=True,
            description="WordPress site base URL (e.g., https://example.com)",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            required=False,
            description="Start date for incremental sync",
        ),
        th.Property(
            "per_page",
            th.IntegerType,
            required=False,
            default=100,
            description="Number of records to fetch per page",
        ),
        th.Property(
            "timeout",
            th.IntegerType,
            required=False,
            default=30,
            description="Request timeout in seconds",
        ),
    ).to_dict()

    def discover_streams(self) -> List:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapWordPress.cli()

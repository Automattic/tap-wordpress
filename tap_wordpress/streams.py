"""Stream type classes for tap-wordpress."""

from __future__ import annotations

from typing import Any, Dict, Optional

from singer_sdk import typing as th

from tap_wordpress.client import WordPressStream


class PostsStream(WordPressStream):
    """Define custom stream for WordPress posts."""

    name = "posts"
    path = "posts"
    primary_keys = ["id"]
    replication_key = "modified"
    records_jsonpath = "$[*]"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("date", th.DateTimeType),
        th.Property("date_gmt", th.DateTimeType),
        th.Property("guid", th.ObjectType(
            th.Property("rendered", th.StringType),
            th.Property("raw", th.StringType),
        )),
        th.Property("modified", th.DateTimeType),
        th.Property("modified_gmt", th.DateTimeType),
        th.Property("slug", th.StringType),
        th.Property("status", th.StringType),
        th.Property("type", th.StringType),
        th.Property("link", th.StringType),
        th.Property("title", th.ObjectType(
            th.Property("rendered", th.StringType),
            th.Property("raw", th.StringType),
        )),
        th.Property("content", th.ObjectType(
            th.Property("rendered", th.StringType),
            th.Property("raw", th.StringType),
            th.Property("protected", th.BooleanType),
        )),
        th.Property("excerpt", th.ObjectType(
            th.Property("rendered", th.StringType),
            th.Property("raw", th.StringType),
            th.Property("protected", th.BooleanType),
        )),
        th.Property("author", th.IntegerType),
        th.Property("featured_media", th.IntegerType),
        th.Property("comment_status", th.StringType),
        th.Property("ping_status", th.StringType),
        th.Property("sticky", th.BooleanType),
        th.Property("template", th.StringType),
        th.Property("format", th.StringType),
        th.Property("meta", th.ObjectType()),
        th.Property("categories", th.ArrayType(th.IntegerType)),
        th.Property("tags", th.ArrayType(th.IntegerType)),
    ).to_dict()


class PagesStream(WordPressStream):
    """Define custom stream for WordPress pages."""

    name = "pages"
    path = "pages"
    primary_keys = ["id"]
    replication_key = "modified"
    records_jsonpath = "$[*]"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("date", th.DateTimeType),
        th.Property("date_gmt", th.DateTimeType),
        th.Property("guid", th.ObjectType(
            th.Property("rendered", th.StringType),
            th.Property("raw", th.StringType),
        )),
        th.Property("modified", th.DateTimeType),
        th.Property("modified_gmt", th.DateTimeType),
        th.Property("slug", th.StringType),
        th.Property("status", th.StringType),
        th.Property("type", th.StringType),
        th.Property("link", th.StringType),
        th.Property("title", th.ObjectType(
            th.Property("rendered", th.StringType),
            th.Property("raw", th.StringType),
        )),
        th.Property("content", th.ObjectType(
            th.Property("rendered", th.StringType),
            th.Property("raw", th.StringType),
            th.Property("protected", th.BooleanType),
        )),
        th.Property("excerpt", th.ObjectType(
            th.Property("rendered", th.StringType),
            th.Property("raw", th.StringType),
            th.Property("protected", th.BooleanType),
        )),
        th.Property("author", th.IntegerType),
        th.Property("featured_media", th.IntegerType),
        th.Property("parent", th.IntegerType),
        th.Property("menu_order", th.IntegerType),
        th.Property("comment_status", th.StringType),
        th.Property("ping_status", th.StringType),
        th.Property("template", th.StringType),
        th.Property("meta", th.ObjectType()),
    ).to_dict()


class UsersStream(WordPressStream):
    """Define custom stream for WordPress users."""

    name = "users"
    path = "users"
    primary_keys = ["id"]
    records_jsonpath = "$[*]"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("username", th.StringType),
        th.Property("name", th.StringType),
        th.Property("first_name", th.StringType),
        th.Property("last_name", th.StringType),
        th.Property("email", th.StringType),
        th.Property("url", th.StringType),
        th.Property("description", th.StringType),
        th.Property("link", th.StringType),
        th.Property("locale", th.StringType),
        th.Property("nickname", th.StringType),
        th.Property("slug", th.StringType),
        th.Property("registered_date", th.DateTimeType),
        th.Property("roles", th.ArrayType(th.StringType)),
        th.Property("capabilities", th.ObjectType()),
        th.Property("extra_capabilities", th.ObjectType()),
        th.Property("avatar_urls", th.ObjectType()),
        th.Property("meta", th.ObjectType()),
    ).to_dict()


class CategoriesStream(WordPressStream):
    """Define custom stream for WordPress categories."""

    name = "categories"
    path = "categories"
    primary_keys = ["id"]
    records_jsonpath = "$[*]"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("count", th.IntegerType),
        th.Property("description", th.StringType),
        th.Property("link", th.StringType),
        th.Property("name", th.StringType),
        th.Property("slug", th.StringType),
        th.Property("taxonomy", th.StringType),
        th.Property("parent", th.IntegerType),
        th.Property("meta", th.ObjectType()),
    ).to_dict()


class TagsStream(WordPressStream):
    """Define custom stream for WordPress tags."""

    name = "tags"
    path = "tags"
    primary_keys = ["id"]
    records_jsonpath = "$[*]"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("count", th.IntegerType),
        th.Property("description", th.StringType),
        th.Property("link", th.StringType),
        th.Property("name", th.StringType),
        th.Property("slug", th.StringType),
        th.Property("taxonomy", th.StringType),
        th.Property("meta", th.ObjectType()),
    ).to_dict()


class CommentsStream(WordPressStream):
    """Define custom stream for WordPress comments."""

    name = "comments"
    path = "comments"
    primary_keys = ["id"]
    replication_key = "date"
    records_jsonpath = "$[*]"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("post", th.IntegerType),
        th.Property("parent", th.IntegerType),
        th.Property("author", th.IntegerType),
        th.Property("author_name", th.StringType),
        th.Property("author_url", th.StringType),
        th.Property("author_email", th.StringType),
        th.Property("author_ip", th.StringType),
        th.Property("author_user_agent", th.StringType),
        th.Property("date", th.DateTimeType),
        th.Property("date_gmt", th.DateTimeType),
        th.Property("content", th.ObjectType(
            th.Property("rendered", th.StringType),
            th.Property("raw", th.StringType),
        )),
        th.Property("link", th.StringType),
        th.Property("status", th.StringType),
        th.Property("type", th.StringType),
        th.Property("author_avatar_urls", th.ObjectType()),
        th.Property("meta", th.ObjectType()),
    ).to_dict()


class MediaStream(WordPressStream):
    """Define custom stream for WordPress media."""

    name = "media"
    path = "media"
    primary_keys = ["id"]
    replication_key = "modified"
    records_jsonpath = "$[*]"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("date", th.DateTimeType),
        th.Property("date_gmt", th.DateTimeType),
        th.Property("guid", th.ObjectType(
            th.Property("rendered", th.StringType),
            th.Property("raw", th.StringType),
        )),
        th.Property("modified", th.DateTimeType),
        th.Property("modified_gmt", th.DateTimeType),
        th.Property("slug", th.StringType),
        th.Property("status", th.StringType),
        th.Property("type", th.StringType),
        th.Property("link", th.StringType),
        th.Property("title", th.ObjectType(
            th.Property("rendered", th.StringType),
            th.Property("raw", th.StringType),
        )),
        th.Property("author", th.IntegerType),
        th.Property("comment_status", th.StringType),
        th.Property("ping_status", th.StringType),
        th.Property("template", th.StringType),
        th.Property("meta", th.ObjectType()),
        th.Property("description", th.ObjectType(
            th.Property("rendered", th.StringType),
            th.Property("raw", th.StringType),
        )),
        th.Property("caption", th.ObjectType(
            th.Property("rendered", th.StringType),
            th.Property("raw", th.StringType),
        )),
        th.Property("alt_text", th.StringType),
        th.Property("media_type", th.StringType),
        th.Property("mime_type", th.StringType),
        th.Property("media_details", th.ObjectType()),
        th.Property("post", th.IntegerType),
        th.Property("source_url", th.StringType),
    ).to_dict()
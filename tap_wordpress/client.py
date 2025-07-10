"""WordPress REST API client handling."""

from __future__ import annotations

import requests
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from typing import Any, Dict, Optional, Iterable


class WordPressStream(RESTStream):
    """WordPress stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        base_url = self.config.get("base_url")
        if not base_url:
            raise ValueError("base_url is required in config")

        # Ensure base_url is a string
        if not isinstance(base_url, str):
            base_url = str(base_url)

        # Ensure base_url ends with /wp-json/wp/v2/
        if not base_url.endswith("/"):
            base_url += "/"

        if "/wp-json/wp/v2/" not in base_url:
            if not base_url.endswith("wp-json/"):
                base_url += "wp-json/"
            if not base_url.endswith("wp/v2/"):
                base_url += "wp/v2/"

        return base_url

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if hasattr(self, "_tap") and hasattr(self._tap, "plugin_version"):
            headers["User-Agent"] = f"{self.tap_name}/{self._tap.plugin_version}"
        else:
            headers["User-Agent"] = f"{self.tap_name}/0.1.0"
        return headers

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}

        # Pagination
        if next_page_token:
            params["page"] = next_page_token

        # Per page limit
        params["per_page"] = self.config.get("per_page", 100)

        # Date filtering for incremental sync
        if self.replication_key:
            start_date = self.get_starting_timestamp(context)
            if start_date:
                params["after"] = start_date.isoformat()

        return params

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        # WordPress API uses X-WP-TotalPages header for pagination
        total_pages_str = response.headers.get("X-WP-TotalPages")
        if not total_pages_str:
            return None

        current_page: int = previous_token or 1
        if not isinstance(current_page, int):
            current_page = int(current_page)

        total_pages = int(total_pages_str)

        if current_page < total_pages:
            return current_page + 1

        return None

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the REST API request."""
        return None

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records."""
        try:
            json_data = response.json()
            yield from extract_jsonpath(self.records_jsonpath, input=json_data)
        except ValueError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            self.logger.error(f"Response content: {response.text[:500]}")
            raise

    def request_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Request records from the REST API."""
        next_page_token: Any = None

        while True:
            try:
                prepared_request = self.prepare_request(
                    context, next_page_token=next_page_token
                )

                # No authentication needed for public WordPress REST API endpoints

                resp = self._request(prepared_request, context)

                # Check for successful response
                if resp.status_code >= 400:
                    self.logger.error(
                        f"HTTP {resp.status_code} error for {self.name} stream: "
                        f"{resp.text}"
                    )
                    if resp.status_code == 401:
                        raise Exception(
                            "Authentication failed. Check username/password or API key."
                        )
                    elif resp.status_code == 403:
                        raise Exception("Access forbidden. Check permissions.")
                    elif resp.status_code == 404:
                        self.logger.warning(
                            f"Endpoint not found: {prepared_request.url}"
                        )
                        break
                    else:
                        resp.raise_for_status()

                for row in self.parse_response(resp):
                    yield row

                previous_token = next_page_token
                next_page_token = self.get_next_page_token(
                    response=resp, previous_token=previous_token
                )

                if next_page_token is None:
                    break

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request failed for {self.name} stream: {e}")
                raise Exception(f"Failed to fetch data from WordPress API: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error in {self.name} stream: {e}")
                raise

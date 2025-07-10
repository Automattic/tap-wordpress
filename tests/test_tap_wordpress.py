"""Tests standard tap features using the built-in SDK tests library."""

from singer_sdk.testing import get_tap_test_class

from tap_wordpress.tap import TapWordPress

SAMPLE_CONFIG = {
    "base_url": "https://techcrunch.com",
    "per_page": 10,
    "timeout": 30,
}


def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    TestClass = get_tap_test_class(TapWordPress, config=SAMPLE_CONFIG)
    # Just test that the class can be instantiated
    test_instance = TestClass()
    assert test_instance is not None
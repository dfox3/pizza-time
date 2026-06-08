"""Test cases for the core module."""

from dfizza.core import greet


def test_greet_returns_message() -> None:
    """It returns a greeting containing the name."""
    assert greet("world") == "Hello, world!"

"""
Unit tests for StringUtils module.
"""
import pytest
from lib.StringUtils import normalize, substring


class TestNormalize:
    """Test cases for the normalize function."""

    def test_normalize_simple_word(self):
        """Test normalization of a simple word."""
        assert normalize("hello") == "hello"
        assert normalize("world") == "world"

    def test_normalize_removes_quotes(self):
        """Test that normalize removes various quote characters."""
        assert normalize('"hello"') == "hello"
        assert normalize("'hello'") == "hello"
        # Note: curly quotes are not removed by normalize function
        assert normalize('hello') == "hello"

    def test_normalize_removes_parentheses(self):
        """Test that normalize removes parentheses."""
        assert normalize("(hello)") == "hello"
        assert normalize("hello)") == "hello"
        assert normalize("(hello") == "hello"

    def test_normalize_removes_underscores(self):
        """Test that normalize removes underscores."""
        assert normalize("hello_world") == "helloworld"
        assert normalize("_hello_") == "hello"

    def test_normalize_removes_backticks(self):
        """Test that normalize removes backticks."""
        assert normalize("`hello`") == "hello"
        assert normalize("hello`") == "hello"

    def test_normalize_removes_newlines(self):
        """Test that normalize removes newline characters."""
        assert normalize("hello\nworld") == "helloworld"
        assert normalize("hello\n") == "hello"

    def test_normalize_mixed_special_chars(self):
        """Test normalization with multiple special characters."""
        assert normalize('"(hello_world)"') == "helloworld"
        assert normalize("'test'\n") == "test"

    def test_normalize_empty_string(self):
        """Test normalization of empty string."""
        assert normalize("") == ""

    def test_normalize_only_special_chars(self):
        """Test normalization when only special characters are present."""
        assert normalize('"""') == ""
        assert normalize("()_") == ""


class TestSubstring:
    """Test cases for the substring function."""

    def test_substring_with_period(self):
        """Test substring split by period."""
        assert substring("Hello. World", ".") == "Hello"
        assert substring("First.Second.Third", ".") == "First"

    def test_substring_with_semicolon(self):
        """Test substring split by semicolon."""
        assert substring("Hello; World", ";") == "Hello"
        assert substring("First;Second;Third", ";") == "First"

    def test_substring_with_exclamation(self):
        """Test substring split by exclamation mark."""
        assert substring("Hello! World", "!") == "Hello"
        assert substring("First!Second!Third", "!") == "First"

    def test_substring_with_multiple_delimiters(self):
        """Test substring with multiple delimiter characters."""
        assert substring("Hello. World! Test", ".!") == "Hello"
        assert substring("Hello! World. Test", ".!") == "Hello"
        assert substring("Hello; World. Test!", ";.!") == "Hello"

    def test_substring_no_delimiter_present(self):
        """Test substring when no delimiter is present."""
        assert substring("Hello World", ".") == "Hello World"
        assert substring("Test", ";.!") == "Test"

    def test_substring_delimiter_at_start(self):
        """Test substring with delimiter at the start."""
        assert substring(".Hello", ".") == ""
        assert substring("!Hello", "!") == ""

    def test_substring_delimiter_at_end(self):
        """Test substring with delimiter at the end."""
        assert substring("Hello.", ".") == "Hello"
        assert substring("Hello!", "!") == "Hello"

    def test_substring_empty_string(self):
        """Test substring with empty string."""
        assert substring("", ".") == ""

    def test_substring_only_delimiter(self):
        """Test substring with only delimiter."""
        assert substring(".", ".") == ""
        assert substring("!;.", "!;.") == ""

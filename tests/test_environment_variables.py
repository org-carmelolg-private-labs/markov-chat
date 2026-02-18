"""
Unit tests for EnvironmentVariables module.
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from lib.EnvironmentVariables import EnvironmentVariables


@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset the singleton instance before each test."""
    EnvironmentVariables._instance = None
    yield
    EnvironmentVariables._instance = None


class TestEnvironmentVariables:
    """Test cases for the EnvironmentVariables class."""

    def test_singleton_pattern(self):
        """Test that EnvironmentVariables implements singleton pattern."""
        instance1 = EnvironmentVariables()
        instance2 = EnvironmentVariables()
        assert instance1 is instance2

    @patch.dict(os.environ, {"MAX_WORDS": "100"}, clear=False)
    def test_get_max_words_from_env(self):
        """Test get_max_words returns value from environment variable."""
        env = EnvironmentVariables()
        assert env.get_max_words() == 100

    @patch.dict(os.environ, {"MAX_WORDS": ""}, clear=False)
    @patch('os.getenv')
    def test_get_max_words_default(self, mock_getenv):
        """Test get_max_words returns default value when not set."""
        mock_getenv.return_value = None
        env = EnvironmentVariables()
        assert env.get_max_words() == 50
        assert env.get_max_words(default=75) == 75

    @patch.dict(os.environ, {"MAX_WORDS": "200"}, clear=False)
    def test_get_max_words_custom_default(self):
        """Test get_max_words with custom default when env is set."""
        env = EnvironmentVariables()
        # Should use env value, not default
        assert env.get_max_words(default=75) == 200

    @patch.dict(os.environ, {"INPUT_FILENAME": "file1.txt,file2.txt,file3.txt"}, clear=False)
    def test_get_input_filename_multiple(self):
        """Test get_input_filename splits comma-separated values."""
        env = EnvironmentVariables()
        filenames = env.get_input_filename()
        assert filenames == ["file1.txt", "file2.txt", "file3.txt"]

    @patch.dict(os.environ, {"INPUT_FILENAME": "single.txt"}, clear=False)
    def test_get_input_filename_single(self):
        """Test get_input_filename with single file."""
        env = EnvironmentVariables()
        filenames = env.get_input_filename()
        assert filenames == ["single.txt"]

    @patch('os.getenv')
    def test_get_input_filename_not_set(self, mock_getenv):
        """Test get_input_filename returns empty list when not set."""
        def getenv_side_effect(key, default=None):
            if key == "INPUT_FILENAME":
                return default
            return None
        mock_getenv.side_effect = getenv_side_effect
        env = EnvironmentVariables()
        filenames = env.get_input_filename()
        assert filenames == []

    @patch('os.getenv')
    def test_get_input_filename_with_default(self, mock_getenv):
        """Test get_input_filename with default value."""
        def getenv_side_effect(key, default=None):
            if key == "INPUT_FILENAME":
                return default
            return None
        mock_getenv.side_effect = getenv_side_effect
        env = EnvironmentVariables()
        filenames = env.get_input_filename(default="default.txt")
        assert filenames == ["default.txt"]

    @patch.dict(os.environ, {"INPUT_FILENAME": "file1.txt,file2.txt"}, clear=False)
    def test_get_input_filename_ignores_default_when_set(self):
        """Test get_input_filename ignores default when env is set."""
        env = EnvironmentVariables()
        filenames = env.get_input_filename(default="default.txt")
        assert filenames == ["file1.txt", "file2.txt"]

    @patch.dict(os.environ, {"TEMPERATURE": "0.7"}, clear=False)
    def test_get_temperature_from_env(self):
        """Test get_temperature returns value from environment variable."""
        env = EnvironmentVariables()
        assert env.get_temperature() == 0.7

    @patch('os.getenv')
    def test_get_temperature_default(self, mock_getenv):
        """Test get_temperature returns default value when not set."""
        mock_getenv.return_value = None
        env = EnvironmentVariables()
        assert env.get_temperature() == 1.0
        assert env.get_temperature(default=0.5) == 0.5

    @patch.dict(os.environ, {"TEMPERATURE": "0.3"}, clear=False)
    def test_get_temperature_custom_default(self):
        """Test get_temperature with custom default when env is set."""
        env = EnvironmentVariables()
        # Should use env value, not default
        assert env.get_temperature(default=0.8) == 0.3

    @patch.dict(os.environ, {"TEMPERATURE": "1.5"}, clear=False)
    def test_get_temperature_greater_than_one(self):
        """Test get_temperature with value greater than 1.0."""
        env = EnvironmentVariables()
        assert env.get_temperature() == 1.5

    @patch.dict(os.environ, {"TEMPERATURE": "0.0"}, clear=False)
    def test_get_temperature_zero(self):
        """Test get_temperature with zero value."""
        env = EnvironmentVariables()
        assert env.get_temperature() == 0.0

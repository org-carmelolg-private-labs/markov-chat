"""
Unit tests for MarkovGenerator module.
"""
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from collections import defaultdict

from lib import MarkovGenerator
from lib.MarkovGenerator import (
    run, _file_path, _read_words, _build_possibles,
    _pick_start_key, _generate, _creative, _deterministic
)


class TestFilePath:
    """Test cases for the _file_path function."""

    @patch('lib.MarkovGenerator.env.get_input_filename')
    def test_file_path_single_file(self, mock_get_input_filename):
        """Test _file_path with a single filename."""
        mock_get_input_filename.return_value = ['test.txt']
        paths = _file_path()
        assert len(paths) == 1
        assert paths[0].name == 'test.txt'
        assert 'static' in str(paths[0])

    @patch('lib.MarkovGenerator.env.get_input_filename')
    def test_file_path_multiple_files(self, mock_get_input_filename):
        """Test _file_path with multiple filenames."""
        mock_get_input_filename.return_value = ['file1.txt', 'file2.txt', 'file3.txt']
        paths = _file_path()
        assert len(paths) == 3
        assert paths[0].name == 'file1.txt'
        assert paths[1].name == 'file2.txt'
        assert paths[2].name == 'file3.txt'

    @patch('lib.MarkovGenerator.env.get_input_filename')
    def test_file_path_empty_list(self, mock_get_input_filename):
        """Test _file_path with empty filename list."""
        mock_get_input_filename.return_value = []
        paths = _file_path()
        assert len(paths) == 0


class TestReadWords:
    """Test cases for the _read_words function."""

    def test_read_words_single_file(self):
        """Test _read_words with a single file."""
        test_file = Path(__file__).parent / 'test_data' / 'test_input.txt'
        words = list(_read_words([test_file]))
        assert len(words) > 0
        assert 'The' in words
        assert 'quick' in words

    def test_read_words_multiple_files(self):
        """Test _read_words with multiple files."""
        test_file1 = Path(__file__).parent / 'test_data' / 'test_input.txt'
        test_file2 = Path(__file__).parent / 'test_data' / 'test_input2.txt'
        words = list(_read_words([test_file1, test_file2]))
        assert len(words) > 0
        # Words from both files should be present
        assert 'The' in words
        assert 'Hello' in words

    def test_read_words_normalizes_words(self):
        """Test that _read_words normalizes words."""
        test_file = Path(__file__).parent / 'test_data' / 'test_input.txt'
        words = list(_read_words([test_file]))
        # Check that punctuation is removed (normalize should have been called)
        # The original file has "dog." which should become "dog"
        assert 'dog' in words


class TestBuildPossibles:
    """Test cases for the _build_possibles function."""

    @patch('lib.MarkovGenerator._file_path')
    @patch('lib.MarkovGenerator.env.get_input_filename')
    def test_build_possibles_creates_dict(self, mock_get_input_filename, mock_file_path):
        """Test that _build_possibles creates a dictionary."""
        test_file = Path(__file__).parent / 'test_data' / 'test_input.txt'
        mock_file_path.return_value = [test_file]
        mock_get_input_filename.return_value = ['test_input.txt']
        
        possibles = _build_possibles(prefix_len=2)
        assert isinstance(possibles, dict)
        assert len(possibles) > 0

    @patch('lib.MarkovGenerator._file_path')
    @patch('lib.MarkovGenerator.env.get_input_filename')
    def test_build_possibles_with_prefix_len_2(self, mock_get_input_filename, mock_file_path):
        """Test _build_possibles with prefix length 2."""
        test_file = Path(__file__).parent / 'test_data' / 'test_input.txt'
        mock_file_path.return_value = [test_file]
        mock_get_input_filename.return_value = ['test_input.txt']
        
        possibles = _build_possibles(prefix_len=2)
        # Each key should be a tuple of length 2
        for key in possibles.keys():
            assert isinstance(key, tuple)
            assert len(key) == 2

    @patch('lib.MarkovGenerator._file_path')
    @patch('lib.MarkovGenerator.env.get_input_filename')
    def test_build_possibles_with_prefix_len_3(self, mock_get_input_filename, mock_file_path):
        """Test _build_possibles with prefix length 3."""
        test_file = Path(__file__).parent / 'test_data' / 'test_input.txt'
        mock_file_path.return_value = [test_file]
        mock_get_input_filename.return_value = ['test_input.txt']
        
        possibles = _build_possibles(prefix_len=3)
        # Each key should be a tuple of length 3
        for key in possibles.keys():
            assert isinstance(key, tuple)
            assert len(key) == 3

    @patch('lib.MarkovGenerator._file_path')
    @patch('lib.MarkovGenerator.env.get_input_filename')
    def test_build_possibles_file_not_found(self, mock_get_input_filename, mock_file_path):
        """Test _build_possibles raises FileNotFoundError for non-existent file."""
        non_existent_file = Path('/tmp/non_existent_file_12345.txt')
        mock_file_path.return_value = [non_existent_file]
        mock_get_input_filename.return_value = ['non_existent.txt']
        
        with pytest.raises(FileNotFoundError):
            _build_possibles(prefix_len=2)

    @patch('lib.MarkovGenerator._file_path')
    @patch('lib.MarkovGenerator.env.get_input_filename')
    def test_build_possibles_empty_file_list(self, mock_get_input_filename, mock_file_path):
        """Test _build_possibles raises FileNotFoundError for empty file list."""
        mock_file_path.return_value = []
        mock_get_input_filename.return_value = []
        
        with pytest.raises(FileNotFoundError):
            _build_possibles(prefix_len=2)


class TestPickStartKey:
    """Test cases for the _pick_start_key function."""

    def test_pick_start_key_prefers_uppercase(self):
        """Test that _pick_start_key prefers keys starting with uppercase."""
        possibles = {
            ('The', 'quick'): ['brown'],
            ('the', 'lazy'): ['dog'],
            ('and', 'slept'): ['all'],
        }
        # Should prefer 'The' (uppercase) over others
        start_key = _pick_start_key(possibles)
        assert start_key[0][0].isupper()

    def test_pick_start_key_fallback_to_any_non_empty(self):
        """Test that _pick_start_key falls back to non-empty first element."""
        possibles = {
            ('the', 'quick'): ['brown'],
            ('and', 'lazy'): ['dog'],
        }
        start_key = _pick_start_key(possibles)
        assert start_key in possibles.keys()
        assert start_key[0] != ''

    def test_pick_start_key_with_empty_elements(self):
        """Test _pick_start_key with keys containing empty strings."""
        possibles = {
            ('', ''): ['The'],
            ('', 'quick'): ['brown'],
            ('The', 'quick'): ['brown'],
        }
        start_key = _pick_start_key(possibles)
        assert start_key in possibles.keys()

    def test_pick_start_key_all_empty_first_elements(self):
        """Test _pick_start_key when all keys have empty first elements."""
        possibles = {
            ('', ''): ['word1'],
            ('', 'a'): ['word2'],
        }
        start_key = _pick_start_key(possibles)
        assert start_key in possibles.keys()
        # Should still work even though all first elements are empty

    def test_pick_start_key_returns_valid_key(self):
        """Test that _pick_start_key returns a valid key from possibles."""
        possibles = {
            ('A', 'B'): ['C'],
            ('D', 'E'): ['F'],
        }
        start_key = _pick_start_key(possibles)
        assert start_key in possibles.keys()


class TestGenerate:
    """Test cases for the _generate function."""

    def test_generate_returns_string(self):
        """Test that _generate returns a string."""
        possibles = {
            ('The', 'quick'): ['brown', 'red'],
            ('quick', 'brown'): ['fox'],
            ('brown', 'fox'): ['jumps'],
            ('fox', 'jumps'): ['over'],
        }
        start_key = ('The', 'quick')
        result = _generate(possibles, start_key, max_words=10)
        assert isinstance(result, str)

    def test_generate_respects_max_words(self):
        """Test that _generate respects the max_words parameter."""
        possibles = {
            ('The', 'quick'): ['brown'],
            ('quick', 'brown'): ['fox'],
            ('brown', 'fox'): ['jumps'],
            ('fox', 'jumps'): ['over'],
            ('jumps', 'over'): ['the'],
        }
        start_key = ('The', 'quick')
        result = _generate(possibles, start_key, max_words=5)
        words = result.split()
        # Should generate approximately max_words (plus the initial key words)
        assert len(words) <= 10  # Some margin for the initial key

    def test_generate_with_empty_choices(self):
        """Test _generate handles keys with no choices gracefully."""
        possibles = {
            ('The', 'quick'): ['brown'],
            ('quick', 'brown'): ['fox'],
        }
        start_key = ('The', 'quick')
        result = _generate(possibles, start_key, max_words=10)
        assert isinstance(result, str)

    def test_generate_with_single_element_key(self):
        """Test _generate with prefix length of 1."""
        possibles = {
            ('The',): ['quick'],
            ('quick',): ['brown'],
            ('brown',): ['fox'],
        }
        start_key = ('The',)
        result = _generate(possibles, start_key, max_words=5)
        assert isinstance(result, str)


class TestCreativeAndDeterministic:
    """Test cases for _creative and _deterministic functions."""

    @patch('lib.MarkovGenerator._file_path')
    @patch('lib.MarkovGenerator.env.get_input_filename')
    @patch('lib.MarkovGenerator.env.get_max_words')
    def test_creative_returns_string(self, mock_max_words, mock_get_input_filename, mock_file_path):
        """Test that _creative returns a string."""
        test_file = Path(__file__).parent / 'test_data' / 'test_input.txt'
        mock_file_path.return_value = [test_file]
        mock_get_input_filename.return_value = ['test_input.txt']
        mock_max_words.return_value = 20
        
        result = _creative()
        assert isinstance(result, str)
        assert len(result) > 0

    @patch('lib.MarkovGenerator._file_path')
    @patch('lib.MarkovGenerator.env.get_input_filename')
    @patch('lib.MarkovGenerator.env.get_max_words')
    def test_deterministic_returns_string(self, mock_max_words, mock_get_input_filename, mock_file_path):
        """Test that _deterministic returns a string."""
        test_file = Path(__file__).parent / 'test_data' / 'test_input.txt'
        mock_file_path.return_value = [test_file]
        mock_get_input_filename.return_value = ['test_input.txt']
        mock_max_words.return_value = 20
        
        result = _deterministic()
        assert isinstance(result, str)
        assert len(result) > 0

    @patch('lib.MarkovGenerator._build_possibles')
    @patch('lib.MarkovGenerator.env.get_max_words')
    def test_creative_uses_prefix_len_2(self, mock_max_words, mock_build_possibles):
        """Test that _creative uses prefix length of 2."""
        mock_max_words.return_value = 10
        mock_build_possibles.return_value = {
            ('The', 'quick'): ['brown'],
            ('quick', 'brown'): ['fox'],
        }
        
        _creative()
        mock_build_possibles.assert_called_once_with(prefix_len=2)

    @patch('lib.MarkovGenerator._build_possibles')
    @patch('lib.MarkovGenerator.env.get_max_words')
    def test_deterministic_uses_prefix_len_3(self, mock_max_words, mock_build_possibles):
        """Test that _deterministic uses prefix length of 3."""
        mock_max_words.return_value = 10
        mock_build_possibles.return_value = {
            ('The', 'quick', 'brown'): ['fox'],
            ('quick', 'brown', 'fox'): ['jumps'],
        }
        
        _deterministic()
        mock_build_possibles.assert_called_once_with(prefix_len=3)


class TestRun:
    """Test cases for the run function."""

    @patch('lib.MarkovGenerator.env.get_temperature')
    @patch('lib.MarkovGenerator._creative')
    def test_run_calls_creative_when_temp_high(self, mock_creative, mock_temp):
        """Test that run calls _creative when temperature >= 0.5."""
        mock_temp.return_value = 0.7
        mock_creative.return_value = "Creative text"
        
        result = run()
        mock_creative.assert_called_once()
        assert result == "Creative text"

    @patch('lib.MarkovGenerator.env.get_temperature')
    @patch('lib.MarkovGenerator._creative')
    def test_run_calls_creative_when_temp_exactly_half(self, mock_creative, mock_temp):
        """Test that run calls _creative when temperature == 0.5."""
        mock_temp.return_value = 0.5
        mock_creative.return_value = "Creative text"
        
        result = run()
        mock_creative.assert_called_once()
        assert result == "Creative text"

    @patch('lib.MarkovGenerator.env.get_temperature')
    @patch('lib.MarkovGenerator._deterministic')
    def test_run_calls_deterministic_when_temp_low(self, mock_deterministic, mock_temp):
        """Test that run calls _deterministic when temperature < 0.5."""
        mock_temp.return_value = 0.3
        mock_deterministic.return_value = "Deterministic text"
        
        result = run()
        mock_deterministic.assert_called_once()
        assert result == "Deterministic text"

    @patch('lib.MarkovGenerator.env.get_temperature')
    @patch('lib.MarkovGenerator._deterministic')
    def test_run_calls_deterministic_when_temp_zero(self, mock_deterministic, mock_temp):
        """Test that run calls _deterministic when temperature == 0."""
        mock_temp.return_value = 0.0
        mock_deterministic.return_value = "Deterministic text"
        
        result = run()
        mock_deterministic.assert_called_once()
        assert result == "Deterministic text"

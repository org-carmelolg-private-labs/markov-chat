"""
Module for generating text using Markov chains.
"""
import random
import textwrap
from pathlib import Path
from collections import defaultdict, deque

from lib.EnvironmentVariables import EnvironmentVariables
from lib.StringUtils import normalize, substring

env = EnvironmentVariables()


def run():
    """
    Run the Markov chain text generator.
    
    Returns:
        Generated text string
    """
    if env.get_temperature() >= 0.5:
        return _creative()
    else:
        return _deterministic()


def _file_path():
    """
    Get the file paths for input text files.
    
    Returns:
        List of Path objects for input files
    """
    base = Path(__file__).resolve().parent.parent
    paths = []
    for filename in env.get_input_filename():
        paths.append(base / 'static' / filename)
    return paths


def _read_words(file_paths):
    """
    Read and normalize words from input files.
    
    Args:
        file_paths: List of Path objects to read from
        
    Yields:
        Normalized words from the files
    """
    for file_path in file_paths:
        with file_path.open('r', encoding='utf-8') as file:
            for line in file:
                for word in line.split():
                    normalized = normalize(word)
                    if normalized is not None:
                        yield normalized


def _build_possibles(prefix_len: int):
    """
    Build a dictionary of possible next words for each prefix.
    
    Args:
        prefix_len: Length of the prefix (context window)
        
    Returns:
        Dictionary mapping prefix tuples to lists of possible next words
        
    Raises:
        FileNotFoundError: If input files are not found
    """
    file_paths = _file_path()
    if len(file_paths) == 0:
        raise FileNotFoundError(f"File empty")

    for file_path in file_paths:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    possibles = defaultdict(list)
    dq = deque([''] * prefix_len, maxlen=prefix_len)
    for word in _read_words(file_paths):
        possibles[tuple(dq)].append(word)
        dq.append(word)

    # Fill tail keys with empty terminator to avoid missing keys
    tail = list(dq)
    for _ in range(prefix_len):
        possibles[tuple(tail)].append('')
        tail = tail[1:] + ['']

    return possibles


def _pick_start_key(possibles):
    """
    Pick a starting key from the possibles dictionary.
    
    Prefers keys that start with uppercase letters for better sentence structure.
    
    Args:
        possibles: Dictionary of possible next words
        
    Returns:
        A tuple representing the starting key
    """
    # Prefer keys whose first element starts with an uppercase letter
    candidates = [k for k in possibles.keys() if k[0] and k[0][0].isupper()]
    if not candidates:
        candidates = [k for k in possibles.keys() if k[0]]
    if not candidates:
        candidates = list(possibles.keys())
    return random.choice(candidates)


def _generate(possibles, start_key, max_words):
    """
    Generate text using the Markov chain.
    
    Args:
        possibles: Dictionary of possible next words
        start_key: Starting key tuple
        max_words: Maximum number of words to generate
        
    Returns:
        Generated text string
    """
    key = tuple(start_key)
    output = list(key)

    for _ in range(max_words):
        choices = possibles.get(key, [''])
        word = random.choice(choices)
        output.append(word)
        key = tuple(list(key[1:]) + [word]) if len(key) > 1 else (word,)

    return substring(textwrap.fill(' '.join(output)), ';.!')


def _deterministic():
    """
    Generate text in deterministic mode (larger prefix for more coherent text).
    
    Returns:
        Generated text string
    """
    possibles = _build_possibles(prefix_len=3)
    start_key = _pick_start_key(possibles)
    return _generate(possibles, start_key, env.get_max_words())


def _creative():
    """
    Generate text in creative mode (smaller prefix for more varied text).
    
    Returns:
        Generated text string
    """
    possibles = _build_possibles(prefix_len=2)
    start_key = _pick_start_key(possibles)
    return _generate(possibles, start_key, env.get_max_words())

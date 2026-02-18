"""
Module for string utility functions.
"""
import re


def normalize(word: str):
    """
    Normalize a word by removing special characters like quotes, parentheses, underscores, etc.
    
    Args:
        word: The word to normalize
        
    Returns:
        The normalized word
    """
    regex_pattern = r'[""()_`\'"\n]'
    cleaned = re.sub(regex_pattern, "", word)

    # if cleaned.isupper() and len(cleaned) > 0:
    #     return cleaned[0].upper() + cleaned[1:].lower()

    return cleaned


def substring(word: str, delimiter: str):
    """
    Split a word by delimiter(s) and return the first part.
    
    Args:
        word: The word to split
        delimiter: String containing delimiter characters (e.g., ';.!')
        
    Returns:
        The first part before any delimiter
    """
    regex_pattern = fr"[{delimiter}]"
    return re.split(regex_pattern, word)[0]

"""
Module to load environment variables from a .env file.
"""
import os
from typing import List
from dotenv import load_dotenv

class EnvironmentVariables:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            load_dotenv()  # Load .env once at initialization
        return cls._instance

    def get_max_words(self, default: int = 50) -> int:
        """
        Get the MAX_WORDS environment variable as an integer.
        
        Args:
            default: Default value if the environment variable is not set (default: 50)
            
        Returns:
            The MAX_WORDS value as an integer
        """
        value = os.getenv("MAX_WORDS")
        if value is None:
            return default
        return int(value)

    def get_input_filename(self, default: str = None) -> List[str]:
        """
        Get the INPUT_FILENAME environment variable and split it into a list.
        
        Args:
            default: Default value if the environment variable is not set
            
        Returns:
            A list of filenames
        """
        value = os.getenv("INPUT_FILENAME", default)
        if value is None:
            return []
        return value.split(',')

    def get_temperature(self, default: float = 1.0) -> float:
        """
        Get the TEMPERATURE environment variable as a float.
        
        Args:
            default: Default value if the environment variable is not set (default: 1.0)
            
        Returns:
            The TEMPERATURE value as a float
        """
        value = os.getenv("TEMPERATURE")
        if value is None:
            return default
        return float(value)


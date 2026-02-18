"""
Module to load environment variables from a .env file.
"""
import os
from dotenv import load_dotenv

class EnvironmentVariables:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            load_dotenv()  # Load .env once at initialization
        return cls._instance

    def get_max_words(self, default: int = None) -> int:
        """
        Get the MAX_WORDS environment variable.
        
        Args:
            default: Default value if the environment variable is not set
            
        Returns:
            The MAX_WORDS value or default
        """
        return os.getenv("MAX_WORDS", default)

    def get_input_filename(self, default: str = None) -> list:
        """
        Get the INPUT_FILENAME environment variable and split it into a list.
        
        Args:
            default: Default value if the environment variable is not set
            
        Returns:
            A list of filenames
        """
        return os.getenv("INPUT_FILENAME", default).split(',')

    def get_temperature(self, default: float = None) -> float:
        """
        Get the TEMPERATURE environment variable as a float.
        
        Args:
            default: Default value if the environment variable is not set
            
        Returns:
            The TEMPERATURE value as a float
        """
        return float(os.getenv("TEMPERATURE", default))


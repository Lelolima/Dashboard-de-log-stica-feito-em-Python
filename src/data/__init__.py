"""
Módulo de dados do Dashboard.
"""

from src.data.loader import DataLoader, load_data  # noqa: F401
from src.data.processor import DataProcessor  # noqa: F401

__all__ = [
    "DataLoader",
    "load_data",
    "DataProcessor",
]
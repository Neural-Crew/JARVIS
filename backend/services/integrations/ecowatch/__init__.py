"""
Package d'intégration ECOWATCH.
"""

from .client import EcoWatchAPIError, EcoWatchClient

__all__ = ["EcoWatchClient", "EcoWatchAPIError"]

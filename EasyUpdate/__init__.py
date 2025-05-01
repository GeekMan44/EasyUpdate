"""
"A simple tool to add auto-update functionality to your Python scripts using a server or GitHub."
"""
from .core import UpdateManager, updater         # ou où que soit ta classe EasyUpdate

__all__ = ["EasyUpdate", "updater"]
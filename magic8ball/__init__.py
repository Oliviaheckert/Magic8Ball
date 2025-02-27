# __init__.py
print(f"Initializing package...")  # Optional startup message

# Import submodules (only if you have utils.py/core.py)
from . import utils, core

# Define public API (controls "from magic8ball import *")
__all__ = ['utils', 'core', 'VERSION']

# Package metadata (accessible via magic8ball.VERSION)
VERSION = "1.0.0"

"""Ensure the repository root is importable no matter where pytest is invoked."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

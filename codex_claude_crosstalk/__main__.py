"""
Main entry point for the Codex-Claude-Agent-Crosstalk CLI.
"""

import sys
from .cli.main import main

if __name__ == "__main__":
    sys.exit(main())
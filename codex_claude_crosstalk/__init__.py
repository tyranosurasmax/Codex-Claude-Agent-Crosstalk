"""
Codex-Claude-Agent-Crosstalk

A powerful integration tool that combines Claude Desktop/Code capabilities 
with Codex to streamline full project creation and development workflows.
"""

__version__ = "0.1.0"
__author__ = "Codex-Claude-Agent-Crosstalk Team"
__email__ = "contact@example.com"

from .core.manager import CrosstalkManager
from .agents.claude_agent import ClaudeAgent
from .agents.codex_agent import CodexAgent

__all__ = [
    "CrosstalkManager",
    "ClaudeAgent", 
    "CodexAgent",
]
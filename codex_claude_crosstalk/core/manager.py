"""
Core integration manager for coordinating between Claude and Codex agents.
"""

import logging
import asyncio
from typing import Dict, Any, Optional, List
from ..config.settings import Settings

logger = logging.getLogger(__name__)


class CrosstalkManager:
    """
    Main manager class that coordinates communication between Claude and Codex agents.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the crosstalk manager.
        
        Args:
            config: Optional configuration dictionary
        """
        self.settings = Settings(config)
        self.claude_agent = None
        self.codex_agent = None
        self._initialized = False
        
    async def initialize(self):
        """Initialize the agents and connections."""
        try:
            from ..agents.claude_agent import ClaudeAgent
            from ..agents.codex_agent import CodexAgent
            
            self.claude_agent = ClaudeAgent(self.settings.claude_config)
            self.codex_agent = CodexAgent(self.settings.codex_config)
            
            await self.claude_agent.initialize()
            await self.codex_agent.initialize()
            
            self._initialized = True
            logger.info("CrosstalkManager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize CrosstalkManager: {e}")
            raise
            
    async def generate_project(self, name: str, project_type: str, requirements: List[str] = None) -> Dict[str, Any]:
        """
        Generate a full project using both Claude and Codex.
        
        Args:
            name: Project name
            project_type: Type of project (web-app, cli-tool, etc.)
            requirements: Optional list of specific requirements
            
        Returns:
            Dictionary containing project structure and files
        """
        if not self._initialized:
            await self.initialize()
            
        logger.info(f"Generating project: {name} (type: {project_type})")
        
        # Get initial project structure from Claude
        claude_structure = await self.claude_agent.design_project_structure(
            name, project_type, requirements
        )
        
        # Have Codex generate the actual code
        codex_implementation = await self.codex_agent.implement_project(
            claude_structure
        )
        
        # Have Claude review the implementation
        reviewed_code = await self.claude_agent.review_implementation(
            codex_implementation
        )
        
        return {
            "name": name,
            "type": project_type,
            "structure": claude_structure,
            "implementation": reviewed_code,
            "status": "completed"
        }
        
    async def generate_component(self, component_name: str, specs: Dict[str, Any], review: bool = True) -> Dict[str, Any]:
        """
        Generate a specific component with optional cross-review.
        
        Args:
            component_name: Name of the component to generate
            specs: Component specifications
            review: Whether to perform cross-review
            
        Returns:
            Generated component code and metadata
        """
        if not self._initialized:
            await self.initialize()
            
        logger.info(f"Generating component: {component_name}")
        
        # Generate initial code with Codex
        initial_code = await self.codex_agent.generate_component(component_name, specs)
        
        if review:
            # Review with Claude
            reviewed_code = await self.claude_agent.review_code(initial_code)
            return reviewed_code
        
        return initial_code
        
    async def interactive_session(self):
        """Start an interactive session for collaborative development."""
        if not self._initialized:
            await self.initialize()
            
        logger.info("Starting interactive session")
        
        print("🤖 Codex-Claude-Agent-Crosstalk Interactive Session")
        print("Type 'help' for commands, 'exit' to quit")
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if user_input.lower() in ['exit', 'quit']:
                    break
                elif user_input.lower() == 'help':
                    self._show_help()
                elif user_input.startswith('generate '):
                    await self._handle_generate_command(user_input[9:])
                elif user_input.startswith('review '):
                    await self._handle_review_command(user_input[7:])
                else:
                    print("Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Error in interactive session: {e}")
                print(f"Error: {e}")
        
        print("Session ended.")
        
    def _show_help(self):
        """Show available commands."""
        help_text = """
Available commands:
  generate <component>  - Generate a new component
  review <file>        - Review existing code
  help                 - Show this help message
  exit/quit           - Exit the session
        """
        print(help_text)
        
    async def _handle_generate_command(self, args: str):
        """Handle generate command in interactive mode."""
        # Simple implementation for demo
        print(f"Generating: {args}")
        
    async def _handle_review_command(self, args: str):
        """Handle review command in interactive mode."""
        # Simple implementation for demo
        print(f"Reviewing: {args}")
        
    async def close(self):
        """Clean up resources."""
        if self.claude_agent:
            await self.claude_agent.close()
        if self.codex_agent:
            await self.codex_agent.close()
        logger.info("CrosstalkManager closed")
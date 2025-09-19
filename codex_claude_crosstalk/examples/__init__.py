"""
Example usage of Codex-Claude-Agent-Crosstalk
"""

import asyncio
import logging
from codex_claude_crosstalk import CrosstalkManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def basic_project_generation():
    """Example: Generate a basic CLI project."""
    print("🚀 Example: Basic Project Generation")
    
    # Initialize the manager
    manager = CrosstalkManager()
    await manager.initialize()
    
    # Generate a CLI tool project
    project = await manager.generate_project(
        name="my-awesome-tool",
        project_type="cli-tool",
        requirements=["Handle file processing", "Support multiple formats"]
    )
    
    print(f"✅ Generated project: {project['name']}")
    print(f"   Type: {project['type']}")
    print(f"   Files: {len(project['implementation']['files'])}")
    
    # Clean up
    await manager.close()


async def component_generation():
    """Example: Generate a specific component."""
    print("\n🔧 Example: Component Generation")
    
    manager = CrosstalkManager()
    await manager.initialize()
    
    # Generate a user authentication component
    component = await manager.generate_component(
        component_name="UserAuth",
        specs={
            "type": "class",
            "language": "python",
            "functionality": "User authentication and authorization"
        },
        review=True
    )
    
    print(f"✅ Generated component: {component['name']}")
    print(f"   Language: {component['language']}")
    print(f"   Review score: {component.get('claude_review', {}).get('quality_score', 'N/A')}")
    
    await manager.close()


async def main():
    """Run all examples."""
    print("🤖 Codex-Claude-Agent-Crosstalk Examples\n")
    
    try:
        await basic_project_generation()
        await component_generation()
        
        print("\n🎉 All examples completed successfully!")
        print("\nNext steps:")
        print("1. Set up your API keys in config/config.yaml")
        print("2. Try the CLI: python -m codex_claude_crosstalk --help")
        print("3. Start an interactive session: python -m codex_claude_crosstalk interactive")
        
    except Exception as e:
        logger.error(f"Example failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
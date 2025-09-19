"""
Main CLI entry point for Codex-Claude-Agent-Crosstalk
"""

import sys
import argparse
import asyncio
import logging
from typing import List, Optional

from ..core.manager import CrosstalkManager
from ..config.settings import Settings


def setup_logging(level: str = "INFO"):
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


async def init_command(args):
    """Initialize a new project."""
    print(f"🚀 Initializing project: {args.name}")
    print(f"   Type: {args.type}")
    
    try:
        manager = CrosstalkManager()
        await manager.initialize()
        
        requirements = args.requirements.split(',') if args.requirements else []
        project = await manager.generate_project(args.name, args.type, requirements)
        
        print(f"✅ Project '{args.name}' generated successfully!")
        print(f"   Architecture: {project['structure']['architecture']['pattern']}")
        print(f"   Files: {len(project['implementation']['files'])} files created")
        
        # Save project files
        output_dir = f"output/{args.name}"
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for file_path, content in project['implementation']['files'].items():
            full_path = os.path.join(output_dir, file_path)
            
            # Handle directories
            if file_path.endswith('/'):
                os.makedirs(full_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w') as f:
                    f.write(content)
        
        print(f"   Project saved to: {output_dir}")
        
        await manager.close()
        
    except Exception as e:
        print(f"❌ Error initializing project: {e}")
        return 1
        
    return 0


async def generate_command(args):
    """Generate a component."""
    print(f"🔧 Generating component: {args.component}")
    
    try:
        manager = CrosstalkManager()
        await manager.initialize()
        
        specs = {
            "type": getattr(args, 'type', 'class'),
            "language": getattr(args, 'language', 'python')
        }
        
        component = await manager.generate_component(args.component, specs, args.review)
        
        print(f"✅ Component '{args.component}' generated successfully!")
        if args.review:
            print("   ✅ Code review completed")
            
        # Save component
        output_file = f"output/{args.component}.py"
        import os
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(component.get('code', '# Generated component'))
            
        print(f"   Component saved to: {output_file}")
        
        await manager.close()
        
    except Exception as e:
        print(f"❌ Error generating component: {e}")
        return 1
        
    return 0


async def interactive_command(args):
    """Start interactive session."""
    print("🤖 Starting interactive session...")
    
    try:
        manager = CrosstalkManager()
        await manager.interactive_session()
        await manager.close()
        
    except Exception as e:
        print(f"❌ Error in interactive session: {e}")
        return 1
        
    return 0


def config_command(args):
    """Handle configuration commands."""
    if args.config_action == 'show':
        settings = Settings()
        print("Current configuration:")
        import yaml
        print(yaml.dump(settings.to_dict(), default_flow_style=False))
        
    elif args.config_action == 'init':
        config_dir = "config"
        import os
        os.makedirs(config_dir, exist_ok=True)
        
        example_config = """# Codex-Claude-Agent-Crosstalk Configuration

claude:
  api_key: "your-claude-api-key-here"
  model: "claude-3-sonnet"
  max_tokens: 4000
  temperature: 0.1

codex:
  api_key: "your-openai-api-key-here"  
  model: "code-davinci-002"
  max_tokens: 2000
  temperature: 0.1

templates:
  directory: "templates/"
  default_language: "python"

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

output:
  directory: "output/"
  overwrite: false
"""
        
        config_file = os.path.join(config_dir, "config.yaml")
        with open(config_file, 'w') as f:
            f.write(example_config)
            
        print(f"✅ Configuration template created at: {config_file}")
        print("   Please edit the file and add your API keys.")
        
    return 0


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        description="Codex-Claude-Agent-Crosstalk - AI-powered project generation"
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version='%(prog)s 0.1.0'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize a new project')
    init_parser.add_argument('name', help='Project name')
    init_parser.add_argument('--type', default='cli-tool', 
                           choices=['web-app', 'cli-tool', 'api', 'library'],
                           help='Project type')
    init_parser.add_argument('--requirements', 
                           help='Comma-separated list of requirements')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate a component')
    gen_parser.add_argument('component', help='Component name')
    gen_parser.add_argument('--type', default='class',
                           choices=['class', 'function', 'module'],
                           help='Component type')
    gen_parser.add_argument('--language', default='python',
                           choices=['python', 'javascript', 'typescript'],
                           help='Programming language')
    gen_parser.add_argument('--review', action='store_true',
                           help='Enable cross-AI review')
    
    # Interactive command
    subparsers.add_parser('interactive', help='Start interactive session')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Configuration management')
    config_parser.add_argument('config_action', choices=['show', 'init'],
                              help='Configuration action')
    
    return parser


def main() -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Set up logging
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logging(log_level)
    
    # Handle commands
    if not args.command:
        parser.print_help()
        return 1
        
    try:
        if args.command == 'init':
            return asyncio.run(init_command(args))
        elif args.command == 'generate':
            return asyncio.run(generate_command(args))
        elif args.command == 'interactive':
            return asyncio.run(interactive_command(args))
        elif args.command == 'config':
            return config_command(args)
        else:
            print(f"Unknown command: {args.command}")
            return 1
            
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user")
        return 130
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
"""
Basic CLI Tool Template

This template provides a foundation for command-line tools.
"""

import sys
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the CLI tool."""
    parser = argparse.ArgumentParser(description='{{ project_name }} - {{ project_description }}')
    parser.add_argument('--version', action='version', version='1.0.0')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    # Add your CLI arguments here
    parser.add_argument('command', nargs='?', help='Command to execute')
    parser.add_argument('--input', '-i', help='Input file or data')
    parser.add_argument('--output', '-o', help='Output file or destination')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info(f"Starting {{ project_name }}")
    
    # Your main logic here
    if args.command:
        logger.info(f"Executing command: {args.command}")
        # Process command
        if args.command == "process":
            process_data(args.input, args.output)
        else:
            logger.error(f"Unknown command: {args.command}")
            return 1
    else:
        parser.print_help()
    
    return 0


def process_data(input_file, output_file):
    """Process data from input to output."""
    logger.info(f"Processing data from {input_file} to {output_file}")
    
    # Add your data processing logic here
    try:
        if input_file:
            with open(input_file, 'r') as f:
                data = f.read()
            
            # Process the data
            processed_data = data.upper()  # Example processing
            
            if output_file:
                with open(output_file, 'w') as f:
                    f.write(processed_data)
                logger.info(f"Data processed and saved to {output_file}")
            else:
                print(processed_data)
        else:
            logger.error("No input file specified")
            
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        raise


if __name__ == "__main__":
    sys.exit(main())
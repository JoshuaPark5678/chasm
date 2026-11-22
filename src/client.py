# Chasm EE2E Chat Client

import argparse
from pathlib import Path

# Get the directory where this script is saved
BASE_DIR = Path(__file__).resolve().parent

def main():
    # Initialize the parser
    parser = argparse.ArgumentParser()
    
    # Define arguments and flags
    parser.add_argument(
        "--name", 
        type=str, 
        default="Anon_0", 
        help="The name of the person to greet."
    )
    
    #  Parse and use the arguments
    args = parser.parse_args()
    print(f"Hello, {args.name}!")


if __name__ == "__main__":
    main()




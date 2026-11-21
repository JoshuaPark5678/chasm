# Chasm EE2E Chat Client

import argparse
from pathlib import Path

# Get the directory where this script is saved
BASE_DIR = Path(__file__).resolve().parent

def main():
    # Initialize the parser
    parser = argparse.ArgumentParser(description="A simple greeting CLI tool.")
    
    # Define arguments and flags
    parser.add_argument(
        "--name", 
        type=str, 
        default="Anon_0", 
        help="The name of the person to greet."
    )
    
    #  Parse and use the arguments
    args = parser.parse_args()
    with open(BASE_DIR / "chasm.txt", "r", encoding="utf-8") as file:
        content = file.read()
        print(content)
    print(f"Hello, {args.name}!")


if __name__ == "__main__":
    main()




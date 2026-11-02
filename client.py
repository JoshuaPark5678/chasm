# Chasm EE2E Chat Client

import argparse

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
    print(f"Hello, {args.name}!")


if __name__ == "__main__":
    main()




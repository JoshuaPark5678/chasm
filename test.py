import argparse

def main():
    # 1. Initialize the parser
    parser = argparse.ArgumentParser(description="A simple greeting CLI tool.")
    
    # 2. Define arguments and flags
    parser.add_argument(
        "--name", 
        type=str, 
        default="World", 
        help="The name of the person to greet."
    )
    
    # 3. Parse and use the arguments
    args = parser.parse_args()
    print(f"Hello, {args.name}!")

if __name__ == "__main__":
    main()


import json
import sys

# Print debugging information
print('__________________________________________')
print(f"Argument received: {sys.argv[1]}")

try:
    # Read JSON content from the file specified in the argument
    with open(sys.argv[1], 'r') as file:
        inputs = json.load(file)  # Use json.load() for files

    # Process and print the inputs
    for key, value in inputs.items():
        print(f"{key}: {value}")

except FileNotFoundError:
    print("Error: File not found.")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON format: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)
``

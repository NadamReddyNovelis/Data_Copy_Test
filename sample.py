import json
import sys

print(sys.argv[1])

# Load inputs from the JSON string passed as the first argument
inputs = json.loads(sys.argv[1])

# Use the inputs
for key, value in inputs.items():
    print(f"{key}: {value}")

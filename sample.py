import json
import sys

# Load inputs from the JSON string passed as the first argument
inputs = json.loads(sys.argv[1])

# Use the inputs
for key, value in inputs.items():
    print(f"{key}: {value}")

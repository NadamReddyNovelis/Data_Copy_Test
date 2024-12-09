import json
import sys

# Print debugging information
print('__________________________________________')
input_args = sys.argv[1]
print(f"Argument received: {input_args}")
print("Type : ",type(input_args))
try:
    if type(input_args) == str:
        inputs = json.loads(input_args)
    elif type(input_args) == dict:
        pass
    else:
        sys.exit(1)
    for key, value in inputs.items():
        print(f"{key}: {value}")
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON format: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)

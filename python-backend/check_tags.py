import json

# Function to load the database.json file
def load_json_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            print("Data loaded successfully.")
            return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

# Function to collect and print tags from the intents
def collect_and_print_tags(data):
    # Check if the 'intents' key exists and is a list
    if isinstance(data, dict) and "intents" in data and isinstance(data["intents"], list):
        tags = [entry["tag"] for entry in data["intents"]]
        print("Collected Tags:")
        for tag in tags:
            print(f"- {tag}")
    else:
        print("Data is not in the expected format.")

# Main execution
if __name__ == "__main__":
    # Load data from database.json
    data = load_json_file('database.json')
    
    # Only proceed if data was loaded successfully
    if data:
        # Collect and print tags
        collect_and_print_tags(data)

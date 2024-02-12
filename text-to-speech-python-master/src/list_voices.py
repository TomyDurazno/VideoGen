import json

# Specify the path to your file
file_path = "file.json"

# Read the JSON file
with open(file_path, "r") as file:
    data = json.load(file)

# Print information for each voice
for voice in data["voices"]:
    print("Voice ID:", voice["voice_id"])
    print("Name:", voice["name"])
    print("Description:", voice["description"])
    print("Preview URL:", voice["preview_url"])
    print("Labels:")
    for label_key, label_value in voice["labels"].items():
        print(f"  {label_key}: {label_value}")
    print("-" * 50)  # Separating each voice with a line
import json
import os

json_file = "transacties.json"

# Voorbeelddata
data = [
    {"date": "2025-06-09", "amount": 100, "category": "Test"}
]

# Volledig pad printen
print("Schrijven naar:", os.path.abspath(json_file))

# Schrijven
with open(json_file, "w") as f:
    json.dump(data, f, indent=4)

print("Data weggeschreven!")

# Lezen en printen
with open(json_file, "r") as f:
    inhoud = json.load(f)

print("Inhoud van bestand:", inhoud)

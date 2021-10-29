import json

with open("./silver/matchIds/silver_1_page_matchid_1.json", "r") as f:
    sample_json = json.load(f)
print(sample_json[0])

print(len(set(sample_json)))

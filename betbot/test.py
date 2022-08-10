import json

str = {"user_id": 413020545}
atr = {'balance': 383.25}

with open("../balance.json", 'w') as file:
    json.dump(atr, file, sort_keys=True, indent=20, ensure_ascii=False)
with open("../coupones.json", 'w') as file:
    json.dump(str, file, sort_keys=True, indent=20, ensure_ascii=False)
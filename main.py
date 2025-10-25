import json
skins=[]
with open("skins.json", "r", encoding="utf-8") as f:
        skins = json.load(f)

# for x in skins:
#     if(x["category"]["name"]!="Knives" and x["category"]["name"]!="Gloves"):
#         print(x["pattern"]["name"])
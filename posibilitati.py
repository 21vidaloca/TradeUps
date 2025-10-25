import requests
import json
from typing import Optional, Dict, Any
from urllib.parse import quote 
import re 

RARITY_HIERARCHY = {
    "Consumer Grade": "Industrial Grade",
    "Industrial Grade": "Mil-Spec Grade",
    "Mil-Spec Grade": "Restricted",
    "Restricted": "Classified",
    "Classified": "Covert",
    "Covert": None # Covert skins trade up to Knives/Gloves (special case)
}

def find_skin(weapon_name, skin_name, skin_db):
    for collection in skin_db:
        for skin in collection.get("contains", []):
            skin_full_name = skin.get("name", "")
            if (skin_name in skin_full_name and weapon_name in skin_full_name):
                return skin, collection
    return None, None


def get_possible_outcome_for(weapon_name, skin_name, skin_db):
    
    skin_obj, collection_obj = find_skin(weapon_name, skin_name, skin_db)
    
    if not skin_obj or not collection_obj:
        raise ValueError(f"Skin not found in database: {weapon_name} | {skin_name}")
        
    # --- Step 2: Get its collection and rarity ---
    collection_name = collection_obj.get("name", "Unknown Collection")
    try:
        input_rarity_name = skin_obj["rarity"]["name"]
    except KeyError:
        raise ValueError(f"Skin has missing rarity data: {weapon_name} | {skin_name}")

    # --- Step 3: Find the target rarity ---
    target_rarity_name = RARITY_HIERARCHY.get(input_rarity_name)
    
    if not target_rarity_name:
        # This is a Covert skin or a rarity not in our map
        raise ValueError(f"No trade-up path found for rarity: {input_rarity_name}")

    possible_outcomes = []
    for skin_in_collection in collection_obj.get("contains", []):
        if skin_in_collection["rarity"]["name"] == target_rarity_name:
            possible_outcomes.append(skin_in_collection.get("name"))
    return possible_outcomes
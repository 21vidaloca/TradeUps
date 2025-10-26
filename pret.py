import requests
import json
from typing import Optional, Dict, Any
from urllib.parse import quote 
import re 
def parse_steam_price(price_str: str) -> float:
    if not price_str:
        return 0.0
    cleaned_str = re.sub(r"[$,€£\s]", "", price_str).replace(",", ".")
    
    try:
        return float(cleaned_str)
    except ValueError:
        numeric_part = re.search(r"[\d\.]+", cleaned_str)
        if numeric_part:
            try:
                return float(numeric_part.group(0))
            except ValueError:
                return 0.0
        return 0.0

def get_skin_price(weapon_name: str, skin_name: str, condition: str) -> Optional[Dict[str, Any]]:
    print(f"Attempting to fetch price for: {weapon_name} | {skin_name} ({condition})")

    # --- START OF REAL API SECTION (Option 1) ---
    
    # Construct the market_hash_name
    # Example: "AK-47 | Redline (Field-Tested)"
    market_hash_name = f"{weapon_name} | {skin_name} ({condition})"
    
    API_ENDPOINT = "https://steamcommunity.com/market/priceoverview/"
    PARAMS = {
        "appid": 730,  
        "currency": 1,     
        "market_hash_name": market_hash_name
    }
    
    # Use a basic User-Agent header to mimic a browser request
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    try:
        # Note: We URL-encode the market_hash_name in the params manually
        # to ensure characters like '|' are handled, although requests usually does this.
        # A safer way is to let requests handle it by passing the dict.
        response = requests.get(API_ENDPOINT, params=PARAMS, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            data = response.json()
            
            if data and data.get("success"):
                
                lowest_price_str = data.get("lowest_price")
                median_price_str = data.get("median_price")
                volume_str = data.get("volume")

                lowest_price = parse_steam_price(lowest_price_str)
                median_price = parse_steam_price(median_price_str)
                
                volume = 0
                if volume_str:
                    try:
                        volume = int(volume_str.replace(",", ""))
                    except ValueError:
                        pass # Keep volume at 0 if parsing fails
                ####################print(median_price)
                return {
                    "market_hash_name": market_hash_name,
                    "lowest_price": lowest_price,
                    "median_price": median_price,
                    "volume": volume,
                    "currency": "USD", # Based on our 'currency: 1' param
                    "note": "Prices from unofficial Steam API. Float value is ignored."
                }
            else:
                print(f"Error: API call was not successful. (Item not found?)")
                print(f"Response: {data}")
                return None

        else:
            # Handle common HTTP errors (e.g., 429 Too Many Requests)
            print(f"Error: API request failed with status code {response.status_code}")
            print("This may be due to rate limiting. Try again later.")
            print(f"Response: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {e}")
        return None
    
    # --- END OF REAL API SECTION ---
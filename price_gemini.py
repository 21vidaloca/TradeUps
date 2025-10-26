import requests
import json
import time

def call_gemini_api(user_query, system_prompt, retries=3, delay=1):
    """
    Calls the Gemini API with exponential backoff and Google Search grounding.
    """
    # API key is handled by the environment, leaving it as an empty string.
    api_key = "AIzaSyAB8GMnCcOMMkl7UxtbVEcEuL-ZoEFjbxU" 
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={api_key}"

    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "tools": [{"google_search": {}}],  # Use Google Search!
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        },
    }

    headers = {
        "Content-Type": "application/json"
    }

    for i in range(retries):
        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(payload))
            
            # Raise an exception for bad status codes
            response.raise_for_status()

            result = response.json()
            candidate = result.get("candidates", [{}])[0]
            
            text = candidate.get("content", {}).get("parts", [{}])[0].get("text")

            if text:
                # Extract grounding sources
                sources = []
                grounding_metadata = candidate.get("groundingMetadata", {})
                if grounding_metadata and "groundingAttributions" in grounding_metadata:
                    sources = [
                        {
                            "uri": attr.get("web", {}).get("uri"),
                            "title": attr.get("web", {}).get("title"),
                        }
                        for attr in grounding_metadata["groundingAttributions"]
                        if attr.get("web", {}).get("uri") and attr.get("web", {}).get("title")
                    ]
                
                return {"text": text, "sources": sources}
            else:
                raise ValueError("Invalid API response structure.")

        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            if i == retries - 1:
                # If this was the last retry, re-throw the error
                raise
            # Wait with exponential backoff before retrying
            time.sleep(delay * (2**i))
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

def fetch_skin_price(skin_name, skin_condition, skin_float=None):
    """
    Prepares the query and calls the Gemini API to get the skin price.
    """
    if not skin_name:
        print("Error: Please enter a skin name.")
        return

    # 1. Construct the User Query
    user_query = f"What is the current market price for a {skin_name} {skin_condition}?"
    if skin_float:
        # If a float is provided, make the query much more specific
        user_query = f"What is the price for a {skin_name} {skin_condition} with a float value of {skin_float}?"

    # 2. Define the System Prompt
    system_prompt = "You are a video game skin price analyst. The user will ask for the price of a skin. Use the provided search tool to find the most accurate, real-time price. Respond *only* with the price in USD (e.g., '$123.45') or, if the price cannot be found, respond with 'Price not found.' Do not add any conversational text, greetings, or explanations."

    try:
        # 3. Call the Gemini API
        print("Searching for price...")
        price_data = call_gemini_api(user_query, system_prompt)
        
        # 4. Display the results
        price_text = price_data.get("text", "")
        sources = price_data.get("sources", [])

        if "price not found" in price_text.lower():
            print(f"Could not find a price for '{skin_name} {skin_condition}'. Please check the spelling.")
        else:
            print("-" * 30)
            print(f"Estimated Market Price: {price_text}")
            print("-" * 30)
            
            return price_data

    except Exception as e:
        print(f"An error occurred while fetching the price: {e}")


import math

def find_best_tradeup_combo(skin_a, skin_b, output_skin, desired_output_float, max_budget):
    # Skin A (Your good, low-float skin)
    skin_a = {
        'name': 'Low-Float Skin (0-1 Range)',
        'float': 0.0123,  # The actual float of the skin you found
        'cost': 1.80,     # The price of this specific skin
        'min_wear': 0.00, # This skin's min possible float
        'max_wear': 1.00  # This skin's max possible float
    }

    # Skin B (Your cheap "floater" skin with a limited range)
    skin_b = {
        'name': 'Floater Skin (Limited Range)',
        'float': 0.185,   # A "good" float for this limited-range skin
        'cost': 0.45,     # The price of this floater
        'min_wear': 0.15, # This skin's min possible float (e.g., FT)
        'max_wear': 0.80  # This skin's max possible float
    }



    

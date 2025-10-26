import requests
import json
from typing import Optional, Dict, Any
from urllib.parse import quote 
from collections import defaultdict
import re 
from conditie import get_condition
def calculate_single_outcome_float(avg_normalized_float, outcome_min_float, outcome_max_float):
    return (avg_normalized_float * (outcome_max_float - outcome_min_float)) + outcome_min_float
def get_outcome(input_skins, skins):
    
    # --- Input Validation ---
    if len(input_skins) != 10:
        raise ValueError(f"Trade-up contract must contain exactly 10 items. Found {len(input_skins)}.")


    # --- Step 2: Group inputs by collection ---
    collection_counts = defaultdict(int)
    collection_to_outcomes = {}

    for skin in input_skins:
        collection_counts[skin[3]] += 1
        
        if skin[3] not in collection_to_outcomes:
            collection_to_outcomes[skin[3]] = skin[4]
    # --- Step 3 & 4: Calculate Probabilities ---
    
    final_probabilities = {}
    total_inputs = 10.0

    for collection_name, count in collection_counts.items():
        
        # P(Collection) = (Number of skins from Collection) / 10
        collection_chance = count / total_inputs
        
        # Get the list of possible skins from this collection
        outcomes = collection_to_outcomes[collection_name]
        num_outcomes = len(outcomes)
        
        if num_outcomes == 0:
            print(f"Warning: Collection '{collection_name}' has 0 defined outcomes for this tier.")
            continue
            
        # Calculate the chance for each individual skin
        # P(Skin) = P(Collection) / (Number of possible outcomes in Collection)
        individual_skin_chance = collection_chance / num_outcomes
        
        # Assign this probability to each skin in the outcome list
        for skin_name in outcomes:
            final_probabilities[skin_name] = [individual_skin_chance]

    # print(collection_to_outcomes)
    # FLOATTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
            
    # --- Step 1 & 2: Calculate Average Normalized Float ---
    total_normalized_float = 0
    for skin in input_skins:
        # Formula: NormalizedFloat = (InputFloat - MinFloat) / (MaxFloat - MinFloat)
        float_max=skin[6]
        float_min=skin[5]
        float_value=skin[7]
        range_width = float_max - float_min
        if range_width == 0:
            normalized_float = 0 # or 0.5, or 1.0; 0 is safest
        else:
            normalized_float = (float_value - float_min) / range_width
        
        total_normalized_float += normalized_float
        
    avg_normalized_float = total_normalized_float / 10.0
    #AM CALCULAT PENTRU INPUTTTTTTTTTTTTT
    #URMEAZA PENTRU OUTPUTTTTTTTTTTTT

    # --- Step 3: Map Average to Each Potential Outcome ---
    outcome_floats = {}
    
    # We iterate through the collections_to_outcomes to find
    # all unique possible outcomes
    # print("###################")
    all_possible_outcomes = []
    for outcomes_list in collection_to_outcomes.values():
        
        all_possible_outcomes.extend(outcomes_list)

    # print(all_possible_outcomes)
    # print("###################")
        
    # Remove duplicates just in case (though unlikely with this structure)
    # This is tricky with dicts. A better way is to just iterate and add.
    
    for collection_outcomes in collection_to_outcomes.values():
        for outcome in collection_outcomes:
            intrare={}
            for ceva in skins:
                if ceva["name"] == outcome:
                    intrare=ceva
                    break
            # print(outcome, intrare["name"],intrare["min_float"],intrare["max_float"])

            if intrare["name"] not in outcome_floats:
                # Formula: OutputFloat = (AvgNormalized * (OutMax - OutMin)) + OutMin
                out_name = intrare["name"]
                out_min = intrare["min_float"]
                out_max = intrare["max_float"]
                
                # Call the new, separate function for the calculation
                output_float = calculate_single_outcome_float(
                    avg_normalized_float, out_min, out_max
                )
                final_probabilities[out_name].append(output_float)
                final_probabilities[out_name].append(get_condition(output_float))
            

    return final_probabilities
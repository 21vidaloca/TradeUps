def get_condition(float_value):
    """
    Returns the string name of a skin's wear condition based on its float value.

    The wear ranges are:
    - 0.00 - 0.07: Factory New (FN)
    - 0.07 - 0.15: Minimal Wear (MW)
    - 0.15 - 0.38: Field-Tested (FT)
    - 0.38 - 0.45: Well-Worn (WW)
    - 0.45 - 1.00: Battle-Scarred (BS)
    """
    if float_value < 0.07:
        return "Factory New"
    elif float_value < 0.15:
        return "Minimal Wear"
    elif float_value < 0.38:
        return "Field-Tested"
    elif float_value < 0.45:
        return "Well-Worn"
    else:
        return "Battle-Scarred"
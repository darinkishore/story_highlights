import random

# TODO: question: how handle bold?

color_mappings = {
        "Main Male Character": "#1155cc",  # Dark cornflower blue 2
        "Other Male 3": "#a4c2f4",  # Light Cornflower blue 2
        "Other Male 2": "#6d9eeb",  # Light Cornflower blue 1
        "Other Male 1": "#4a86e8",  # Cornflower blue
        "One-off Male": "#c9daf8", # Light Cornflower blue 3
        "Main Female Character": "#ff00ff",  # Magenta
        "Other Female 3": "#ead1dc",  # Light Magenta 3
        "Other Female 2": "#d5a6bd",  # Light Magenta 2
        "Other Female 1": "#a64d79",  # Light Magenta 1
        "One-off Female": "#f8d9e9",
        # TODO: unrevealed/revealed antagonist
        "Antagonist/Villain": "#ff0000" if random.random() > discretion_threshold else "#999999",  # Red or Dark gray 2
        "Groups of People": "#9900ff",  # Purple
        "Danger or Violence": "#ff0000",  # Red
        "Important Information": "#f1c232",  # Dark Yellow 1
        "Climax or Resolution": "#ff9900", # Orange
        "Positive Time Reference": "#93c47d",
        "Negative Time Reference": "#ff0000"
        "Positive Descriptions": "#6fa8dc",  # Light blue 1
        "Negative Descriptions": "#ff0000",  # Red
        "Nature Descriptions": "#b6d7a8",  # Light green 2
        "Money and Wealth": "#38761d",  # Dark Green 2
        "Water-Related Descriptions": "#6fa8dc",  # Light blue 1
    }

def get_color_mapping(key):
    discretion_threshold = 0.5  # 50% probability
    # if its other male or other female > 3 then subtract 3
    if "Other Male" in key or "Other Female" in key:
        ind = int(key[-1])
        if ind > 3:
            key = "Other Male" if "Other Male" in key else "Other Female"
            key = f"{key} {ind - 3}"
    

    return color_mappings.get(key, None)

def get_reverse_color_mapping(value):
    return {v: k for k, v in color_mappings.items()}.get(value, None)
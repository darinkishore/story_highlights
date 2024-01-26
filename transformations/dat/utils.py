import rapidfuzz.process
from rapidfuzz.distance import Levenshtein
from transformations.dat.prompts.prompt_templates import categories


def get_highlight_priority(label):
    category_priorities = {
        "Characters": 3,
        "Plot Elements": 2,
        "Descriptions": 1
    }
    
    # Flatten the categories dictionary to a list of keys with their associated category
    flattened_categories = [(key, category) for category, keys in categories.items() for key in keys]
    
    # Find the closest match within a Levenshtein distance of 2
    closest_match = rapidfuzz.process.extractOne(
        label,
        [key for key, _ in flattened_categories],
        score_cutoff=2,
        scorer=Levenshtein.distance
    )
    
    if closest_match is None:
        raise ValueError(f"No category found within a Levenshtein distance of 2 for label '{label}'")
    
    # Get the category of the closest match
    _, closest_category = next(filter(lambda x: x[0] == closest_match[0], flattened_categories))
    
    # Return the priority number for the category
    return category_priorities[closest_category]

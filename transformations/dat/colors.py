import rapidfuzz
from loguru import logger

# TODO: question: how handle bold?

color_mappings = {
    "Main Male Character": "#1155cc",
    "Male Character 3": "#a4c2f4",
    "Male Character 2": "#6d9eeb",
    "Male Character 1": "#4a86e8",
    "Main Female Character": "#ff00ff",
    "Female Character 3": "#ead1dc",
    "Female Character 2": "#d5a6bd",
    "Female Character 1": "#a64d79",
    "Antagonist/Villain": "#ff0000",
    "Antagonist or Villain": "#ff0000",
    "Danger or Violence": "#ff0000",
    "Danger/Violence": "#ff0000",
    "Unknown Role": "#999999",
    "Groups of People": "#9900ff",
    "Important Information": "#f1c232",
    "Climax or Resolution": "#ff9900",
    "Positive Time Reference": "#93c47d",
    "Neutral Time Reference": "#93c47d",
    "Negative Time Reference": "#ff0000",
    "Positive Description": "#6fa8dc",
    "Negative Description": "#ff0000",
    "Nature Description": "#b6d7a8",
    "Money and Wealth": "#38761d",
    "Water-Related Description": "#6fa8dc",
}

color_set = set(color_mappings.keys())


def get_color_mapping(key):
    logger.info(f'Entering get_color_mapping with key: {key}')
    # if its other male or other female > 3 then subtract 3
    if key[-1].isdigit():
        ind = int(key[-1])
        if ind > 3:
            key = "Other Male" if "Other Male" in key else "Other Female"
            key = f"{key} {ind - 3}"
    try:
        color = color_mappings[key]
        logger.info(f'Successfully retrieved color: {color}')
    except KeyError:
        # use levenshtein distance to find the closest match
        logger.warning(f'Key "{key}" not found in color mappings. Using rapidfuzz to find closest match.')
        closest_match = rapidfuzz.process.extractOne(
            key,
            color_set,
            score_cutoff=2,
            scorer=rapidfuzz.distance.Levenshtein.distance,
        )
        if closest_match is None:
            raise KeyError(f"Label {key} not found in color mapping.")
        else:
            color = color_mappings[closest_match[0]]
            logger.info(f'Closest match found for key "{key}": {closest_match[0]}')
    return color


def get_reverse_color_mapping(value):
    reverse_map = {v: k for k, v in color_mappings.items()}
    try:
        key = reverse_map[value]
    except KeyError:
        raise KeyError(f"Value {value} not found in reverse mapping.")
    return key

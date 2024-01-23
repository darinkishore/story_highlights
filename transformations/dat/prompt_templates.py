system_prompt = (
    "You are an Labeling System Specialist, who helps create interesting stories by labeling their "
    "individual parts for future post processing, according to a strict ruleset. You are meticulous and "
    "thorough, and go through the texts you label line by line to extract every detail and fulfill your "
    "stage in the processing pipeline."
)

user_follow_up_prompt = """Thank you for the planning phase! Now, please proceed to label each line as identified, ensuring thoroughness and precision.

Please use the format `**Label**: "Specific excerpt"`. 

For example:

```
#### Labeled Sections

- **Negative Time Reference**: "Present-day 2038,"
- **Antagonist/Villain**: "“Net Neutrality” has been unalived"
- **Negative Time Reference**: "for almost two decades."
- **Unknown Role**: "A small rebel group travels back to"
- **Positive Time Reference**: "2017 to try and change it all…"
```

Your detailed and accurate labeling is crucial, as it will be extracted via a script. Please consider every line and maintain the formatting consistently. Thank you."""

# Characters dictionary
characters = {
    "Main Male Character": "Label name/pronouns/dialogue.",
    
    "Male Character 1|2|3|n": "For each male side character, label their individual name/pronouns/dialogue as Male "
    "Character n. (where n is a consistently assigned number for their character in order of appearance)",
    
    "Main Female Character": "Label name, pronouns, and dialogue.",
    
    "Female Character 1|2|3|n": "For each female side character, label their individual name/pronouns/dialogue as "
    "`Female Character n`. (where n is a consistently assigned number for their character "
    "in order of appearance)",
    
    "Antagonist/Villain": "Only during and after a character's reveal as the antagonist/villain, label their name, "
    "pronouns, and dialogue as 'Antagonist/Villain'.",
    
    "Unknown Role": "Label name and dialogue, if we don't know the role of the character yet. Generally, this person "
    "turns into the antagonist/villain.",
    
    "Groups of People": "Label references to and dialogue from groups of people.",
}

# Plot Elements dictionary
plot_elements = (
    {
        "Danger or Violence": "Label acts of violence, violent verbs/adjectives, any words that indicate or "
        "contribute to a feel of physical/emotional danger",
        
        "Important Information": "Label names of significant places, events, entities.",
        
        "Climax or Resolution": "Label the specific, flashy/pivotal/important story moments that are crucial elements "
        "in the climax or resolution of the story. Do not label the whole sentence(s), "
        "but only the most important contributing snippets.",
        
        "Positive Time Reference": "Label references to a particular time, event, or memory that are positive and "
        "favorably looked remembered/anticipated, (eg: anniversaries, birthdays, etc.)",
        
        "Neutral Time Reference": "Label references to a particular time, event, or memory that are generally "
        "neutral. Always label dates, ages, months, and years.",
        
        "Negative Time Reference": "Label references to a particular time, event, or memory that are remembered "
        "unfavorably or anticipated with dread.",
    },
)

# Descriptions dictionary
descriptions = {
    "Positive Description": "Label adjectives and adverbs that are in a positive context, or describe something "
    "positive/happy in general.",
    
    "Negative Description": "Label creepy/negative/bad adjectives, adverbs, and verbs.",
    
    "Nature Description": "Label all nature-related descriptions. This includes plants, animals, natural phenomena, "
    "forests, ecosystems, and the like.",
    
    "Money and Wealth": "Label references to money, wealth, luxury, opulence. This includes expensive things, places, "
    "services, scenarios. Any specific dollar amount should also be labeled.",
    
    "Water-Related Description": "Label all water body-related descriptions.",
}

#  PROMPT PART 1: RULES AND PLANNING


def generate_label_section(title, labels_dict):
    label_section = f"#### {title}\n"
    for label, description in labels_dict.items():
        label_section += f"- **{label}**: {description}\n"
    return label_section


def generate_user_prompt(story):
    prompt = "Hi! Please help me label my story using the following system:\n\n"
    prompt += "### Labeling Rules for Reddit Stories\n\n"
    prompt += generate_label_section("Characters", characters)
    prompt += generate_label_section("Plot Elements", plot_elements)
    prompt += generate_label_section("Descriptions", descriptions)
    prompt += f"\nPlease plan the labels for the following story:\n\n### Reddit Story\n```\n{story}\n```\n\n"
    prompt += "Initially, let's focus on planning the labels. The execution will be in the next message."
    return prompt


# PROMPT PART 2: EXAMPLES AND LABELING

story_labels = [
    ("Unknown Role", "You are Death, but in a postapocalyptic world."),
    ("Positive Time Reference", "Only a few survivors remain,"),
    ("Positive Description", "and you're doing everything you can to help them"),
    ("Important Detail", "because if the last human dies, you die as well."),
    (
        "Unknown Role",
        "The survivors can't see you, but they feel your presence and noticed your effort.",
    ),
    ("Positive Description", "They started to call you Life."),
    ("Negative Time Reference", "Five thousand left today on all the Earth."),
    (
        "Violence/Danger",
        "I cut the soul of the five thousand and first not one hour ago.",
    ),
]


def generate_labeled_text(story_labels):
    labeled_text = "#### Labeled Sample Text:\n\n"
    for excerpt, label in story_labels:
        labeled_text += f'- **{label}**: "{excerpt}"\n'
    return labeled_text


# TODO: use the models in .models.py to dynamically provide examples for each category of labels.
# pseudocode:
# for category in categories: (ie: characters, plot elements, descriptions)
#     go through each reddit story in the samples, in stories_html.reference.py
#     for each story, read those into the pydantic models in .models.py
#     get stats on label counts for all the stories
#     use the story with the most labels for each category as the example
#     return the example story in the format below:

def generate_follow_up_prompt(story_labels):
    prompt = "Thank you for the planning phase! Now, please proceed to label each line as identified, ensuring thoroughness and precision. Don't blindly highlight everything!\n\n"
    prompt += 'Please use the format `**Label**: "Specific excerpt"`.\n\n'
    prompt += "For example:\n\n```"
    prompt += generate_labeled_text(story_labels)
    prompt += "```\n\n"
    prompt += "\n An accurate and engaging labeling is crucial, as it will be extracted via a script. Consider every line and maintain the formatting consistently. Thank you."
    return prompt

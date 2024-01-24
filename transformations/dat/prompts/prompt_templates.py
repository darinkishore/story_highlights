from transformations.dat.prompts.example_gen import BestExamplePicker
from transformations.dat.prompts.prompt_elements import (
    characters,
    plot_elements,
    descriptions,
)

categories = {
    "Characters": characters,
    "Plot Elements": plot_elements,
    "Descriptions": descriptions,
}

#  PROMPT PART 1: RULES AND PLANNING


def generate_label_section(title, labels_dict):
    label_section = f"#### {title}\n"
    for label, description in labels_dict.items():
        label_section += f"- **{label}**: {description}\n"
    return label_section


def generate_user_prompt(story):
    prompt = "Please plan out how these labeling rules could apply to the reddit story below. Your plan should comprise of 1-3 bullet points per example.\n\n"
    prompt += "### Labeling Rules for Reddit Stories\n\n"
    prompt += generate_label_section("Characters", characters)
    prompt += generate_label_section("Plot Elements", plot_elements)
    prompt += generate_label_section("Descriptions", descriptions)
    prompt += f"\nPlease plan the labels for the following story:\n\n### Reddit Story\n```\n{story}\n```\n\n"
    prompt += "Initially, let's focus on planning the labels. The execution will be in the next message."
    return prompt


# PROMPT PART 2: EXAMPLES AND LABELING


def generate_labeled_text(story_labels):
    labeled_text = "#### Labeled Sample Text:\n\n"
    for excerpt, label in story_labels:
        labeled_text += f'- **{label}**: "{excerpt}"\n'
    return labeled_text


def get_best_example_for_category(category):
    best_example_picker = BestExamplePicker(categories[category])
    markdown_example = best_example_picker.get_markdown_example()
    return markdown_example

def generate_examples_for_all_categories():
    examples = {}
    for category in categories.keys():
        examples[category] = get_best_example_for_category(category)
    return examples


def generate_follow_up_prompt(example, example_labels):
    prompt = "Thank you for the planning phase! Now, please proceed to label each line as identified, ensuring thoroughness and precision. Don't blindly highlight everything!\n\n"
    prompt += 'Please use the format `**Label**: "Specific excerpt"`.\n\n'
    prompt += "For example:\n\n```"
    prompt += f"\n### Reddit Story\n```\n{example}\n```\n\n"
    prompt += "\n#### Labeled Sample Text:\n\n"
    prompt += generate_labeled_text(story_labels)
    prompt += "```\n\n"
    prompt += "\n An accurate and engaging labeling is crucial, as your output will be extracted via exact text matching and put into a TikTok video. Consider every line and maintain the formatting consistently. Thank you."
    return prompt

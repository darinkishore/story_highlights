from transformations.dat.prompts.prompt_templates import story_labels
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
    prompt = "Hi! The following is a series of labels :\n\n"
    prompt += "### Labeling Rules for Reddit Stories\n\n"
    category_prompts = {}
    for category_name, category_labels in categories.items():
        category_prompt = f"### {category_name} Labels\n"
        category_prompt += generate_label_section(category_name, category_labels)
        best_example_picker = BestExamplePicker(category_labels)
        markdown_example = best_example_picker.get_markdown_example()
        category_prompt += f"\n{markdown_example}" if markdown_example else "No example available for this category.\n"
        category_prompts[category_name] = category_prompt

    for category_name, category_prompt in category_prompts.items():
        prompt += f"\n\n---\n\n{category_prompt}"
    prompt += f"\nPlease plan the labels for the categories above using the formatted examples as a guide."
    prompt += "Initially, let's focus on planning the labels. The execution will be in the next message."
    return prompt


# PROMPT PART 2: EXAMPLES AND LABELING


def generate_labeled_text(story_labels):
    labeled_text = "#### Labeled Sample Text:\n\n"
    for excerpt, label in story_labels:
        labeled_text += f'- **{label}**: "{excerpt}"\n'
    return labeled_text


def generate_follow_up_prompt(categories):
    prompt = "Thank you for the planning phase! Now, please proceed to label each line as identified, ensuring thoroughness and precision. Don't blindly highlight everything!\n\n"
    prompt += 'Please use the format `**Label**: "Specific excerpt"`.\n\n'
    for category_name, category_labels in categories.items():
        best_example_picker = BestExamplePicker(category_labels)
        markdown_example = best_example_picker.get_markdown_example()
        prompt += f"### {category_name} Example\n\n"
        prompt += markdown_example if markdown_example else "No example available for this category.\n"
        prompt += "\n---\n\n"
    prompt += "\n An accurate and engaging labeling is crucial, as your output will be extracted via exact text matching and put into a TikTok video. Consider every line and maintain the formatting consistently. Thank you."
    return prompt

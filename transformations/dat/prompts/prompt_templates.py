from transformations.dat.prompts.prompt_templates import story_labels
from transformations.dat.prompts.prompt_elements import (
    characters,
    plot_elements,
    descriptions,
)
from transformations.dat.prompts.example_gen import BestExamplePicker

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
    for category_name, category_labels in categories.items():
        prompt += generate_label_section(category_name, category_labels)
    prompt += "Here are some examples for each category:\n\n"
    for category_name, category_labels in categories.items():
        best_example_picker = BestExamplePicker(category_labels)
        markdown_example = best_example_picker.get_markdown_example()
        if markdown_example:
            prompt += f"#### {category_name} Example\n" + markdown_example + "\n"
    prompt += "\nNow please plan the labels for the following story:\n\n### Reddit Story\n```\n{story}\n```\n\n"
    prompt += "Initially, let's focus on planning the labels. The execution will be in the next message."
    return prompt


# PROMPT PART 2: EXAMPLES AND LABELING


def generate_labeled_text(story_labels):
    labeled_text = "#### Labeled Sample Text:\n\n"
    for excerpt, label in story_labels:
        labeled_text += f'- **{label}**: "{excerpt}"\n'
    return labeled_text


def generate_follow_up_prompt(story):
    prompt = "Thank you for the planning phase! Here are some examples to guide you:\n"
    for category_name, category_labels in categories.items():
        best_example_picker = BestExamplePicker(category_labels)
        markdown_example = best_example_picker.get_markdown_example()
        if markdown_example:
            prompt += f"### {category_name} Example\n{markdown_example}\n"
    prompt += "\nNow, please label the story's sections according to the categories and examples provided. Ensure accuracy and attention to detail."
    prompt += "\n\n### Reddit Story\n```\n{story}\n```\nAn accurate and consistent labeling is crucial for our TikTok video content. Thanks for your contribution!"
    return prompt

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


def generate_category_plan_prompt(story, category_name, category_labels):
    prompt = ""
    prompt += "You are tasked with labeling a reddit story."
    prompt += "Your labels will be used to create a dynamic, engaging TikTok video by mapping them to colors."
    prompt += (
        "Please strive for accuracy (exact textual matching) and engagingness (variety, succinct excerpts) in "
        "your labels."
    )
    prompt += (
        "Please plan out exactly how these labeling rules could apply to the reddit story below. Your plan "
        "should comprise of 1-3 bullet points per example. It'll be your notes for later, "
        "so think carefully!\n\n"
    )
    prompt += "# Labeling Rules for Reddit Stories\n\n"
    prompt += generate_label_section(category_name, category_labels)
    prompt += f"\n\n## Reddit Story\n```\n{story}\n```\n\n"
    prompt += (
        "Please create a plan for labeling the story, for each (applicable) category. Do not label the story "
        "yet--make sure you feel confident that your plan will create an engaging video!"
    )
    return prompt


def gen_all_category_plans(story):
    prompts = {}
    for category_name, category_labels in categories.items():
        prompts[category_name] = generate_category_plan_prompt(
            story, category_name, category_labels
        )
    return prompts


# PROMPT PART 2: EXAMPLES AND LABELING


def get_best_example_for_category(category):
    best_example_picker = BestExamplePicker(categories[category])
    markdown_example = best_example_picker.get_markdown_example()
    return markdown_example


def generate_examples_for_all_categories():
    examples = {}
    for category in categories.keys():
        examples[category] = get_best_example_for_category(category)
    return examples


def generate_follow_up_prompt(category):
    best_example_picker = BestExamplePicker(categories[category])
    example = best_example_picker.get_markdown_example()
    prompt = (
        "Thank you! Now, please proceed to label the reddit story, ensuring thoroughness and precision. Don't "
        "blindly highlight everything!\n\n"
    )
    prompt += (
        'Your labels should be formatted like so: `**Label**: "Specific excerpt"`\n"'
        "A well-done example is provided below: \n\n"
    )
    prompt += "```\n"
    prompt += f"{example}\n"
    prompt += "```\n\n"
    prompt += (
        "Engagingly and accurately labeling excerpts is crucial, as your output will be extracted via exact "
        "text matching, mapped to colors, then put into a TikTok video. Consider every line and use identical "
        "formatting to the example (ie: start your response with `#### Labeled Sections`).  Thank you!"
    )
    return prompt


def gen_all_follow_up_prompts():
    prompts = {}
    for category in categories.keys():
        prompts[category] = generate_follow_up_prompt(category)
    return prompts


def generate_all_prompts(story):
    init_prompts = gen_all_category_plans(story)
    follow_up_prompts = gen_all_follow_up_prompts()
    # link the two by categories
    prompts = {"initial": init_prompts, "follow_up": follow_up_prompts}
    return prompts

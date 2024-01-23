import sglang as sgl
from concurrent.futures import ThreadPoolExecutor
from typing import List
from transformations.dat.models import Highlight, Story, StoryHighlights
from transformations.dat.prompt_templates import (characters, descriptions,
                                                  generate_label_section,
                                                  generate_user_prompt,
                                                  plot_elements)
from transformations.dat.stories_html.reference import stories
from .prompt_templates import characters, plot_elements, descriptions, generate_label_section, system_prompt

@sgl.function
def label_story_with_sglang(s, story_text):
    # Start with the role definition
    s += sgl.system(system_prompt)
    # Include the labeling rules
    s += generate_user_prompt(story_text)
    # Instruct the AI to plan the labels for the story
    for category, labels_dict in categories:
        s += generate_label_section(category, labels_dict)
    # Include the labeling format instructions
    s += user_follow_up_prompt
    # Integrate the execution phase with dynamically generated examples
    # (Placeholder for dynamic example generation logic)
    example_story, example_labels = find_best_example(characters)  # Example for characters category
    s += generate_follow_up_prompt(example_story, example_labels)
    # Emphasize the importance of accuracy
    s += "\nPlease ensure accuracy as the output will be used in a TikTok video.\n"

    # Define the categories and their corresponding label dictionaries
    categories = [("Characters", characters), ("Plot Elements", plot_elements), ("Descriptions", descriptions)]

    # Forking to handle multiple categories in parallel
    forks = s.fork(len(categories))

    # Dynamically select the best examples for each category
    for f, (category, labels_dict) in zip(forks, categories):
        f += f"Now, plan the labels for the category: {category}.\n"
        f += generate_label_section(category, labels_dict) + "\n"
        f += sgl.gen(f"plan_{category.lower()}", max_tokens=256)

    # Generate the labels for the story text
    s += f"Now, label the following story:\n\n### Reddit Story\n```\n{story_text}\n```\n\n"
    s += f"Now, label the following story:\n\n### Reddit Story\n```\n{story_text}\n```\n\n"
    s += sgl.gen("labeled_story", max_tokens=1024)
    
    # Process the labeled story and apply HTML formatting
    labeled_story = s["labeled_story"]
    story_highlights = StoryHighlights.process_story_highlights(labeled_story, story_text)
    html_formatted_story = story_highlights.apply_html_highlights_to_story()
    
    # Return the HTML formatted story
    return html_formatted_story



def find_best_example(category_labels: dict) -> (str, List[Highlight]):
        best_story = None
        best_highlights = []
        max_label_count = 0
        for story_data in stories:
            story_highlights = StoryHighlights.process_story_highlights(story_data['highlights'], story_data['story'], story_data['title'])
            label_count = sum(highlight.label in category_labels for highlight in story_highlights.highlights)
            if label_count > max_label_count:
                max_label_count = label_count
                best_story = story_data['story']
                best_highlights = story_highlights.highlights
        return best_story, best_highlights



# def generate_dynamic_prompts(story_text: str, story_title: str = "Story Title") -> str:
#     def generate_plan(category_name: str, category_labels: dict) -> str:


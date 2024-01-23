import sglang as sgl
from concurrent.futures import ThreadPoolExecutor
from typing import List
from transformations.dat.models import Highlight, Story, StoryHighlights
from transformations.dat.prompt_templates import (characters, descriptions,
                                                  generate_label_section,
                                                  generate_user_prompt,
                                                  plot_elements)
from transformations.dat.stories_html.reference import stories
from .prompt_templates import characters, plot_elements, descriptions, generate_label_section, system_prompt, user_follow_up_prompt, generate_follow_up_prompt

@sgl.function
def label_story_with_sglang(s, story_text):
    s += sgl.system(system_prompt)  # Include the system prompt

    # Define the categories and their corresponding label dictionaries
    categories = [("Characters", characters), ("Plot Elements", plot_elements), ("Descriptions", descriptions)]

    # Start with the planning phase
    s += generate_user_prompt(story_text)
    
    # Dynamically select the best examples for each category
    best_examples = {category: find_best_example(labels_dict) for category, labels_dict in categories}
    
    # Include the execution phase with examples
    example_story, example_labels = best_examples["Characters"]  # Assuming Characters as the default example
    s += generate_follow_up_prompt(example_story, example_labels)
    
    # Emphasize the importance of accuracy
    s += "\nYour detailed and accurate labeling is crucial, as it will be extracted via a script for a TikTok video.\n"



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


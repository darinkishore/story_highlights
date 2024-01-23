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
    s += sgl.system(system_prompt)  # Include the system prompt

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
    s += sgl.gen("labeled_story", max_tokens=1024)
    
    labeled_story = s["labeled_story"]
    story_highlights = StoryHighlights.process_story_highlights(labeled_story, story_text)
    html_formatted_story = story_highlights.apply_html_highlights_to_story()

    # Include the specific output format
    s += "Please use the format `**Label**: \"Specific excerpt\"`.\n\n"

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
#         return generate_label_section(category_name, category_labels)

    

    # def render_highlights_to_html(story: str, highlights: List[Highlight]) -> str:
    #     story_highlights = StoryHighlights(story=Story(title=story_title, story=story), highlights=highlights)
    #     return story_highlights.apply_html_highlights_to_story()

    # with ThreadPoolExecutor() as executor:
    #     plans = list(executor.map(generate_plan, ["Characters", "Plot Elements", "Descriptions"], [characters, plot_elements, descriptions]))
    #     examples = list(executor.map(find_best_example, [characters, plot_elements, descriptions]))

    # prompts = [generate_user_prompt(story_text)]
    # prompts.extend(plans)
    # for example, example_labels in examples:
    #     prompts.append(render_highlights_to_html(example, example_labels))

    # return "\n\n".join(prompts)


# TODO: get rid of planning stage. intelligently managing examples and instructions should do it.


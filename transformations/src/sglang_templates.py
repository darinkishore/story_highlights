from concurrent.futures import ThreadPoolExecutor
from typing import List

from transformations.dat.models import Highlight, Story, StoryHighlights
from transformations.dat.prompt_templates import (characters, descriptions,
                                                  generate_label_section,
                                                  generate_user_prompt,
                                                  plot_elements)
from transformations.dat.stories_html.reference import stories


def generate_dynamic_prompts(story_text: str, story_title: str = "Story Title") -> str:
    def generate_plan(category_name: str, category_labels: dict) -> str:
        return generate_label_section(category_name, category_labels)

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

    def render_highlights_to_html(story: str, highlights: List[Highlight]) -> str:
        story_highlights = StoryHighlights(story=Story(title=story_title, story=story), highlights=highlights)
        return story_highlights.apply_html_highlights_to_story()

    with ThreadPoolExecutor() as executor:
        plans = list(executor.map(generate_plan, ["Characters", "Plot Elements", "Descriptions"], [characters, plot_elements, descriptions]))
        examples = list(executor.map(find_best_example, [characters, plot_elements, descriptions]))

    prompts = [generate_user_prompt(story_text)]
    prompts.extend(plans)
    for example, example_labels in examples:
        prompts.append(render_highlights_to_html(example, example_labels))

    return "\n\n".join(prompts)

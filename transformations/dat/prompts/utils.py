from pprint import pprint

from transformations.dat.prompts.prompt_templates import (
    generate_labeled_text,
)
from transformations.dat.reference_stories.reference import reference_stories
from transformations.dat.models import StoryHighlights
from prompt_templates import categories
import rich


"""
BestExamplePicker Usage:
Pick a category from the categories dictionary

`for category in categories.keys():`
- Be careful! Make sure you access the dict via categories[category]

Then, initialize the class, 
`BestExamplePicker(categories[category])`

and then call the `get_markdown_example` method
`best_example_picker.get_markdown_example()`

ex: 
for category in categories.keys():
    best_example_picker = BestExamplePicker(categories[category])
    markdown_example = best_example_picker.get_markdown_example()
    if markdown_example:
        print(markdown_example)
    else:
        print("No markdown example found")
    
"""


class BestExamplePicker:
    """
    For each category passed to BestExamplePicker,
    It will go through each story and count the number of highlights that have the category label
    It will then return the story with the most highlights for that category
    """

    def __init__(self, category):
        self.category = category
        self.stories = [StoryHighlights(story=story[0]) for story in reference_stories]
        for i, story in enumerate(self.stories):
            story.add_highlights(reference_stories[i][1])
        self.markdown_example = self.get_markdown_example()

    def update_label_counts(self):
        label_counts = {}
        for story_highlight in self.stories:
            for highlight in story_highlight.highlights:
                if highlight.label in self.category:
                    label_counts[story_highlight.story.title] = (
                        label_counts.get(story_highlight.story.title, 0) + 1
                    )
        return label_counts

    def get_best_story(self, label_counts):
        top = 0
        max_story = None
        for key in label_counts.keys():
            if label_counts[key] > top:
                top = label_counts[key]
                max_story = key
        best_story_title = max_story
        return best_story_title

    def get_best_story_for_category(self):
        label_counts = self.update_label_counts()
        return self.get_best_story(label_counts)

    def get_markdown_example(self):
        best_story_title = self.get_best_story_for_category()
        for story in self.stories:
            if story.story.title == best_story_title:
                # Filter labels by category
                filtered_highlights = [
                    highlight
                    for highlight in story.highlights
                    if highlight.label in self.category
                ]
                # Make a new story highlights object
                new_story = StoryHighlights(
                    story=story.story, highlights=filtered_highlights
                )
                return str(new_story)
        return None


# debug prints
def print_story_details(category, story, story_label_counts, best_story):
    print("\n----------------")
    print(f"Category: {category}")
    print(f"Story: {story[:20]}")
    print(f"Label counts: {story_label_counts[story]}")
    print(f"Best Story for this category: {best_story}")
    print("----------------\n")


for category in categories.keys():
    best_example_picker = BestExamplePicker(categories[category])
    story_label_counts = best_example_picker.get_markdown_example()
    rich.print(best_example_picker.markdown_example)

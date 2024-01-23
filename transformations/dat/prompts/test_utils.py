import pytest
from transformations.dat.prompts.prompt_templates import (
    characters,
    plot_elements,
    descriptions,
)
from transformations.dat.prompts.utils import BestExamplePicker
from transformations.dat.reference_stories.reference import reference_stories
from transformations.dat.models import Story, StoryHighlights

# verify that the best story is being selected for each category


# @pytest.fixture
# def best_examples():
#     story_models = [StoryHighlights(story=Story(story=story[0]), highlights=story[1]).process_story_highlights() for story in reference_stories]
#     for story in story_models:
#         # compute the label counts for each story
#         label_counts = {}
#         for label in story.labels:
#             label_counts[label] = label_counts.get(label, 0) + 1
#     # each category has certain labels.
#     characters_label_counts = {label: label_counts[label] for label in characters}
#     plot_elements_label_counts = {label: label_counts[label] for label in plot_elements}
#     descriptions_label_counts = {label: label_counts[label] for label in descriptions}

#     # sum the total number of labels for each category
#     characters_total_labels_per_story = sum(characters_label_counts.values())
#     plot_elements_total_labels_per_story = sum(plot_elements_label_counts.values())
#     descriptions_total_labels_per_story = sum(descriptions_label_counts.values())

#     # TODO: fix so this isn't shit.
#     assert False

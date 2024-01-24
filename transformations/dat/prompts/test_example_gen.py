import pytest
from transformations.dat.prompts.prompt_templates import categories
from .example_gen import BestExamplePicker
from transformations.dat.reference_stories.reference import reference_stories
from transformations.dat.models import Story, StoryHighlights
from bs4 import BeautifulSoup

# test to see if all the individual best examples can be merged into one story and html highlighted


def test_merged_best_examples():
    for story in reference_stories:
        # find the one that has the word "harry" in story[0]
        if "Harry" in story[0]:
            gold_std = StoryHighlights(story=story[0])
            gold_std.add_highlights(story[1])

    category_examples = []
    for category in categories:
        best_example_picker = BestExamplePicker(categories[category])
        markdown_example = best_example_picker.get_markdown_example()
        if markdown_example:
            category_examples.append(markdown_example)

    combined_highlights = []
    for example in category_examples:
        combined_highlights += example.highlights

    possible_missing_list = []
    for highlight in gold_std.highlights:
        if highlight not in combined_highlights:
            possible_missing_list.append(highlight)
    assert (
        not possible_missing_list
    ), f"Highlights not found in combined highlights: {possible_missing_list}"

    merged_markdown = '\n\n'.join(category_examples)   # Combine all category markdown examples

    # Convert gold standard highlights to markdown for comparison
    gold_std_markdown = '\n'.join([str(highlight) for highlight in gold_std.highlights])
    # Validating that the merged markdown is equal to the gold standard
    assert merged_markdown == gold_std_markdown, "Markdown does not match"

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
        filtered_story = best_example_picker.get_story_model_example()
        if filtered_story:
            category_examples.append(filtered_story)

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

    gold_std.apply_html_highlights()
    merged_example = StoryHighlights(
        story=gold_std.story, highlights=combined_highlights
    )
    merged_example.apply_html_highlights()

    soup1 = BeautifulSoup(gold_std.html_story, "html.parser")
    soup2 = BeautifulSoup(merged_example.html_story, "html.parser")
    assert str(soup1) == str(soup2), "HTML does not match"

from transformations.dat.models import Highlight

def test_tiebreaking_logic():
    # Create a mock story with overlapping highlights
    mock_story = 'The quick brown fox jumps over the lazy dog.'
    mock_highlights = [
        Highlight(label='Descriptions', excerpt='quick brown fox'),
        Highlight(label='Plot Elements', excerpt='quick brown'),
        Highlight(label='Characters', excerpt='brown fox')
    ]

    # Instantiate StoryHighlights with mock data
    story_highlights = StoryHighlights(story=Story(story=mock_story), highlights=mock_highlights)

    # Apply the highlights with the tiebreaking logic
    story_highlights.apply_html_highlights()

    # Verify that the correct highlight is applied based on priority
    soup = BeautifulSoup(story_highlights.html_story, 'html.parser')
    expected_html = '<span style="color:#CharactersColor;">brown fox</span>'
    assert expected_html in str(soup), 'Tiebreaking logic failed'

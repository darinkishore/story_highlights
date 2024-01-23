import pytest
from transformations.dat.models import Highlight, StoryHighlights, Story, re
from transformations.dat.stories_html.reference import reference_stories
from transformations.dat.label_statistics import get_label_statistics
from transformations.dat.colors import get_color_mapping  # Import the function


@pytest.mark.parametrize("story_text, markdown_text", reference_stories)
def test_story_model_instantiation(story_text, markdown_text):
    story = Story(title="Test Story", story=story_text)
    assert story.title == "Test Story"
    assert story.story == story_text


@pytest.mark.parametrize("story_text, markdown_text", reference_stories)
def test_label_model_instantiation(story_text, markdown_text):
    label_pattern = re.compile(r'- \*\*(.*?)\*\*: "(.*?)"(?=\s|$)')
    for match in label_pattern.finditer(markdown_text):
        label_text, excerpt_text = match.groups()
        label = Highlight(label=label_text, excerpt=excerpt_text)
        assert label.label == label_text
        assert label.excerpt == excerpt_text


@pytest.mark.parametrize("story_text, markdown_text", reference_stories)
def test_labeled_story_from_markdown(story_text, markdown_text):
    labeled_story = StoryHighlights.process_story_highlights(markdown_text, story_text)
    assert labeled_story.story.story == story_text
    assert len(labeled_story.highlights) == len(
        list(re.finditer(r'- \*\*(.*?)\*\*: "(.*?)"(?=\s|$)', markdown_text))
    )


@pytest.mark.parametrize("story_text, markdown_text", reference_stories)
def test_get_label_statistics(story_text, markdown_text):
    label_stats = get_label_statistics(markdown_text)
    assert isinstance(label_stats, dict), "The result should be a dictionary."
    # Example assertion for specific label statistics
    if label_stats: # Check if not empty
        max_count_label = max(label_stats.items(), key=lambda x: x[1]['count'])
        assert max_count_label[1]['count'] > 0, "The max count label should have a count greater than 0."
        assert isinstance(max_count_label[1]['example_story'], str), "The example story should be a string."

    # Ensure that all labels have the 'count' key
    for label, stats in label_stats.items():
        assert 'count' in stats, f"The stats for label '{label}' must have a 'count' field."
        assert isinstance(stats['count'], int), f"The count for label '{label}' must be an integer."

    # Handling edge case when no labels are present
    if not markdown_text.strip():
        assert not label_stats, "Label statistics should be empty if there are no labels."

@pytest.mark.parametrize("story_text, markdown_text", reference_stories)
def test_apply_html_tags(story_text, markdown_text):
    labeled_story = StoryHighlights.process_story_highlights(markdown_text, story_text)
    html_story = labeled_story.apply_html_highlights_to_story()
    for label in labeled_story.highlights:
        color = get_color_mapping(label.label)  # Use the function to get the color
        assert f'<span style="color:{color};">{label.excerpt}</span>' in html_story

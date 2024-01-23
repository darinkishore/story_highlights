import pytest
from transformations.dat.models import Highlight, StoryHighlights, Story, re
from transformations.dat.stories_html.reference import reference_stories
from transformations.dat.colors import get_color_mapping  # Import the function


@pytest.mark.parametrize("story_text, raw_highlights", reference_stories)
def test_story_model_instantiation(story_text, raw_highlights):
    story = Story(title="Test Story", story=story_text)
    assert story.title == "Test Story"
    assert story.story == story_text


@pytest.mark.parametrize("story_text, raw_highlights", reference_stories)
def test_label_model_instantiation(story_text, raw_highlights):
    label_pattern = re.compile(r'- \*\*(.*?)\*\*: "(.*?)"(?=\s|$)')
    for match in label_pattern.finditer(raw_highlights):
        label_text, excerpt_text = match.groups()
        label = Highlight(label=label_text, excerpt=excerpt_text)
        assert label.label == label_text
        assert label.excerpt == excerpt_text


@pytest.mark.parametrize("story_text, raw_highlights", reference_stories)
def test_num_labels_accurate(story_text, raw_highlights):
    # makes sure no labels are missed
    num_highlights = len(re.findall(r"^- ", raw_highlights, re.MULTILINE))
    story_highlights = StoryHighlights.process_story_highlights(
        raw_highlights, story_text
    )
    assert len(story_highlights.highlights) == num_highlights


@pytest.mark.parametrize("story_text, markdown_text", reference_stories)
def process_story_highlights_test(story_text, raw_highlights):
    labeled_story = StoryHighlights.process_story_highlights(raw_highlights, story_text)
    assert labeled_story.story.story == story_text
    assert len(labeled_story.highlights) == len(
        list(re.finditer(r'- \*\*(.*?)\*\*: "(.*?)"(?=\s|$)', raw_highlights))
    )


@pytest.mark.parametrize("story_text, raw_highlights", reference_stories)
def test_apply_html_tags(story_text, raw_highlights):
    labeled_story = StoryHighlights.process_story_highlights(raw_highlights, story_text)
    html_story = labeled_story.apply_html_highlights_to_story()
    for label in labeled_story.highlights:
        color = get_color_mapping(label.label)  # Use the function to get the color
        assert f'<span style="color:{color};">{label.excerpt}</span>' in html_story

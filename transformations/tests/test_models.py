import pytest
from transformations.dat.colors import get_color_mapping
from transformations.dat.models import Highlight, Story, StoryHighlights, re
from transformations.dat.stories_html.reference import reference_stories


@pytest.mark.parametrize("story_text, markdown_text", reference_stories)
def test_story_model_instantiation(story_text, markdown_text):
    story = Story(title="Test Story", story=story_text)
    assert story.title == "Test Story"
    assert story.story == story_text

@pytest.mark.parametrize("story_text, markdown_text", reference_stories)
def test_highlight_model_instantiation(story_text, markdown_text):
    label_pattern = re.compile(r'- \*\*(.*?)\*\*: "(.*?)"(?=\s|$)')
    for match in label_pattern.finditer(markdown_text):
        label_text, excerpt_text = match.groups()
        highlight = Highlight(label=label_text, excerpt=excerpt_text)
        assert highlight.label == label_text
        assert highlight.excerpt == excerpt_text
        assert highlight.color is None or isinstance(highlight.color, str)

@pytest.mark.parametrize("story_text, markdown_text", reference_stories)
def test_process_story_highlights(story_text, markdown_text):
    story_highlights = StoryHighlights.process_story_highlights(markdown_text, story_text)
    assert story_highlights.story.story == story_text
    assert len(story_highlights.highlights) == len(list(label_pattern.finditer(markdown_text)))
    for highlight in story_highlights.highlights:
        assert isinstance(highlight, Highlight)

@pytest.mark.parametrize("story_text, markdown_text", reference_stories)
def test_apply_html_highlights_to_story(story_text, markdown_text):
    story_highlights = StoryHighlights.process_story_highlights(markdown_text, story_text)
    html_story = story_highlights.apply_html_highlights_to_story()
    for highlight in story_highlights.highlights:
        color = get_color_mapping(highlight.label)
        expected_html_tag = f'<span style="color:{color};">{highlight.excerpt}</span>'
        assert expected_html_tag in html_story

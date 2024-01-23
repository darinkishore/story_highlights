
import pytest
from transformations.dat.models import Label, LabeledStory, Story, re
from transformations.dat.stories_html.reference import reference_stories
from transformations.dat.colors import color_mappings


@pytest.fixture(scope="module")
def color_mapping():
    return color_mappings
    
    
    
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
        label = Label(label=label_text, excerpt=excerpt_text)
        assert label.label == label_text
        assert label.excerpt == excerpt_text

@pytest.mark.parametrize("story_text, markdown_text", reference_stories)
def test_labeled_story_from_markdown(story_text, markdown_text):
    labeled_story = LabeledStory.from_markdown(markdown_text, story_text)
    assert labeled_story.story.story == story_text
    assert len(labeled_story.labels) == len(list(re.finditer(r'- \*\*(.*?)\*\*: "(.*?)"(?=\s|$)', markdown_text)))

@pytest.mark.parametrize("story_text, markdown_text", reference_stories)
def test_apply_html_tags(story_text, markdown_text, color_mapping):
    labeled_story = LabeledStory.from_markdown(markdown_text, story_text)
    html_story = labeled_story.apply_html_tags(color_mapping)
    for label in labeled_story.labels:
        assert f'<span style="color:{color_mapping[label.label]};">{label.excerpt}</span>' in html_story

@pytest.mark.parametrize("story_text, markdown_text", reference_stories)
def test_apply_html_tags_invalid_label(story_text, markdown_text, color_mapping):
    labeled_story = LabeledStory.from_markdown(markdown_text, story_text)
    incomplete_color_mapping = color_mapping.copy()
    incomplete_color_mapping.popitem()
    with pytest.raises(KeyError):
        labeled_story.apply_html_tags(incomplete_color_mapping)
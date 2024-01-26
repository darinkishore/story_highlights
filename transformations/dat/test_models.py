import pytest
from transformations.dat.models import Highlight, StoryHighlights, Story, re
from transformations.dat.reference_stories.reference import reference_stories
from transformations.dat.colors import get_color_mapping
from transformations.dat.prompts.prompt_elements import characters, plot_elements, descriptions  # Import tiebreaking dictionaries


@pytest.mark.parametrize("story_text, raw_highlights", reference_stories)
def test_story_model_instantiation(story_text, raw_highlights):
    story = Story(story=story_text)
    assert story is not None


@pytest.mark.parametrize("story_text, raw_highlights", reference_stories)
def test_story_title_is_first_line(story_text, raw_highlights):
    story = Story(story=story_text)
    assert story_text.strip().split("\n")[0] == story.title


@pytest.mark.parametrize("story_text, raw_highlights", reference_stories)
def test_story_title_removed_from_story(story_text, raw_highlights):
    story = Story(story=story_text)
    assert story.title not in story.story


@pytest.mark.parametrize("story_text, raw_highlights", reference_stories)
def test_story_is_not_empty(story_text, raw_highlights):
    story = Story(story=story_text)
    assert story.story != ""


@pytest.mark.parametrize("story_text, raw_highlights", reference_stories)
def test_total_story_length_is_same(story_text, raw_highlights):
    story = Story(story=story_text)
    abs_diff = 4
    assert (
        abs(
            len(story_text.strip())
            - (len(story.title.strip()) + len(story.story.strip()))
        )
        <= abs_diff
    )


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
    nice = StoryHighlights(story=story_text)
    nice.add_highlights(raw_highlights)
    assert len(nice.highlights) == num_highlights


@pytest.mark.parametrize("story_text, raw_highlights", reference_stories)
def test_highlight_model_instantiation(story_text, raw_highlights):
    label_pattern = re.compile(r'- \*\*(.*?)\*\*: "(.*?)"(?=\s|$)')
    for match in label_pattern.finditer(raw_highlights):
        label_text, excerpt_text = match.groups()
        highlight = Highlight(label=label_text, excerpt=excerpt_text)
        assert highlight.label == label_text
        assert highlight.excerpt == excerpt_text
        assert highlight.color is None or isinstance(highlight.color, str)


@pytest.mark.parametrize("story_text, markdown_text", reference_stories)
def process_story_highlights_test(story_text, raw_highlights):
    labeled_story = StoryHighlights.add_highlights(raw_highlights, story_text)
    assert labeled_story.story.story == story_text
    assert len(labeled_story.highlights) == len(
        list(re.finditer(r'- \*\*(.*?)\*\*: "(.*?)"(?=\s|$)', raw_highlights))
    )


@pytest.mark.parametrize("story_text, raw_highlights", reference_stories)
def test_apply_html_tags(story_text, raw_highlights):
    nice = StoryHighlights(story=story_text)
    nice.add_highlights(raw_highlights)
    nice.apply_html_highlights()

    for label in nice.highlights:
        color = get_color_mapping(label.label)  # Use the function to get the color
        assert f'<span style="color:{color};">{label.excerpt}</span>' in nice.html_story

@pytest.mark.parametrize(
    "story_text, raw_highlights, expected_overrides",
    [
        (
            'Story with simple override',
            '- **descriptions**: "The sky"\n- **plot_elements**: "The sky was clear"\n- **characters**: "Alice looked at the sky"',
            [("The sky", "characters")]
        ),
        (
            'Story with Levenshtein rule',
            '- **charcters**: "Bob looked at the stars"\n- **plot_elemnts**: "The stars in the night"',
            [("Bob looked at the stars", "characters"), ("The stars in the night", "plot_elements")]
        )
        # Add more test cases if needed.
    ]
)
def test_tiebreaking_logic(story_text, raw_highlights, expected_overrides):
    story_highlights = StoryHighlights(story=story_text)
    story_highlights.add_highlights(raw_highlights)
    story_highlights.apply_html_highlights()

    for excerpt, expected_label in expected_overrides:
        actual_highlight = next((hl for hl in story_highlights.highlights if hl.excerpt == excerpt), None)
        assert actual_highlight is not None, f'Expected highlight "{excerpt}" not found'
        assert actual_highlight.label == expected_label, f'For highlight "{excerpt}", expected "{expected_label}", but found "{actual_highlight.label}"'

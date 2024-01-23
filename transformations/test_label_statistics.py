import pytest
from transformations.dat.label_statistics import get_label_statistics
from transformations.dat.models import StoryHighlights
from transformations.dat.stories_html.reference import reference_stories


@pytest.mark.parametrize("story_text, labeled_sections", reference_stories)
def test_get_label_statistics_with_reference_stories(story_text, labeled_sections):
    story_highlights = StoryHighlights.process_story_highlights(
        raw_highlight_response=labeled_sections,
        story_text=story_text
    )
    label_stats = get_label_statistics()
    expected_label_counts = {}
    for highlight in story_highlights.highlights:
        label = highlight.label
        if label not in expected_label_counts:
            expected_label_counts[label] = 1
        else:
            expected_label_counts[label] += 1
    for label, count in expected_label_counts.items():
        assert label in label_stats
        assert label_stats[label]['count'] == count
        assert label_stats[label]['example_story'] == story_text

def test_get_label_statistics_with_no_labels():
    reference_stories_empty = [("", "")]
    with pytest.raises(ValueError):
        get_label_statistics()

def test_get_label_statistics_with_uniform_labels():
    uniform_label_story = "This is a test story with uniform labels."
    uniform_labeled_sections = "#### Labeled Sections\n\n" + "- **Test Label**: \"This is a test excerpt.\"" * 5
    reference_stories_uniform = [(uniform_label_story, uniform_labeled_sections)]
    label_stats = get_label_statistics()
    assert "Test Label" in label_stats
    assert label_stats["Test Label"]['count'] == 5
    assert label_stats["Test Label"]['example_story'] == uniform_label_story

def test_get_label_statistics_with_varying_label_counts():
    varying_label_story = "This story has varying counts of labels."
    varying_labeled_sections = (
        "#### Labeled Sections\n\n"
        "- **Label One**: \"First excerpt.\"\n"
        "- **Label Two**: \"Second excerpt.\"\n"
        "- **Label One**: \"Third excerpt.\"\n"
    )
    reference_stories_varying = [(varying_label_story, varying_labeled_sections)]
    label_stats = get_label_statistics()
    assert "Label One" in label_stats
    assert "Label Two" in label_stats
    assert label_stats["Label One"]['count'] == 2
    assert label_stats["Label Two"]['count'] == 1
    assert label_stats["Label One"]['example_story'] == varying_label_story
    assert label_stats["Label Two"]['example_story'] == varying_label_story

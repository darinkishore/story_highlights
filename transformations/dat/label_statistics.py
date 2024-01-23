from transformations.dat.models import StoryHighlights
from transformations.dat.stories_html.reference import reference_stories


def get_label_statistics():
    label_stats = {}

    for story_text, labeled_sections in reference_stories:
        story_highlights = StoryHighlights.process_story_highlights(
            raw_highlight_response=labeled_sections,
            story_text=story_text
        )

        for highlight in story_highlights.highlights:
            label = highlight.label
            if label not in label_stats:
                label_stats[label] = {'count': 0, 'example_story': story_text}
            label_stats[label]['count'] += 1
            if label_stats[label]['count'] > label_stats[label]['example_story']['count']:
                label_stats[label]['example_story'] = story_text

    return label_stats

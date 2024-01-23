from transformations.dat.prompt_templates import (
    characters,
    plot_elements,
    descriptions,
    generate_labeled_text,
)
from transformations.dat.reference_stories.reference import reference_stories
from transformations.dat.models import Story, StoryHighlights

class BestExamplePicker:
    def __init__(self, category):
        self.category = category
        self.reference_stories = reference_stories

    def update_label_counts(self, category):
        label_counts = {}
        story_model = None
        for reference_story in self.reference_stories:
            story_model = Story(
                title=reference_story["title"], story=reference_story["story"]
            )
            story_highlights = StoryHighlights(
                story=story_model, highlights=reference_story["highlights"]
            )
            for highlight in story_highlights.highlights:
                if highlight.label in category:
                    label_counts[story_model.title] = (
                        label_counts.get(story_model.title, 0) + 1
                    )
        return label_counts

    def get_best_story(self, label_counts):
        best_story_title = max(label_counts, key=label_counts.get)
        best_story_data = next(
            item for item in self.reference_stories if item["title"] == best_story_title
        )
        best_story_model = Story(
            title=best_story_data["title"], story=best_story_data["story"]
        )
        return StoryHighlights(
            story=best_story_model, highlights=best_story_data["highlights"]
        )

    def format_story_highlights(self, category, story_highlights):
        story_highlights.apply_html_highlights_to_story()
        example_formatted = generate_labeled_text(story_highlights.highlights)
        return f"\n\n### Example for {category} Labels:\n" + example_formatted

    def get_best_story_for_category(self, category):
        label_counts = self.update_label_counts(category)
        return self.get_best_story(label_counts)
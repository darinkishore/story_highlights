import unittest

from transformations.dat.colors import get_color_mapping
from transformations.dat.models import StoryHighlights
from transformations.dat.prompts.prompt_elements import (characters,
                                                         descriptions,
                                                         plot_elements)


class TestTiebreakingLogic(unittest.TestCase):

    def test_tiebreaking_priority(self):
        story_text = "John, the main male character, encountered a dangerous situation."
        highlights = [
            {"label": "Main Male Character", "excerpt": "John"},
            {"label": "Danger/Violence", "excerpt": "dangerous situation"}
        ]
        story_highlights = StoryHighlights(story=story_text, highlights=highlights)
        story_highlights.apply_html_highlights()
        self.assertIn('<span style="color:#1155cc;">John</span>', story_highlights.html_story)
        self.assertIn('<span style="color:#ff0000;">dangerous situation</span>', story_highlights.html_story)

    def test_tiebreaking_levenshtein_distance(self):
        story_text = "The antagonist caused a violent outbreak."
        highlights = [
            {"label": "Antagonist/Villain", "excerpt": "antagonist"},
            {"label": "Danger or Violence", "excerpt": "violent outbreak"}
        ]
        story_highlights = StoryHighlights(story=story_text, highlights=highlights)
        story_highlights.apply_html_highlights()
        self.assertIn('<span style="color:#ff0000;">antagonist</span>', story_highlights.html_story)
        self.assertIn('<span style="color:#ff0000;">violent outbreak</span>', story_highlights.html_story)

if __name__ == '__main__':
    unittest.main()

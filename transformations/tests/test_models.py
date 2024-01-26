from django.test import TestCase
from transformations.models import (HighlightModel, StoryHighlightsModel,
                                    StoryModel)


class StoryModelTests(TestCase):
    def test_create_and_retrieve_story(self):
        story = StoryModel(title="Test Title", story="Once upon a time...")
        story.save()
        retrieved_story = StoryModel.objects.get(id=story.id)
        self.assertEqual(retrieved_story.title, "Test Title")
        self.assertEqual(retrieved_story.story, "Once upon a time...")

class HighlightModelTests(TestCase):
    def test_create_and_retrieve_highlight(self):
        highlight = HighlightModel(label="Important", excerpt="An important part of the text", color="#FF0000")
        highlight.save()
        retrieved_highlight = HighlightModel.objects.get(id=highlight.id)
        self.assertEqual(retrieved_highlight.label, "Important")
        self.assertEqual(retrieved_highlight.excerpt, "An important part of the text")
        self.assertEqual(retrieved_highlight.color, "#FF0000")

class StoryHighlightsModelTests(TestCase):
    def test_create_and_retrieve_story_highlights(self):
        story = StoryModel(title="Test Title", story="Once upon a time...")
        story.save()
        highlight = HighlightModel(label="Important", excerpt="An important part of the text")
        highlight.save()
        story_highlights = StoryHighlightsModel(story=story)
        story_highlights.save()
        story_highlights.highlights.add(highlight)
        retrieved_story_highlights = StoryHighlightsModel.objects.get(id=story_highlights.id)
        self.assertEqual(retrieved_story_highlights.story, story)
        self.assertIn(highlight, retrieved_story_highlights.highlights.all())

    def test_save_highlights(self):
        # Assuming save_highlights method is implemented to save raw_highlight_response
        story = StoryModel(title="Test Title", story="Once upon a time...")
        story.save()
        story_highlights = StoryHighlightsModel(story=story)
        story_highlights.save()
        raw_highlight_response = "- **Important**: \"An important part of the text\""
        story_highlights.save_highlights(raw_highlight_response)
        self.assertEqual(story_highlights.highlights.count(), 1)
        self.assertEqual(story_highlights.highlights.first().label, "Important")
        self.assertEqual(story_highlights.highlights.first().excerpt, "An important part of the text")

    def test_apply_html_highlights(self):
        # Assuming apply_html_highlights method is implemented to save html_story
        story = StoryModel(title="Test Title", story="Once upon a time...")
        story.save()
        story_highlights = StoryHighlightsModel(story=story)
        story_highlights.save()
        story_highlights.apply_html_highlights()
        self.assertIsNotNone(story_highlights.html_story)
        self.assertIn('<span style="color:', story_highlights.html_story)

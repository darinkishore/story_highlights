from django.db import models


class StoryModel(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    story = models.TextField()

    def __str__(self):
        return f'{self.title or "Untitled Story"} - {self.story[:50]}...'


class HighlightModel(models.Model):
    label = models.CharField(max_length=200)
    excerpt = models.TextField()
    color = models.CharField(max_length=7, null=True, blank=True)

    def __str__(self):
        return f'- **{self.label}**: "{self.excerpt[:50]}..."'


class StoryHighlightsModel(models.Model):
    story = models.ForeignKey(StoryModel, on_delete=models.CASCADE)
    highlights = models.ManyToManyField(HighlightModel)
    html_story = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.story.title or "Untitled Story"} - Highlights'

    def save_highlights(self, raw_highlight_response):
        # TODO: Implement this method
        pass

    def apply_html_highlights(self):
        # TODO: Implement this method
        pass

# Create your models here.

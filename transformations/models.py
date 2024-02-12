from django.db import models
from django.utils.text import slugify


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


class Story(models.Model):
    title = models.TextField()
    body = models.TextField()
    raw_text = models.TextField()

    is_edited = models.BooleanField(default=False)
    is_highlighted = models.BooleanField(default=False)

    highlights = models.TextField()
    edited_story = models.TextField()  # text
    highlighted_story = models.TextField()  # html

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    url = models.URLField()

    def save(self, *args, **kwargs):
        if not self.id:  # If the story is being created
            self.slug = slugify(self.title)  # Generate a slug based on the title
        super(Story, self).save(*args, **kwargs)  # Call the "real" save() method.

from django.db import models
from django.utils.html import format_html


class Story(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    story = models.TextField()

    def __str__(self):
        return self.title if self.title else 'Untitled'


class Highlight(models.Model):
    label = models.CharField(max_length=255)
    excerpt = models.TextField()
    color = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        color_style = f'style="color: {self.color};"' if self.color else ''
        return format_html('<span {}>{{}}</span>', color_style, self.label)


class StoryHighlights(models.Model):
    story = models.ForeignKey(Story, related_name='story_highlights', on_delete=models.CASCADE)
    highlights = models.ManyToManyField(Highlight, related_name='story_highlights')

    def to_markdown(self) -> str:
        markdown_text = f'### {self.story.title}\n\n{self.story.story}\n\n#### Highlights:\n\n'
        for highlight in self.highlights.all():
            markdown_text += f'- **{highlight.label}**: "{highlight.excerpt}"\n'
        return markdown_text

    def apply_html_highlights(self):
        highlighted_story = self.story.story
        for h in self.highlights.all():
            color = self.color if self.color else 'red'
            highlight_format = f'<span style="color: {color};">{{}}</span>'
            highlighted_story = highlighted_story.replace(h.excerpt, format_html(highlight_format, h.excerpt))
        return highlighted_story

    def __str__(self):
        return f'Story: {self.story.title}'

# Create your models here.

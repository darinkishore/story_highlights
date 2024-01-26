from django.db import models
from django.core.validators import MaxLengthValidator
import re
from flashtext import KeywordProcessor
import rapidfuzz
from transformations.dat.colors import color_set, get_color_mapping

class DjangoStory(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    story = models.TextField()

    def __str__(self):
        return f"{self.title}\n\n{self.story}"

class DjangoHighlight(models.Model):
    label = models.CharField(max_length=255)
    excerpt = models.TextField()
    color = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'- **{self.label}**: "{self.excerpt}"'

class DjangoStoryHighlights(models.Model):
    story = models.ForeignKey(DjangoStory, on_delete=models.CASCADE, related_name='story_highlights')
    highlights = models.ManyToManyField(DjangoHighlight, related_name='story_highlights')
    html_story = models.TextField(blank=True, null=True)

    def add_highlights(self, raw_highlight_response: str):
        label_pattern = re.compile(r'- \*\*(.*?)\*\*: "(.*?)"(?=\s|$)')

        for match in label_pattern.finditer(raw_highlight_response):
            label, excerpt = match.groups()
            try:
                get_color_mapping(label)
            except KeyError:
                closest_match = rapidfuzz.process.extractOne(
                    label,
                    color_set,
                    score_cutoff=2,
                    scorer=rapidfuzz.distance.Levenshtein.distance,
                )
                if closest_match is not None:
                    label = closest_match[0]

            highlight, created = DjangoHighlight.objects.get_or_create(label=label, excerpt=excerpt)
            self.highlights.add(highlight)

    def apply_html_highlights(self):
        keyword_processor = KeywordProcessor()
        for highlight in self.highlights.all():
            try:
                color = get_color_mapping(highlight.label)
            except KeyError as e:
                raise KeyError(
                    f"Label {highlight.label} not found in color mapping."
                ) from e
            html_tag = f'<span style="color:{color};">{highlight.excerpt}</span>'
            keyword_processor.add_keyword(highlight.excerpt, html_tag)

        html_story = keyword_processor.replace_keywords(
            self.story.title + "\n" + self.story.story
        )

        self.html_story = html_story
        self.save()

    def __str__(self):
        labeled_text = (
            "\n".join(str(highlight) for highlight in self.highlights.all())
            if self.highlights.exists()
            else "No highlights"
        )

        return f"### Reddit Story\n\n{self.story.title}\n{self.story.story}\n\n#### Labeled Text: \n\n{labeled_text}"

    def __repr__(self):
        num_highlights = self.highlights.count()
        num_words = len(self.story.story.split())
        num_chars = len(self.story.story)
        return f"<DjangoStoryHighlights story={self.story.title} num_highlights={num_highlights} num_words={num_words} num_chars={num_chars}>"
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=DjangoStoryHighlights)
def save_html_output(sender, instance, **kwargs):
    if not instance.html_story:
        instance.apply_html_highlights()

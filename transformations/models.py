from django.db import models
from django.db.models import (
    DateTimeField,
    JSONField,
    SlugField,
    TextField,
    URLField,
    UUIDField,
    BooleanField,
    FloatField,
    IntegerField,
)
from django.utils.text import slugify
import uuid


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


class StoryDetail(models.Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = TextField()
    body = TextField()

    raw_text = TextField()

    is_edited = models.BooleanField(default=False)
    is_highlighted = models.BooleanField(default=False)

    highlights = TextField()
    edited_story = TextField()  # text
    highlighted_story = TextField()  # html

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    slug = SlugField(unique=True, blank=True)
    url = URLField()

    def save(self, *args, **kwargs):
        if not self.id:  # If the story is being created
            self.slug = slugify(self.title)  # Generate a slug based on the title
        super(StoryDetail, self).save(*args, **kwargs)  # Call the "real" save() method.


### LEGACY TABLE


class Story(models.Model):
    created_at = DateTimeField(db_column="createdAt")
    system = TextField()
    voice = TextField()
    transpose = FloatField()
    playback = FloatField()
    stability = FloatField(blank=True, null=True)
    boost = FloatField(blank=True, null=True)
    font_family = TextField(db_column="fontFamily")
    font_size = IntegerField(db_column="fontSize")
    stroke = IntegerField()
    limit = IntegerField()
    username = TextField()
    picture = TextField()
    background = TextField(blank=True, null=True)
    start_from = IntegerField(db_column="startFrom", blank=True, null=True)
    soundtrack = TextField(blank=True, null=True)
    volume = FloatField(blank=True, null=True)
    reddit = TextField(blank=True, null=True)
    content = JSONField()
    title = TextField()
    url = TextField(blank=True, null=True)
    render_id = TextField(db_column="renderId", unique=True, blank=True, null=True)
    audio_done = BooleanField(db_column="audioDone", blank=True, null=True)
    marks_done = BooleanField(db_column="marksDone", blank=True, null=True)
    audio_id = TextField(db_column="audioId", unique=True, blank=True, null=True)
    marks_id = TextField(db_column="marksId", unique=True, blank=True, null=True)
    audio_url = TextField(db_column="audioURL", blank=True, null=True)
    marks = JSONField(blank=True, null=True)
    status = TextField()
    engine = TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Story"

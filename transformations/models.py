from django.db import models
from django.utils.text import slugify

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

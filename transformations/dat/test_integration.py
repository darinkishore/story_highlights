import pytest

from transformations.dat.models import Highlight, StoryHighlights, Story
from transformations.dat.reference_stories.reference import reference_stories
from transformations.dat.colors import get_color_mapping

# This test should read in a story, process it with highlights, use it in the prompt templates, and verify that the prompt templates are created properly. Here's a basic example of how you might structure this test:


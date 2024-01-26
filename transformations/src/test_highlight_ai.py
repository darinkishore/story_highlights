import pytest
from transformations.src.highlight_ai import *
from transformations.dat.models import StoryHighlights
from transformations.dat.reference_stories.reference import reference_stories


# @pytest.fixture
# def raw_story_text():
#     return reference_stories[0][0]


# @pytest.mark.asyncio
# async def generate_and_apply_highlights_async(raw_story_text):
#     message_list = await generate_and_apply_highlights_async(raw_story_text)
#     logger.debug("MESSAGE LIST: {}", message_list)
#     assert message_list is not None
#     assert message_list != []


# @pytest.mark.asyncio
# async def test_label_story(raw_story_text):
#     _ = await label_story(raw_story_text)
#     assert True


# async def test_label_story_returns_valid_html(raw_story_text):
# TODO

# async def test_

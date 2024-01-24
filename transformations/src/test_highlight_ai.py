import pytest
from transformations.src.highlight_ai import triple_kickstart
from transformations.dat.models import StoryHighlights
from transformations.dat.reference_stories.reference import reference_stories
from loguru import logger


@pytest.fixture
def raw_story_text():
    return reference_stories[0][0]


@pytest.mark.asyncio
async def test_triple_kickstart(raw_story_text):
    message_list = await triple_kickstart(raw_story_text)
    logger.debug("MESSAGE LIST: {}", message_list)
    assert message_list is not None
    assert message_list != []

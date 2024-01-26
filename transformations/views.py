# transfomations/views.py
from .logger import logger
from django.shortcuts import render
from django.http import HttpResponse

from .models import DjangoStory, DjangoStoryHighlights
from django.template import loader
from transformations.src.highlight_ai import label_story
from asgiref.sync import async_to_sync
from django.views.decorators.csrf import csrf_exempt

html_placeholder = "<p>Here is some text</p>"


def index(request):
    template = loader.get_template("transformations/index.html")
    return HttpResponse(template.render({}, request))


@csrf_exempt
async def highlight(request):
    logger.info(f"Incoming request - Method: {request.method}, Data: {request.POST if request.method == 'POST' else 'N/A'}")
    response_data = None
    if request.method == "POST" and request.htmx:
        text = request.POST.get("input_text")
        # Create a DjangoStory instance and save it
        django_story = DjangoStory(story=text)
        django_story.save()
        
        # Create a DjangoStoryHighlights instance and associate it with the DjangoStory
        django_story_highlights = DjangoStoryHighlights(story=django_story)
        django_story_highlights.save()
        
        # Use the DjangoStoryHighlights instance for labeling
        html = await label_story(django_story_highlights)
        django_story_highlights.html_story = html
        django_story_highlights.save()
        response_data = html
        response = HttpResponse(response_data, content_type="text/html")
        logger.debug(f"Outgoing response - Status Code: {response.status_code}, Content Type: {response['Content-Type']}")
        return response
        # text_to_highlight = request.POST.get("input_text")
        # _ = StoryHighlights(story=text_to_highlight)

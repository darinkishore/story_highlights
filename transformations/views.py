# transfomations/views.py
from transformations.dat.logger import logger
from django.shortcuts import render
from django.http import HttpResponse

from .dat.models import StoryHighlights
from django.template import loader
from transformations.src.highlight_ai import label_story
from django.views.decorators.csrf import csrf_exempt
from loguru import logger
from asgiref.sync import async_to_sync

html_placeholder = "<p>Here is some text</p>"


def index(request):
    template = loader.get_template("transformations/index.html")
    logger.info(f"Rendering index.html")
    return HttpResponse(template.render({}, request))


@csrf_exempt
def highlight(request):
    logger.info(
        f"Incoming request - Method: {request.method}, Data: {request.POST if request.method == 'POST' else 'N/A'}"
    )
    response_data = None
    if request.method == "POST" and request.htmx:
        text = request.POST.get("input_text")
        html = async_to_sync(label_story(StoryHighlights(story=text)))
        response_data = html
        response = HttpResponse(response_data, content_type="text/html")
        logger.debug(
            f"Outgoing response - Status Code: {response.status_code}, Content Type: {response['Content-Type']}"
        )
        return response
        # text_to_highlight = request.POST.get("input_text")
        # _ = StoryHighlights(story=text_to_highlight)

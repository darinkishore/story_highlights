# transfomations/views.py
from django.shortcuts import render
from django.http import HttpResponse

from .dat.models import StoryHighlights
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
    if request.method == "POST" and request.htmx:
        text = request.POST.get("input_text")
        html = await label_story(StoryHighlights(story=text))
        return HttpResponse(html, content_type="text/html")
        # text_to_highlight = request.POST.get("input_text")
        # _ = StoryHighlights(story=text_to_highlight)

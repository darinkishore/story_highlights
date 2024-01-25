# transfomations/views.py
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse

from .dat.models import StoryHighlights
from .forms import TextProcessingForm
from django.template import loader
from transformations.src.highlight_ai import label_story

html_placeholder = "<p>Here is some text</p>"


def index(request):
    template = loader.get_template("transformations/index.html")
    return HttpResponse(template.render({}, request))


from transformations.src.highlight_ai import label_story


async def highlight(request):
    if request.method == "POST":
        text = request.POST.get("input_text")
        html = await label_story(StoryHighlights(story=text))
        return HttpResponse(html, content_type="text/html")
        # text_to_highlight = request.POST.get("input_text")
        # _ = StoryHighlights(story=text_to_highlight)


def edit_1(request):
    if request.method == "POST":
        form = TextProcessingForm(request.POST)
    raise NotImplementedError


def edit_2(request):
    if request.method == "POST":
        form = TextProcessingForm(request.POST)
    raise NotImplementedError

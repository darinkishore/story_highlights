# transfomations/views.py
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from .forms import TextProcessingForm
from django.template import loader

def index(request):
    template = loader.get_template("transformations/index.html")
    return HttpResponse(template.render({}, request))
    
    

from transformations.src.highlight_ai import label_story

def highlight(request):
    if request.htmx and request.method == 'POST':
        text_to_highlight = request.POST.get('text_field_name')
        highlighted_story = label_story(text_to_highlight)
        # TODO: Apply HTML formatting to the highlighted story
        return HttpResponse(highlighted_story, content_type='text/html')
            

def edit_1(request):
    if request.method == 'POST':
        form = TextProcessingForm(request.POST)
    raise NotImplementedError

def edit_2(request):
    if request.method == 'POST':
        form = TextProcessingForm(request.POST)
    raise NotImplementedError
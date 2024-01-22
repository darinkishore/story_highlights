# transfomations/views.py
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from .forms import TextProcessingForm
from django.template import loader
from .src.highlight_ai import label_story

def index(request):
    template = loader.get_template("transformations/index.html")
    return HttpResponse(template.render({}, request))
    
    

def highlight(request):
    if request.htmx:
        if request.method == 'POST':
            text_to_highlight = request.POST['text_field_name']  # TODO: Replace 'text_field_name' with actual field name
            labeled_story = label_story(text_to_highlight)
            # TODO: Apply HTML formatting to the labeled story
            html_content = f'<div>{{labeled_story}}</div>'  # Simple HTML wrapper for demonstration
            return HttpResponse(html_content)
            

def edit_1(request):
    if request.method == 'POST':
        form = TextProcessingForm(request.POST)
    raise NotImplementedError

def edit_2(request):
    if request.method == 'POST':
        form = TextProcessingForm(request.POST)
    raise NotImplementedError
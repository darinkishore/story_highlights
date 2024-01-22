# transfomations/views.py
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from .forms import TextProcessingForm
from django.template import loader

def index(request):
    template = loader.get_template("transformations/index.html")
    return HttpResponse(template.render({}, request))
    
    
# TODO: change so we don't use form anymore

def highlight(request):
    if request.htmx:
        if request.method == 'POST':
            # get text from input field
            # highlight the text by calling the highlight_text function
            # from transformations/src/highlight_ai.py
            # return the html-highlighted text
            raise NotImplementedError
            

def edit_1(request):
    if request.method == 'POST':
        form = TextProcessingForm(request.POST)
    raise NotImplementedError

def edit_2(request):
    if request.method == 'POST':
        form = TextProcessingForm(request.POST)
    raise NotImplementedError
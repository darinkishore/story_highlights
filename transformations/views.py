# transfomations/views.py
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from .forms import TextProcessingForm

def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)

# TODO: change so we don't use form anymore

def highlight(request):
    if request.method == 'POST':
        form = TextProcessingForm(request.POST)
        if form.is_valid():
            # Process form data
            # ...
            # Return an HTMX response (e.g., JsonResponse with the processed text)
            raise NotImplementedError
    else:
        form = TextProcessingForm()

    return render(request, 'highlight.html', {'form': form})

def edit_1(request):
    if request.method == 'POST':
        form = TextProcessingForm(request.POST)
    raise NotImplementedError

def edit_2(request):
    if request.method == 'POST':
        form = TextProcessingForm(request.POST)
    raise NotImplementedError
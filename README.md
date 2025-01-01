# Story Highligter 

Story Highlighter is a Django-based application for LLM-powered story highlighting. It provides a set of models, prompts, and tests that enable the generation and application of labeled highlights to various texts—particularly “stories”—primarily for use in automating tiktok video generation according to an arbitrary set of rules. 

## Overview

Story Highlighter is designed as a Django app that processes user-provided stories or text, sends them to an LLM (e.g., GPT-4), and returns highlight labels according to a set of categories. Each highlight is mapped to a color, then rendered in HTML. The system is organized around a few primary components:

- **transformations/**  
  This Django app contains the models (e.g., `Story`, `StoryDetail`, `Highlight`, `StoryHighlights`), the logic for prompt creation (in `prompts/`), reference story examples, and test coverage.  
  - `models.py` in the main transformations directory (and in `dat/models.py`) define Pydantic or Django-based model structures.  
  - `src/highlight_ai.py` handles sending text to an LLM with structured prompts, merges highlights, and returns HTML.  
  - `dat/prompts/` includes prompt templates and examples that feed into your label logic.  
  - `dat/reference_stories/` houses sample stories plus labeled segments, illustrating how the labeling system should work.

- **vercel_app/**  
  This is the Django project directory with `settings.py`, `urls.py`, and other configuration files. It’s set up to deploy on Vercel (or can be run locally). The Django settings are configured to use environment variables for database connectivity and other secrets.  

- **manage.py**  
  Standard Django entry point for running commands (migrations, server, etc.).

- **requirements.txt**  
  Lists the dependencies, including OpenAI, Django, and a few testing and logging libraries.

- **Tests**  
  A variety of tests (Pytest style) live under `transformations/dat/test_*.py` and the top-level `tests.py`. These cover model initialization, highlight logic, HTML generation, and more.

## Key Features

1. **Story and Highlight Models**  
   `StoryHighlights` and `Highlight` track how each snippet of text should be labeled and displayed.  

2. **Prompt Templates & LLM Integration**  
   In `prompts/prompt_templates.py`, you’ll find logic that auto-generates prompts to be sent to an OpenAI model. It categorizes highlights into Characters, Plot Elements, Descriptions, etc.

3. **Reference Stories**  
   The `reference_stories` folder includes example stories with thorough “labeled sections,” making it easy to see how the pipeline infers and marks text with an LLM.

4. **Asynchronous Calls to GPT**  
   `highlight_ai.py` demonstrates asynchronous usage of the OpenAI API, bridging Django with Python’s `asyncio`.

5. **HTML Highlight Rendering**  
   After receiving label data from GPT, the system inserts inline HTML `<span style="color:...">...</span>` tags for easy color-based highlighting.

## Getting Started

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/yourusername/LLMStoryLab.git
   cd LLMStoryLab
   ```

   
2.	Install Dependencies
```
pip install -r requirements.txt
```

3.	Set Up Environment Variables
Create a .env file or export env variables for your OpenAI credentials, database, etc. Example:
```
DJANGO_SECRET_KEY=someSecretKey
OPENAI_API_KEY=your_openai_key
DJANGO_DEBUG=True
SECRET_KEY=&yz70mwzl*4qsjq8fexdz!s@jl6q$#5u_%srecpc*)m9l-)nj3 (change this!)
DJANGO_ALLOWED_HOSTS=*
# DJANGO_DATABASE_URL=postgres://
DJANGO_DATABASE_NAME=postgres
DJANGO_DATABASE_USER=postgres
DJANGO_DATABASE_PASSWORD=alsopostgres
DJANGO_DATABASE_HOST=aws-0-us-west-1.pooler.supabase.com
DJANGO_DATABASE_PORT=5432
```

4.	Apply Migrations and Run Locally

```
python manage.py migrate
python manage.py runserver
```
By default, it'll run at http://127.0.0.1:8000.

5.	Explore the Transformations App
6.	Visit the root URL. Then go to /highlight (see transformations/urls.py) to test the highlight logic in an HTMX-based form submission flow. You can paste text and see how the LLM labeling pipeline processes it.

7. Optional: Run with Granian
If you want to try a different server or just wanna go real fast >:) 

```
granian --interface wsgi vercel_app.wsgi:app --reload
```

7.	Deploying to Vercel
The project is set up for quick deploy via the Python Runtime on Vercel. Make sure to set environment variables in Vercel’s dashboard for your Django secret keys, OpenAI key, etc. More details are in vercel_app/settings.py and the included vercel.json.

Contributing

Contributions are welcome. Feel free to open issues for any bugs, suggestions, or enhancements. This repo includes a variety of test files to ensure the reliability of highlight logic, so be sure to write your own tests or run existing ones (pytest) before submitting PRs.

License

MIT. 

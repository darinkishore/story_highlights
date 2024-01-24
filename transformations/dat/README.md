# What is this directory?
This directory contains the models and prompts for working with reddit stories and highlighting them.

Key Info:

`models.py`:
Contains 3 models for working with stories and their (ai-generated, see ../src) highlights.

1. `Story`: This model represents a story with a title and the story text. If no title is provided, the first line of the story text is used as the title.

2. `Highlight`: This model represents a highlight with a label, an excerpt, and an optional color. The `__str__` method returns a string representation of the highlight in markdown format.

3. `StoryHighlights`: This model represents a story with its highlights. It contains methods to process the story, convert the story to markdown, add highlights to the story, apply HTML highlights to the story, and return string representations of the story. 

The most important model is `StoryHighlights` which is a model that contains a story and its highlights.

It's initialized by simply passing in the raw story text. 
ie: `story = StoryHighlights(story=story_text)`

It also has a method `add_highlights` which takes a raw highlights string and adds them to the story. Generally, in the `transformations` app, we will get the input raw story text from the form, use GPT calls to get the raw highlight string, then adds the highlights to the story for storage.

Finally, before rendering the story in the `highlight` view in views.py, we will call the `apply_html_highlights` method to apply the highlights to the story text. 

The `apply_html_highlights` method applies HTML color highlights to the story text. The `to_markdown` method converts the story and its highlights to markdown format.


import sglang as sgl
from sglang import (OpenAI, assistant, function, gen, set_default_backend,
                    system, user)
from transformations.dat.models import HTMLStory, Label, LabeledStory, Story
from transformations.dat.prompt_templates import (characters, descriptions,
                                                  generate_labeled_text,
                                                  plot_elements)
from transformations.dat.stories_html.reference import reference_stories

set_default_backend(OpenAI("gpt-3.5-turbo"))

@function
def generate_and_label_story(s):
    s += system("You are an Labeling System Specialist, who helps create interesting stories by labeling their "
                "individual parts for future post processing, according to a strict ruleset. You are meticulous and "
                "thorough, and go through the texts you label line by line to extract every detail and fulfill your "
                "stage in the processing pipeline.")

    forks = s.fork(3)
    categories = [characters, plot_elements, descriptions]
    category_names = ["Characters", "Plot Elements", "Descriptions"]
    example_stories = {}

    for i, fork in enumerate(forks):
        category = categories[i]
        category_name = category_names[i]
        fork += user(f"Please plan the labels for the category: {category_name}")
        fork += assistant(gen(f"label_plan_{i}", max_tokens=500))

        # Dynamically select the best example for each category
        best_example = None
        max_label_count = 0
        for story_text, labeled_text in reference_stories:
            labeled_story = LabeledStory.from_markdown(labeled_text, story_text)
            label_count = sum(1 for label in labeled_story.labels if label.label in category)
            if label_count > max_label_count:
                best_example = labeled_story
                max_label_count = label_count

        example_stories[category_name] = best_example

    # Generate follow-up prompts with examples
    for category_name, labeled_story in example_stories.items():
        s += user(f"Here is the best example for the category {category_name}:")
        s += assistant(generate_labeled_text(labeled_story.labels))

    # Render the highlights to HTML
    color_mapping = {
        "Main Male Character": "#FF0000",
        "Main Female Character": "#00FF00",
        "Antagonist/Villain": "#0000FF",
        # Add more color mappings as needed
    }
    html_content = ""
    for labeled_story in example_stories.values():
        html_story = HTMLStory(story=Story(title=labeled_story.story.title, story=labeled_story.story.story),
                               labels=labeled_story.labels)
        html_content += html_story.apply_html_tags(color_mapping)

    return html_content

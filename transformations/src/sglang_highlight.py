from sglang import OpenAI, fork, function, gen, set_default_backend
from transformations.dat.models import HTMLStory
from transformations.dat.stories_html.reference import reference_stories

set_default_backend(OpenAI("gpt-3.5-turbo"))

@function
def generate_highlighted_stories(s):
    categories = ["Characters", "Plot Elements", "Descriptions"]
    forks = s.fork(len(categories))
    category_examples = {}

    for i, f in enumerate(forks):
        category = categories[i]
        f += gen(f"{category}_plan", max_tokens=256)
        best_example, best_labels = select_best_example_for_category(category)
        category_examples[category] = (best_example, best_labels)

    html_content = ""
    for category, (example, labels) in category_examples.items():
        html_story = HTMLStory(story=example, labels=labels)
        html_content += html_story.apply_html_tags(color_mapping=get_color_mapping_for_category(category))

    return html_content

def select_best_example_for_category(category):
    label_counts = {story[0]: 0 for story in reference_stories}
    for story, labeled_text in reference_stories:
        label_counts[story] += labeled_text.count(category)

    best_story = max(label_counts, key=label_counts.get)
    best_labels = [label for label in reference_stories if label[0] == best_story][0][1]
    return best_story, best_labels

def get_color_mapping_for_category(category):
    color_mappings = {
        "Characters": "#FF0000",
        "Plot Elements": "#00FF00",
        "Descriptions": "#0000FF",
    }
    return color_mappings.get(category, "#000000")

# Unit tests for the generate_highlighted_stories function
def test_generate_highlighted_stories():
    state = generate_highlighted_stories.run()
    assert "<span style=" in state.result()
    assert "Characters" in state.result()
    assert "Plot Elements" in state.result()
    assert "Descriptions" in state.result()

# Unit tests for the select_best_example_for_category function
def test_select_best_example_for_category():
    for category in ["Characters", "Plot Elements", "Descriptions"]:
        story, labels = select_best_example_for_category(category)
        assert story in [story[0] for story in reference_stories]
        assert isinstance(labels, str)

# Unit tests for the get_color_mapping_for_category function
def test_get_color_mapping_for_category():
    assert get_color_mapping_for_category("Characters") == "#FF0000"
    assert get_color_mapping_for_category("Plot Elements") == "#00FF00"
    assert get_color_mapping_for_category("Descriptions") == "#0000FF"
    assert get_color_mapping_for_category("Unknown") == "#000000"

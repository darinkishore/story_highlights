import sglang as sgl

from .models import Label, LabeledStory, Story
from .prompt_templates import characters, descriptions, plot_elements
from .stories_html.reference import sample_stories


@sgl.function
def generate_labeling_prompts(s, story_text, story_title):
    # Load the story into a Story model
    story = Story(title=story_title, story=story_text)

    # Forking to handle each category in parallel
    categories = [characters, plot_elements, descriptions]
    category_names = ["Characters", "Plot Elements", "Descriptions"]
    forks = s.fork(len(categories))

    # Generate prompts for each category and select the best examples
    for i, f in enumerate(forks):
        category = categories[i]
        category_name = category_names[i]
        f += sgl.system(f"You are an AI trained to label text using the following categories: {category_name}.")
        f += sgl.user(f"Please plan the labels for the following story: {story_text}")
        f += sgl.assistant(sgl.gen(f"{category_name}_labels", max_tokens=500))

        # Analyze stories and count labels to select the best example
        best_example = None
        max_label_count = 0
        for sample_story in sample_stories:
            labeled_story = LabeledStory.from_markdown(f[category_name + "_labels"], sample_story["story"], sample_story["title"])
            label_count = len(labeled_story.labels)
            if label_count > max_label_count:
                best_example = labeled_story
                max_label_count = label_count

        # Apply HTML tags to the best example
        f += best_example.apply_html_tags()

    # Combine the results from all forks
    labeled_sections = []
    for i, f in enumerate(forks):
        category_name = category_names[i]
        labeled_sections.append(f"#### {category_name}\n{f.result}")

    # Generate the final prompt with all labeled sections
    s += sgl.system("Combine all labeled sections into a single prompt.")
    s += sgl.user("\n\n".join(labeled_sections))
    s += sgl.assistant(sgl.gen("final_prompt", max_tokens=1000))

    # Return the final HTML story with labels
    return s["final_prompt"]

# Example usage
if __name__ == "__main__":
    example_story_text = "Once upon a time in a land far, far away..."
    example_story_title = "An Epic Tale"
    labeled_html_story = generate_labeling_prompts.run(story_text=example_story_text, story_title=example_story_title)
    print(labeled_html_story)

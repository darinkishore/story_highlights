import sglang as sgl

from .models import StoryHighlights


@sgl.function
def label_story_with_sglang(s, story_text):
    s += sgl.system("You are an Labeling System Specialist.")
    
    # Forking to handle multiple categories in parallel
    categories = ["Characters", "Plot Elements", "Descriptions"]
    forks = s.fork(len(categories))
    
    # Dynamically select the best examples for each category
    for f, category in zip(forks, categories):
        f += f"Now, plan the labels for the category: {category}.\n"
        f += sgl.gen(f"plan_{category.lower()}", max_tokens=256)
    
    # Generate the labels for the story text
    s += f"Now, label the following story:\n\n### Reddit Story\n```\n{story_text}\n```\n\n"
    s += sgl.gen("labeled_story", max_tokens=1024)
    
    # Apply HTML formatting to the labeled story
    labeled_story = s["labeled_story"]
    story_highlights = StoryHighlights.process_story_highlights(labeled_story, story_text)
    html_formatted_story = story_highlights.apply_html_highlights_to_story()
    
    return html_formatted_story

# Example usage of the function
if __name__ == "__main__":
    example_story = "Once upon a time in a land far, far away..."
    html_story = label_story_with_sglang.run(story_text=example_story)
    print(html_story)

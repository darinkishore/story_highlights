from transformations.src.sglang_highlight import generate_highlighted_stories

def kickstart(story: str = ""):
    return generate_highlighted_stories.run(story)
# def generate(prompt: str, max_tokens: int = 500, message_history: List[dict] = []):
#     ...
    html_content = kickstart(story)
    return html_content

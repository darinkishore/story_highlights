from transformations.src.sglang_highlight import generate_highlighted_stories

def kickstart(story: str = ""):
<<<<<<< HEAD
    return generate_highlighted_stories.run(story)
# def generate(prompt: str, max_tokens: int = 500, message_history: List[dict] = []):
#     ...
    html_content = kickstart(story)
    return html_content
=======
    prompt1 = get_prompt_part1(story)
    prompt2 = get_prompt_part2()
    message_list = generate(prompt1)
    message_list = generate(prompt2, message_history=message_list)
    return message_list
    if message_history:
        message_history.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=message_history,
            temperature=0.0,
        )
        return message_history + [{"role": "assistant", "content": response.choices[0].message.content.strip()}]
    else:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            temperature=0.0,
            max_tokens=max_tokens,
        )
        return messages + [{"role": "assistant", "content": response.choices[0].message.content.strip()}]
def get_last(message_history: List[dict]):
    return message_history[-1]["content"]

def label_story(story: str):
    _ = (kickstart(story))
    highlight_schema = get_last(_)
    # TODO: Apply HTML formatting to the labeled story
    return highlight_schema
def get_last(message_history: List[dict]):
    return message_history[-1]["content"]

def label_story(story: str):
    _ = (kickstart(story))
    highlight_schema = get_last(_)
    # TODO: Apply HTML formatting to the labeled story
    return highlight_schema
def get_last(message_history: List[dict]):
    return message_history[-1]["content"]

def label_story(story: str):
    _ = (kickstart(story))
    highlight_schema = get_last(_)
    # TODO: Apply HTML formatting to the labeled story
    return highlight_schema
    # TODO: Apply HTML formatting to the labeled story
    return highlight_schema
>>>>>>> origin/main

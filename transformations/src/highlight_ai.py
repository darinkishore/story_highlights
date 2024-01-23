from http.client import HTTPException

from openai import OpenAI
import openai
from typing import List
import os
from dotenv import load_dotenv
from ..dat.prompt_templates import system_prompt, generate_user_prompt, user_follow_up_prompt




load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_prompt_part1(story):
    return generate_user_prompt(story)

def get_prompt_part2():
    return user_follow_up_prompt

def kickstart(story: str, story_title: str):
    # Call to the new SGLang function from transformations/dat/sglang_templates
    from .sglang_templates import generate_labeling_prompts
    return generate_labeling_prompts.run(story_text=story, story_title=story_title)

def generate(prompt: str, max_tokens: int = 500, message_history: List[dict] = []):
    try:
        client = OpenAI()
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_last(message_history: List[dict]):
    return message_history[-1]["content"]

def label_story(story: str, story_title: str):
    from .models import LabeledStory
    # Call to the new SGLang function and applying HTML formatting
    labeled_html_story = kickstart(story, story_title)
    # Convert the labeled sections to the LabeledStory object
    labeled_story = LabeledStory.from_html(labeled_html_story)
    # Apply HTML tags to the labeled story
    labeled_story.apply_html_tags()
    return labeled_story.html

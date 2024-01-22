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

from .sglang_templates import generate_and_label_story

def kickstart(story: str = ""):
    html_content = generate_and_label_story(story)
    return html_content

def generate(prompt: str, max_tokens: int = 500, message_history: List[dict] = []):
# def generate(prompt: str, max_tokens: int = 500, message_history: List[dict] = []):
#     ...
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

def label_story(story: str):
    html_content = kickstart(story)
    return html_content

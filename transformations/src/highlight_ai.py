from http.client import HTTPException

from openai import AsyncOpenAI
import openai
from typing import List
import os
import asyncio
from dotenv import load_dotenv
from transformations.dat.prompts.prompt_templates import (
    system_prompt,
    generate_user_prompt,
    user_follow_up_prompt,
)


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_prompt_part1(story):
    return generate_user_prompt(story)


def get_prompt_part2():
    return user_follow_up_prompt


async def kickstart(story: str = ""):
    prompts = [get_prompt_part1(story), get_prompt_part2()]
    message_lists = await asyncio.gather(*(generate(prompt) for prompt in prompts))
    return [item for sublist in message_lists for item in sublist]


async def generate(prompt: str, max_tokens: int = 500, message_history: List[dict] = []):
    try:
        client = AsyncOpenAI()
        if message_history:
            message_history.append({"role": "user", "content": prompt})
            try:
                response = await client.chat.completions.create(
                    model="gpt-4-1106-preview",
                    messages=message_history,
                    temperature=0.0,
                )
            except openai.error.OpenAIError as e:
                raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
            return message_history + [
                {
                    "role": "assistant",
                    "content": response.choices[0].message.content.strip(),
                }
            ]
        else:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]
            response = await client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=messages,
                temperature=0.0,
                max_tokens=max_tokens,
            )
            return messages + [
                {
                    "role": "assistant",
                    "content": response.choices[0].message.content.strip(),
                }
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_last(message_history: List[dict]):
    return message_history[-1]["content"]


def label_story(story: str):
    _ = asyncio.run(kickstart(story))
    highlight_schema = get_last(_)
    # Applying HTML formatting to the labeled story
    highlighted_html = f"<div class='story'>{''.join(['<strong>' + part.split(':')[0] + '</strong>' + part.split(':')[1] for part in highlight_schema.split('**Label**:') if part.strip() != ''])}</div>"
    return highlighted_html

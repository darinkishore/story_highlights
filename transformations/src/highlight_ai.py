import time
from http.client import HTTPException
import asyncio
from openai import OpenAI, AsyncOpenAI
import openai
from typing import List
import os
from dotenv import load_dotenv
from transformations.dat.prompts.prompt_templates import (
    generate_category_plan_prompt,
)
from transformations.dat.prompts.prompt_elements import (
    system_prompt,
    user_follow_up_prompt,
)
from transformations.dat.models import StoryHighlights, Story
from transformations.dat.prompts.prompt_templates import generate_all_prompts
from typing import Any


load_dotenv()

# Refactored MODEL into a constant
MODEL = "gpt-4-1106-preview"


def get_last(message_history: List[dict]):
    return message_history[-1]["content"]


async def generate_raw_highlights(initial_prompt, follow_up_prompt):
    message_list = await async_generate(initial_prompt)
    message_list += await async_generate(follow_up_prompt, message_history=message_list)
    return message_list[-1]["content"]


async def label_story(story: StoryHighlights) -> str:
    all_prompts = generate_all_prompts(str(story.story))

    highlight_generation_tasks = []
    for category in all_prompts["initial"].keys():
        initial_prompt = all_prompts["initial"][category]
        follow_up_prompt = all_prompts["follow_up"][category]
        highlight_generation_tasks.append(
            generate_raw_highlights(initial_prompt, follow_up_prompt)
        )

    for task in asyncio.as_completed(highlight_generation_tasks):
        highlight_content = await task
        story.add_highlights(highlight_content)

    story.apply_html_highlights()
    return story.html_story


async def async_generate(prompt: str, max_tokens=500, message_history=None):
    if message_history is None:
        message_history = []
    client = AsyncOpenAI()
    if message_history:
        message_history.append({"role": "user", "content": prompt})
        try:
            response = await client.chat.completions.create(
                model=MODEL,
                messages=message_history,
                temperature=0.0,
            )
        except (openai.OpenAIError, openai.APIError, openai.RateLimitError) as e:
            try:
                time.sleep(0.5)
                response = await client.chat.completions.create(
                    model=MODEL,
                    messages=message_history,
                    temperature=0.0,
                )
            except (
                openai.OpenAIError,
                openai.APIError,
                openai.RateLimitError,
            ) as e:
                raise e
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
        try:
            response = await client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.0,
                max_tokens=max_tokens,
            )
        except (openai.OpenAIError, openai.APIError, openai.RateLimitError) as e:
            try:
                time.sleep(0.5)
                response = await client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    temperature=0.0,
                    max_tokens=max_tokens,
                )
            except (
                openai.OpenAIError,
                openai.APIError,
                openai.RateLimitError,
            ) as e:
                raise e
        return messages + [
            {
                "role": "assistant",
                "content": response.choices[0].message.content.strip(),
            }
        ]


### OLD METHODS ###
# def get_prompt_part1(story):
#     return generate_category_plan_prompt(story)
#
#
# def get_prompt_part2():
#     return user_follow_up_prompt
#
#
# def kickstart(story: str = ""):
#     prompt1 = get_prompt_part1(story)
#     prompt2 = get_prompt_part2()
#     message_list = generate(prompt1)
#     message_list = generate(prompt2, message_history=message_list)
#     return message_list
#
#
# def generate(prompt: str, max_tokens: int = 500, message_history: List[dict] = []):
#     try:
#         client = OpenAI()
#         if message_history:
#             message_history.append({"role": "user", "content": prompt})
#             response = client.chat.completions.create(
#                 model="gpt-4-1106-preview",
#                 messages=message_history,
#                 temperature=0.0,
#             )
#             return message_history + [
#                 {
#                     "role": "assistant",
#                     "content": response.choices[0].message.content.strip(),
#                 }
#             ]
#         else:
#             messages = [
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": prompt},
#             ]
#             response = client.chat.completions.create(
#                 model="gpt-4-1106-preview",
#                 messages=messages,
#                 temperature=0.0,
#                 max_tokens=max_tokens,
#             )
#             return messages + [
#                 {
#                     "role": "assistant",
#                     "content": response.choices[0].message.content.strip(),
#                 }
#             ]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#


#
#
# def label_story(story: str):
#     _ = kickstart(story)
#     highlight_schema = get_last(_)
#     # TODO: Apply HTML formatting to the labeled story
#     return highlight_schema

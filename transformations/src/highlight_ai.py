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

load_dotenv()


async def handle_category(initial_prompt, follow_up_prompt):
    message_list = await async_generate(initial_prompt)
    message_list += await async_generate(follow_up_prompt, message_history=message_list)
    return message_list

async def triple_kickstart(story: str = ""):
    from transformations.dat.prompts.prompt_templates import generate_all_prompts

    all_prompts = generate_all_prompts(story)
    message_list = []

    tasks = []
    for category in all_prompts['initial'].keys():
        initial_prompt = all_prompts['initial'][category]
        follow_up_prompt = all_prompts['follow_up'][category]
        tasks.append(handle_category(initial_prompt, follow_up_prompt))

    results = await asyncio.gather(*tasks)

    for result in results:
        message_list += result

    return message_list

async def async_generate(prompt: str, max_tokens=500, message_history: List[dict] = []):
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


def get_prompt_part1(story):
    return generate_category_plan_prompt(story)


def get_prompt_part2():
    return user_follow_up_prompt


def kickstart(story: str = ""):
    prompt1 = get_prompt_part1(story)
    prompt2 = get_prompt_part2()
    message_list = generate(prompt1)
    message_list = generate(prompt2, message_history=message_list)
    return message_list

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
            response = client.chat.completions.create(
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
    _ = kickstart(story)
    highlight_schema = get_last(_)
    # TODO: Apply HTML formatting to the labeled story
    return highlight_schema

from typing import List, Any
import rapidfuzz
from pydantic import BaseModel, validator, model_validator
import re
from flashtext import KeywordProcessor

from transformations.dat.colors import color_set, get_color_mapping


# Define the Pydantic models


class Story(BaseModel):
    title: str = None
    story: str

    @model_validator(mode="before")
    def gen_title(cls, data):
        # look for the very first line break in the story, return the text before it, and modify the original story to remove the title
        if data.get("title") is not None and data["title"].strip() != "Test Story":
            return data
        else:
            data["story"] = data["story"].strip()
            title = data["story"].split("\n")[0].strip()
            data["title"] = title
            data["story"] = data["story"].replace(title, "", 1).strip()
            return data


class Highlight(BaseModel):
    label: str
    excerpt: str
    color: str = None

    def __str__(self):
        return f'- **{self.label}**: "{self.excerpt}"'


class StoryHighlights(BaseModel):
    story: Story
    highlights: List[Highlight]
    html_story: str = None

    def to_markdown(self) -> str:
        markdown_text = f"### {self.story.title}\n\n{self.story.story}\n\n#### Labeled Sections:\n\n"
        for label in self.labels:
            markdown_text += str(label) + "\n"
        return markdown_text

    @classmethod
    def process_story_highlights(
        cls,
        raw_highlight_response: str,
        story_text: str,
        story_title: str = "Story Title",
    ):
        # Update the regex pattern to handle nested quotations
        label_pattern = re.compile(r'- \*\*(.*?)\*\*: "(.*?)"(?=\s|$)')
        highlights_list = []

        for match in label_pattern.finditer(raw_highlight_response):
            label, excerpt = match.groups()
            try:
                # This will raise a KeyError if the label doesn't exist in the color mappings
                get_color_mapping(label)
            except KeyError:
                # If the label doesn't exist, find the closest match and replace the label with that
                closest_match = rapidfuzz.process.extractOne(
                    label,
                    color_set,
                    score_cutoff=2,
                    scorer=rapidfuzz.distance.Levenshtein.distance,
                )
                if closest_match is not None:
                    label = closest_match[0]

            highlights_list.append(Highlight(label=label, excerpt=excerpt))

        story = Story(title=story_title, story=story_text)
        return cls(story=story, highlights=highlights_list)

    def apply_html_highlights_to_story(self):
        from transformations.dat.colors import get_color_mapping

        keyword_processor = KeywordProcessor()
        for highlight in self.highlights:
            try:
                color = get_color_mapping(highlight.label)
            except KeyError as e:
                raise KeyError(
                    f"Label {highlight.label} not found in color mapping."
                ) from e
            html_tag = f'<span style="color:{color};">{highlight.excerpt}</span>'
            keyword_processor.add_keyword(highlight.excerpt, html_tag)

        html_story = keyword_processor.replace_keywords(self.story.story)

        return html_story

    def __str__(self):
        labeled_text = "\n".join(str(highlight.label) for highlight in self.highlights)

        return f"""### Reddit Story\n
        {self.story.title}\n
        {self.story.story}\n\n
        #### Labeled Text:\n\n
        {labeled_text}
        """

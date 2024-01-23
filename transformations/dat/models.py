from spacy import load
from typing import List, Any
from pydantic import BaseModel
import re
import pysubstringsearch as psss
import os
import snoop
from flashtext import KeywordProcessor

# Define the Pydantic models


class Story(BaseModel):
    title: str
    story: str

class Label(BaseModel):
    label: str
    excerpt: str

    def __str__(self):
        return f'- **{self.label}**: "{self.excerpt}"'


class LabeledStory(BaseModel):
    story: Story
    labels: List[Label]
    html_story: str = None

    def to_markdown(self) -> str:
        markdown_text = f'### {self.story.title}\n\n{self.story.story}\n\n#### Labeled Sections:\n\n'
        for label in self.labels:
            markdown_text += str(label) + '\n'
        return markdown_text

    @classmethod
    def from_markdown(
        cls, markdown_text: str, story_text: str, story_title: str = "Story Title"
    ):
        # Update the regex pattern to handle nested quotations
        label_pattern = re.compile(r'- \*\*(.*?)\*\*: "(.*?)"(?=\s|$)')
        labels = []

        for match in label_pattern.finditer(markdown_text):
            label, excerpt = match.groups()
            labels.append(Label(label=label, excerpt=excerpt))

        story = Story(title=story_title, story=story_text)
        return cls(story=story, labels=labels)

    def apply_html_tags(self):
        from transformations.dat.colors import get_color_mapping
        keyword_processor = KeywordProcessor()
        for label in self.labels:
            try:
                color = get_color_mapping(label.label)
            except KeyError as e:
                raise KeyError(f"Label {label.label} not found in color mapping.") from e
            html_tag = f'<span style="color:{color};">{label.excerpt}</span>'
            keyword_processor.add_keyword(label.excerpt, html_tag)

        html_story = keyword_processor.replace_keywords(self.story.story)

        return html_story

    def __str__(self):
        labeled_text = "\n".join(str(label) for label in self.labels)

        return f"""### Reddit Story\n
        {self.story.title}\n
        {self.story.story}\n\n
        #### Labeled Text:\n\n
        {self.labeled_text}
        """
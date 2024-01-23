from typing import List, Any
import rapidfuzz
from pydantic import BaseModel
import re
from flashtext import KeywordProcessor

from transformations.dat.colors import color_set, get_color_mapping


# Define the Pydantic models


class Story(BaseModel):
    story: str


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
        story_text: str
    ):

        label_pattern = re.compile(r'- \*\*(.*?)\*\*: "(.*?)"(?=\s|$)')
        highlights_list = []
    def __init__(self, story: str):
        lines = story.split('\n', 1)
        self.title = lines[0]
        self.story = lines[1] if len(lines) > 1 else ''
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


        return cls(story=Story(story=story_text), highlights=highlights_list)

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
        {self.story.title.strip()}\n  # Ensure title has no leading/trailing whitespace
        {self.story.story}\n\n
        #### Labeled Text:\n\n
        {labeled_text}
        """

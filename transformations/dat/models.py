from typing import List, Any
from pydantic import BaseModel
import re
from flashtext import KeywordProcessor

# Define the Pydantic models


class Story(BaseModel):
    story: str

    def __init__(self, story: str, **data: Any):
        super().__init__(story=story, **data)
        story_lines = story.split('\n', 1)
        self.title = story_lines[0] if story_lines else ''
        self.story = story_lines[1] if len(story_lines) > 1 else story


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
        markdown_text = f'### {self.story.title}\n\n{self.story.story}\n\n#### Labeled Sections:\n\n'
        for label in self.labels:
            markdown_text += str(label) + '\n'
        return markdown_text

    @classmethod
    def process_story_highlights(
        cls,
        raw_highlight_response: str,
        story_text: str
    ):
        # Update the regex pattern to handle nested quotations
        label_pattern = re.compile(r'- \*\*(.*?)\*\*: "(.*?)"(?=\s|$)')
        highlights_list = []

        for match in label_pattern.finditer(raw_highlight_response):
            label, excerpt = match.groups()
            highlights_list.append(Highlight(label=label, excerpt=excerpt))

        story = Story(story=story_text)

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

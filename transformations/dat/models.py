from typing import List, Any
from pydantic import BaseModel
import re
from flashtext import KeywordProcessor

# Define the Pydantic models


class Story(BaseModel):
    title: str
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

        html_story = keyword_processor.replace_keywords(self.html_story)

        return html_story

    def __str__(self):
        labeled_text = "\n".join(str(highlight.label) for highlight in self.highlights)

        return f"""### Reddit Story\n
        {self.story.title}\n
        {self.story.story}\n\n
        #### Labeled Text:\n\n
        {labeled_text}
        """

from typing import List, Any, Optional, Union
import rapidfuzz
from pydantic import BaseModel, field_validator, model_validator
import re
from flashtext import KeywordProcessor

from transformations.dat.colors import color_set, get_color_mapping
from transformations.dat.prompts.prompt_elements import characters, plot_elements, descriptions
from transformations.dat.prompts.prompt_templates import categories

def get_category(label: str) -> str:
    if label in characters:
        return 'characters'
    elif label in plot_elements:
        return 'plot_elements'
    elif label in descriptions:
        return 'descriptions'
    else:
        raise ValueError(f"Label '{label}' does not belong to any recognized category.")


class Story(BaseModel):
    title: str = None
    story: str

    @model_validator(mode="before")
    def gen_title(cls, data):
        if data.get("title") is not None and data["title"].strip() != "Test Story":
            return data
        else:
            data["story"] = data["story"].strip()
            title = data["story"].split("\n")[0].strip()
            data["title"] = title
            data["story"] = data["story"].replace(title, "", 1).strip()
            return data

    def __str__(self):
        return f"{self.title}\n\n{self.story}"


class Highlight(BaseModel):
    label: str
    excerpt: str
    color: str = None

    def __str__(self):
        return f'- **{self.label}**: "{self.excerpt}"'


class StoryHighlights(BaseModel):
    story: Union[Story, str] = None
    highlights: Optional[List[Highlight]] = []
    html_story: str = None

    @model_validator(mode="before")
    def process_story(cls, data):
        if isinstance(data["story"], Story):
            return data
        else:
            data["story"] = Story(story=data["story"])
            return data

    def to_markdown(self) -> str:
        markdown_text = f"### {self.story.title}\n\n{self.story.story}\n\n#### Labeled Sections:\n\n"
        for label in self.labels:
            markdown_text += str(label) + "\n"
        return markdown_text

    def add_highlights(self, raw_highlight_response: str):
        label_pattern = re.compile(r'- \*\*(.*?)\*\*: "(.*?)"(?=\s|$)')

        for match in label_pattern.finditer(raw_highlight_response):
            label, excerpt = match.groups()
            try:
                get_color_mapping(label)
            except KeyError:
                closest_match = rapidfuzz.process.extractOne(
                    label,
                    color_set,
                    score_cutoff=2,
                    scorer=rapidfuzz.distance.Levenshtein.distance,
                )
                if closest_match is not None:
                    label = closest_match[0]

            self.highlights.append(Highlight(label=label, excerpt=excerpt))

    def apply_html_highlights(self):
        from transformations.dat.colors import get_color_mapping

        keyword_processor = KeywordProcessor()
        processed_highlights = []
        for highlight in self.highlights:
            highlight_category = get_category(highlight.label)
            overlap = False
            for existing_highlight in processed_highlights:
                existing_category = get_category(existing_highlight.label)
                # according to prompt, highlights may overlap, so here we assume this function exists
                if excerpts_overlap(highlight.excerpt, existing_highlight.excerpt):
                    # Implement tiebreaking logic based on categories
                    category_priority = {'characters': 3, 'plot_elements': 2, 'descriptions': 1}
                    if category_priority[highlight_category] > category_priority[existing_category]:
                        # Replace existing highlight with the current one
                        processed_highlights.remove(existing_highlight)
                        processed_highlights.append(highlight)
                        overlap = True
                        break
            if not overlap:
                # Add the current highlight to processed_highlights
                processed_highlights.append(highlight)
            try:
                color = get_color_mapping(highlight.label)
            except KeyError as e:
                raise KeyError(
                    f"Label {highlight.label} not found in color mapping."
                ) from e
            html_tag = f'<span style="color:{color};">{highlight.excerpt}</span>'
            keyword_processor.add_keyword(highlight.excerpt, html_tag)

        # Apply the highlighted HTML tags
        for highlight in processed_highlights:
            color = get_color_mapping(highlight.label)
            html_tag = f'<span style="color:{color}">{highlight.excerpt}</span>'
            keyword_processor.add_keyword(highlight.excerpt, html_tag)

        html_story = keyword_processor.replace_keywords(
            self.story.title + "\n" + self.story.story
        )

        self.html_story = html_story

    def __str__(self):
        labeled_text = (
            "\n".join(str(highlight) for highlight in self.highlights)
            if self.highlights
            else "No highlights"
        )

        return f"### Reddit Story\n\n{self.story.title}\n{self.story.story}\n\n#### Labeled Text: \n\n{labeled_text}"

    def __repr__(self):
        # get useful stats
        num_highlights = len(self.highlights)
        num_words = len(self.story.story.split())
        num_chars = len(self.story.story)
        return f"<StoryHighlights story={self.story.title} num_highlights={num_highlights} num_words={num_words} num_chars={num_chars}>"

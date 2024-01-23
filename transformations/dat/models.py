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
    substring_file_path: str = ""

    def __init__(self, **data):
        super().__init__(**data)
        self.create_substring_file()

    def create_substring_file(self):
        file_hash = hash(self.story)
        filepath = os.getcwd() + f"/{file_hash}.idx"
        if os.path.exists(filepath):
            self.substring_file_path = filepath
            return
        writer = psss.Writer(filepath)
        writer.add_entry(self.story)
        writer.finalize()
        self.substring_file_path = filepath


class Label(BaseModel):
    label: str
    excerpt: str

    def __str__(self):
        return f'- **{self.label}**: "{self.excerpt}"'


class LabeledStory(BaseModel):
    story: Story
    labels: List[Label]
    html_story: str = None

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

    def find_all_matches(self):
        reader = psss.Reader(index_file_path=self.story.substring_file_path)
        matches = {}
        for label in self.labels:
            excerpt = label.excerpt.strip('"')
            matches[excerpt] = reader.search(excerpt)
        return matches

    def resolve_ties(self, matches):
        # TODO: Implement proximity-based tie-breaking logic
        raise NotImplementedError

    def apply_html_tags_keywords(self):
        from transformations.dat.colors import get_color_mapping
        keyword_processor = KeywordProcessor()
        for label in self.labels:
            try:
                color = get_color_mapping(label.excerpt)
            except KeyError:
                color = "#000000"  # Default to black if color mapping not found
            html_tag = f'<span style="color:{color};">{label.excerpt}</span>'
            keyword_processor.add_keyword(label.excerpt, html_tag)

        html_story = keyword_processor.replace_keywords(self.story.story)

        return html_story

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

    # def apply_html_tags(self, color_mapping):
    #     html_story = self.story.story
    #
    #     for label in self.labels:
    #         try:
    #             color = color_mapping[label.label]
    #         except KeyError:
    #             raise KeyError(f"Label {label.label} not found in color mapping.")
    #
    #         html_tag = f'<span style="color:{color};">{label.excerpt}</span>'
    #         escaped_excerpt = re.escape(label.excerpt.strip('"'))
    #         pattern = rf"(\b|\s|^)({escaped_excerpt})(\b|\s|$)"
    #         html_story = re.sub(pattern, r"\1" + html_tag + r"\3", html_story)
    #
    #     return html_story

    def __str__(self):
        labeled_text = "\n".join(str(label) for label in self.labels)

        return f"""### Reddit Story\n
        {self.story.title}\n
        {self.story.story}\n\n
        #### Labeled Text:\n\n
        {self.labeled_text}
        """

    # TODO: ensure we don't have fucky formatting when matching, add fuzzy matching or lemmatization-based matching.


class HTMLStory(BaseModel):
    story: Story
    labels: List[Label]

    def find_all_matches(self):
        reader = psss.Reader(index_file_path=self.story.substring_file_path)
        matches = {}
        for label in self.labels:
            excerpt = label.excerpt.strip('"')
            matches[excerpt] = reader.search(excerpt)
        return matches

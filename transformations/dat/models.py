from spacy import load
from typing import List, Any
from pydantic import BaseModel
import re
import pysubstringsearch as psss
import os
import snoop

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

    def apply_html_tags(self, color_mapping):
        html_story = self.story.story

        for label in self.labels:
            try:
                color = color_mapping[label.label]
            except KeyError:
                raise KeyError(f"Label {label.label} not found in color mapping.")

            html_tag = f'<span style="color:{color};">{label.excerpt}</span>'
            escaped_excerpt = re.escape(label.excerpt.strip('"'))
            pattern = rf"(\b|\s|^)({escaped_excerpt})(\b|\s|$)"
            html_story = re.sub(pattern, r"\1" + html_tag + r"\3", html_story)

        return html_story

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

    def find_all_matches(self, reference_stories=None):
        if not reference_stories:
            reader = psss.Reader(index_file_path=self.story.substring_file_path)
        matches = {}
        for label in self.labels:
            excerpt = label.excerpt.strip('"')
            matches[excerpt] = reader.search(excerpt)
        return matches

    def resolve_ties(self, matches, reference_excerpt=None):
        # TODO: Implement proximity-based tie-breaking logic
        # For now, return the first match assuming ordered text
        return matches[0] if matches else None

    def apply_html_tags(self, color_mapping, reference_stories=None):
        html_story = self.story.story
        all_matches = self.find_all_matches(reference_stories)

        for label in self.labels:
            excerpt = label.excerpt.strip('"')
            match_positions = all_matches[excerpt]

            if len(match_positions) > 1:
                chosen_match = self.resolve_ties(match_positions)
            else:
                chosen_match = match_positions[0] if match_positions else None

            if chosen_match:
                color = color_mapping.get(label.label, "#000000")
                html_tag = f'<span style="color:{color};">{label.excerpt}</span>'
                pattern = re.escape(chosen_match)
                html_story = re.sub(
                    pattern, html_tag, html_story, 1
                )  # Apply the tag only to the chosen match

        return html_story

from spacy import load
from typing import List
from pydantic import BaseModel
import re


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

    @classmethod
    def from_markdown(
        cls, markdown_text: str, story_text: str, story_title: str = "Story Title"
    ):
        # Fix regex pattern to handle empty excerpts
        label_pattern = re.compile(r'- \*\*(.*?)\*\*: "(.*?)"\s*')
        labels = []
        
        for match in label_pattern.finditer(markdown_text):
            label, excerpt = match.groups()
            labels.append(Label(label=label, excerpt=excerpt))
            
        story = Story(title=story_title, story=story_text)
        return cls(story=story, labels=labels)

    def __str__(self):
        labeled_text = "\n".join(str(label) for label in self.labels)
        
        return f"""### Reddit Story\n
        {self.story.title}\n
        {self.story.story}\n\n
        #### Labeled Text:\n\n
        {self.labeled_text}
        """

class HTMLStory(BaseModel):
    # TODO: ensure we don't have fucky formatting when matching, add fuzzy matching or lemmatization-based matching.
    pass

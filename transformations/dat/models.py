import pydantic

class Story(pydantic.BaseModel):
    title: str
    story: str
    sentences: list[str] = None

class Label(pydantic.BaseModel):
    label: str
    excerpt: str

    def __str__(self):
        return f"- **{self.label}**: \"{self.excerpt}\""

class ExampleLabeledStory(pydantic.BaseModel):
    story: Story
    labels: list[Label]

    def __str__(self):
        return f"""### Reddit Story\n
        {self.story.title}\n
        {self.story.story}\n\n
        #### Labeled Sample Text:\n\n
        {self.labels}
        """

class HTMLStory(pydantic.BaseModel):
    # TODO: use bs4 to render story as html using labels and lemmatized words
    pass
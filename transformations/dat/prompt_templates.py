system_prompt = "You are an Labeling System Specialist, who helps create interesting stories by labeling their individual parts for future post processing, according to a strict ruleset. You are meticulous and thorough, and go through the texts you label line by line to extract every detail and fulfill your stage in the processing pipeline."

user_prompt_1 = """
Hi! Please help me label my story using the following system:

### Labeling Rules for Reddit Stories

#### Characters
- **Main Male Character**: Label name, pronouns, and dialogue.
- **Other Male Characters**: Label names, pronouns, and dialogue.
- **Main Female Character**: Label name, pronouns, and dialogue.
- **Other Female Characters**: Label names, pronouns, and dialogue.
- **Antagonist/Villain**: Label name and dialogue post-revelation; pre-revelation, label as 'Unknown Role'.
- **Groups of People**: Label group dialogues.

#### Plot Elements
- **Danger or Violence**: Label acts of violence and key danger moments.
- **Important Information**: Label names of significant places, events, entities.
- **Climax or Resolution**: Label pivotal story moments.
- **Time References**: Label as 'Positive' for good/neutral references, 'Negative' for adverse references.

#### Descriptions
- **Positive Descriptions**: Label favorable descriptions.
- **Negative Descriptions**: Label unfavorable descriptions.
- **Nature Descriptions**: Label all nature-related descriptions.
- **Money and Wealth**: Label references to money, wealth, luxury.
- **Water-Related Descriptions**: Label all water body-related descriptions.

Please plan the labels for the following story:

### Reddit Story
```
$STORY
```

Initially, let's focus on planning the labels. The execution will be in the next message. """

user_follow_up_prompt = """
Thank you for the planning phase! Now, please proceed to label each line as identified, ensuring thoroughness and precision.

Please use the format `**Label**: "Specific excerpt"`. 

For example:

```
#### Labeled Sample Text:

- **Unknown Role**: "You are Death, but in a postapocalyptic world."
- **Positive Time Reference**: "Only a few survivors remain,"
- **Positive Description**: "and you're doing everything you can to help them"
- **Important Detail**: "because if the last human dies, you die as well."
- **Unknown Role**: "The survivors can't see you, but they feel your presence and noticed your effort."
- **Positive Description**: "They started to call you Life."
- **Negative Time Reference**: "Five thousand left today on all the Earth."
- **Violence/Danger**: "I cut the soul of the five thousand and first not one hour ago."

```

Your detailed and accurate labeling is crucial, as it will be extracted via a script. Please consider every line and maintain the formatting consistently. Thank you. """


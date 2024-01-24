# current goals left

- [ ] prompt should be adapted to fit our new models, usages, dynamic example generation (check transformations/dat/readme.md)
  - Easily done by just replacing a couple things in prompt_templates.py, can keep almost same logic but have to
    - [ ] split into 3 categories
      - modify generate_user_prompt to plan per category
      - modify generate_follow_up_prompt function to use 
        - an example from example_gen.py for each category in categories dict (use the get_markdown method to get a perfectly formatted example!!!!)
        - (see: test_example_gen.py) to understand how to implement
    - [ ] run off all 3 at once, asynchronously (in transformations/src/highlight_ai.py), turn 
    - [ ] parse highlights for each story
    - [ ] merge with no tiebreaking logic, save the HTML
- [ ] implement tiebreaking logic when merging multiple disparate sets of highlights
- [ ] return the HTML of the combined highlights in views.py
- [ ] verify site works, add basic auth
- [ ] deploy
- [ ] finish edit 1 and 2
- [ ] SGLang (or DSPy) the prompt


## Quick Start
The example below shows how to use sglang to answer a mulit-turn question.

### Using OpenAI Models

Then, answer a multi-turn question.
```python
from sglang import function, system, user, assistant, gen, set_default_backend, OpenAI

@function
def multi_turn_question(s, question_1, question_2):
    s += system("You are a helpful assistant.")
    s += user(question_1)
    s += assistant(gen("answer_1", max_tokens=256))
    s += user(question_2)
    s += assistant(gen("answer_2", max_tokens=256))

set_default_backend(OpenAI("gpt-3.5-turbo"))

state = multi_turn_question.run(
    question_1="What is the capital of the United States?",
    question_2="List two local attractions.",
)

for m in state.messages():
    print(m["role"], ":", m["content"])
```
## Frontend: Structured Generation Language (SGLang)

To begin with, import sglang.
```python
import sglang as sgl
```

`sglang` provides some simple primitives such as `gen`, `select`, `fork`, `image`.
You can implement your prompt flow in a function decorated by `sgl.function`.
You can then invoke the function with `run` or `run_batch`.
The system will manage the state, chat template, and parallelism for you.

### Control Flow
You can use any Python code within the function body, including control flow, nested function calls, and external libraries.

```python
@sgl.function
def control_flow(s, question):
    s += "To answer this question: " + question + ", "
    s += "I need to use a " + sgl.gen("tool", choices=["calculator", "web browser"]) + ". "

    if s["tool"] == "calculator":
        s += "The math expression is" + sgl.gen("expression")
    elif s["tool"] == "web browser":
        s += "The website url is" + sgl.gen("url")
```

### Parallelism
Use `fork` to launch parallel prompts.
Because `sgl.gen` is non-blocking, the for loop below issues two generation calls in parallel.

```python
@sgl.function
def tip_suggestion(s):
    s += (
        "Here are two tips for staying healthy: "
        "1. Balanced Diet. 2. Regular Exercise.\n\n"
    )

    forks = s.fork(2)
    for i, f in enumerate(forks):
        f += f"Now, expand tip {i+1} into a paragraph:\n"
        f += sgl.gen(f"detailed_tip", max_tokens=256, stop="\n\n")

    s += "Tip 1:" + forks[0]["detailed_tip"] + "\n"
    s += "Tip 2:" + forks[1]["detailed_tip"] + "\n"
    s += "In summary" + sgl.gen("summary")
```

### Multi Modality
Use `sgl.image` to pass an image as input.

```python
@sgl.function
def image_qa(s, image_file, question):
    s += sgl.user(sgl.image(image_file) + question)
    s += sgl.assistant(sgl.gen("answer", max_tokens=256)
```

### Constrained Decoding
Use `regex=` to specify a regular expression as a decoding constraint.

```python
@sgl.function
def regular_expression_gen(s):
    s += "Q: What is the IP address of the Google DNS servers?\n"
    s += "A: " + sgl.gen(
        "answer",
        temperature=0,
        regex=r"((25[0-5]|2[0-4]\d|[01]?\d\d?).){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)",
    )
```

### Batching
Use `run_batch` to run a batch of requests with continuous batching.

```python
@sgl.function
def text_qa(s, question):
    s += "Q: " + question + "\n"
    s += "A:" + sgl.gen("answer", stop="\n")

states = text_qa.run_batch(
    [
        {"question": "What is the capital of the United Kingdom?"},
        {"question": "What is the capital of France?"},
        {"question": "What is the capital of Japan?"},
    ],
    progress_bar=True
)
```

### Streaming
Add `stream=True` to enable streaming.

```python
@sgl.function
def text_qa(s, question):
    s += "Q: " + question + "\n"
    s += "A:" + sgl.gen("answer", stop="\n")

states = text_qa.run(
    question="What is the capital of France?",
    temperature=0.1,
    stream=True
)

for out in state.text_iter():
    print(out, end="", flush=True)
```

### Advanced Usage

```python
dimensions = ["Clarity", "Originality", "Evidence"]
@sgl.function
def essay_judge(s, essay):
    s += "Please evaluate the following essay. " + essay
    # Evaluate an essay from multiple dimensions in parallel
    forks = s.fork(len(dimensions))
    for f, dim in zip(forks, dimensions):
        f += (
                "Evaluate based on the following metric: " +
                dim + ". End your judgement with the word 'END'")
    f += "Judgment: " + f.gen("judgment", stop="END")
    # Merge judgments
    for f, dim in zip(forks, dimensions):
        s += dim + ": " + f["judgment"]
    # Generate a summary and give a score
    s += "In summary," + s.gen("summary")
    s += "I give the essay a letter grade of " +
    s += s.gen("grade", choices=["A", "B", "C", "D"])
    ret = essay_judge.run(essay="A long essay ...")
    print(ret["grade"])
```
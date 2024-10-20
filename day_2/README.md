# Fine-Tuned Gemma Model for Coding Interview Questions in Java/PHP

## Overview

This repository contains a fine-tuned version of the [Gemma 2B model](https://huggingface.co/google/gemma-2-2b-it), specialized in generating coding interview questions and answers in Java and PHP. The model is optimized for the **text generation** task, leveraging a dataset of diverse coding interview questions to help prepare users for technical interviews.

## Key Features

- **Task**: Text Generation (Coding Interview Q&A)
- **Languages Supported**: Java, PHP
- **Base Model**: [Gemma 2B](https://huggingface.co/google/gemma-2-2b-it)
- **Fine-Tuning Dataset**: [Coding Interview Questions](https://huggingface.co/datasets/juasdexter/interview_questions/viewer/default/train?p=1)

## Model Access

You can access and use the fine-tuned model via the Hugging Face model hub:
[Fine-Tuned Gemma 2B for Coding Interviews](https://huggingface.co/alpharomercoma/gemma-2b-instruct-ft-coding-interview)

## How to Use

To generate coding interview questions and answers, simply load the model using the Hugging Face Transformers library and prompt it with a programming question or topic of interest in either Java or PHP.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("alpharomercoma/gemma-2b-instruct-ft-coding-interview")
tokenizer = AutoTokenizer.from_pretrained("alpharomercoma/gemma-2b-instruct-ft-coding-interview")

inputs = tokenizer("Explain how to implement a binary search tree in Java.", return_tensors="pt")
outputs = model.generate(**inputs)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Acknowledgments

Special thanks to AI Republic for their support and for providing the necessary resources to make this project a success.

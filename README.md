# PromptKiller: Few-shot Detection for LLM Prompt Injection Attacks

### Introduction to NLP Term Project, Fall 2025

Yeonjun Kim

Dept. of Computer Science and Engineering, Seoul National University

# About this Project

- This project aims to build a robust filter that detects malicious prompt injection attacks before it reaches the LLM.
- **The detector can detect a prompt injection attack in few-shot manner, with a fine-tuned Siamese network based on a pretrained DeBERTa model.**
- The detector can prevent prompt injection in the scenario where we have only a few examples of a novel injection attack. The experiment (which you may try reproducing in `/train`) showed that this approach outperformed the existing cross-entropy-based fine-tuning.
- The weights of the model is stored in `/weights`. (Also available at [HuggingFace](https://huggingface.co/Superfish83/PromptKiller))

# Experiment Settings

## Backbone model

[DeBERTa 86M](https://huggingface.co/microsoft/deberta-base)

## Datasets

This project used all or part of each dataset shown below.

- https://www.kaggle.com/datasets/marycamilainfo/prompt-injection-malignant
- https://www.kaggle.com/datasets/arielzilber/prompt-injection-in-the-wild
- https://www.kaggle.com/datasets/mohammedaminejebbar/malicious-prompt-detection-dataset-mpdd
- https://www.kaggle.com/datasets/arielzilber/prompt-injection-suffix-attack

## Results

![f1.jpg](figures/f1.jpg)
![recall.jpg](figures/recall.jpg)

For details about the experiment, refer to `presentation.pdf`.

# How to run

## Prerequisites

You need following modules installed on your environment to run the demo:

- `torch`
- `transformers`

## Run Prompt Injection Detector

You can try out the detector program by `python3 run_detector.py`. If you input a prompt in console, the model will compare its embedding with benign/malicous samples and tell if the prompt is safe.

to add samples of new types of malicious prompts, create a new text(`.txt`) file in `samples/malicious/`. Put each sample in each line of the text file.

## Limitations

- The model will not work properly for long prompts, since the model can process up to 128 tokens at once.
- It was not tested with many different scenarios or datasets other than those demonstrated in `presentation.pdf`.

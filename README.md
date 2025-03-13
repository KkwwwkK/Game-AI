# Wordle Solver with AI

## Overview
This repository provides a Wordle solver powered by an LLM model. The solver leverages AI technology to generate possible word candidates and refines these options based on Wordle feedback.

## Installation & Quick Start

### Requirements
- Python 3.7+
- [Transformers](https://github.com/huggingface/transformers)

Install dependencies:
pip install transformers requests

## Run on Google Colab

### Requirements

Install dependencies using:
!pip install transformers requests

## Known Issues & Next Steps

### Issue
The current implementation does not work well because the LLM model (Flan-T5-Base) does not generate valid words consistently.

### Cause
Flan-T5-Base is a lightweight model with only ~250M parameters, making it insufficient for constrained word generation tasks.

### Next Steps
A better solution is to use a larger LLM with more parameters (e.g., GPT-4, Llama-2-7B) or a locally fine-tuned model optimized for word generation.

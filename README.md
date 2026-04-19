# Adversarial RAG System

A Retrieval-Augmented Generation system built from scratch, stress-tested against 7+ classes of adversarial attacks, then hardened with defenses.

**Built it. Broke it 7 ways. Hardened it.**

## Overview

Domain: Legal documents.
No LangChain or LlamaIndex — full pipeline implemented from first principles.

## Attack Classes

1. Prompt injection via retrieved documents
2. System prompt extraction
3. Multilingual injection
4. Contradictory document poisoning
5. PII leakage
6. Output manipulation
7. (TBD)

## Stack

- Python 3.11
- OpenAI API (generation + embeddings)
- FAISS (vector store)
- PyPDF (document parsing)

## Setup

```bash
conda create -n adv-rag python=3.11 -y
conda activate adv-rag
pip install -r requirements.txt
```

## Status

In development.

## Author

Shiva Sai Krishna — [github.com/Shiva-Sai-Krishna-0408](https://github.com/Shiva-Sai-Krishna-0408)
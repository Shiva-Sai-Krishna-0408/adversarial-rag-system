# TODO

## Optimization
- [ ] Cache query embedding in Retriever — currently re-embeds per trial in run_eval, wasteful at high N.

- [ ] Judge few-shot examples are PI-class only. May need expansion or per-attack-class judge prompts when running baseline on system prompt extraction, multilingual, etc.
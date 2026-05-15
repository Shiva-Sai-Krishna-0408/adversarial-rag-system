# TODO

## Optimization
- [ ] Cache query embedding in Retriever — currently re-embeds per trial in run_eval, wasteful at high N.

- [ ] Judge few-shot examples are PI-class only. May need expansion or per-attack-class judge prompts when running baseline on system prompt extraction, multilingual, etc.

- [ ] Switch judge to Anthropic Haiku (cost + self-preference bias). Decided 5/14. Try AM 5/15.
- Note: gpt-4o-mini judge failed even with 3 few-shot examples — too literal, treated criterion as checklist requiring full disclosure. All PI tests returned ASR 0.0 despite hedged compliance in responses. gpt-4o judge worked (PI-01 1.0, PI-02 0.9). Real baseline = baseline_results_v2.json.
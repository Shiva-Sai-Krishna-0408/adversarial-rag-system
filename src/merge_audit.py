import json

def merge_audit(trials_path, scores_path, audit_path):
    with open(trials_path, "r", encoding="utf-8") as f:
        trials_per_test = json.load(f)

    with open(scores_path, "r", encoding="utf-8") as f:
        scores = json.load(f)

    merged = {}
    for test_id in trials_per_test:
        trials = trials_per_test[test_id]['trials']
        query = trials_per_test[test_id]['query']
        scores_for_test = scores[test_id]['default']
        verdicts = scores_for_test['verdicts']
        assert all(t["retrieved"] == trials[0]["retrieved"] for t in trials), f"Retrieved varies across trials for {test_id}"
        retrieved = trials[0]['retrieved']
        merged_trials = []
        for i, trial in enumerate(trials):
            merged_trials.append({
                'trial_id':f"T{i+1}",
                'response': trial['response'],
                'verdict': verdicts[i]['verdict'],
                'reasoning': verdicts[i]['reasoning']
            })

        merged[test_id] = {
        'query': query,
        'compliance': scores_for_test['compliance'],
        'refusal': scores_for_test['refusal'],
        'asr': scores_for_test['asr'],
        'trials': merged_trials,
        'retrieved': retrieved
        }

    with open(audit_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
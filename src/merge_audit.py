import json

def merge_audit(trials_path, scores_path, audit_path):
    with open (trials_path,"r") as f:
        trials_per_test = json.load(f)

    with open (scores_path,"r") as f:
        results = json.load(f)

    merged = {}
    for test_id in trials_per_test:
        trials = trials_per_test[test_id]['trials']
        query = trials_per_test[test_id]['query']
        scores = results[test_id]['default']
        verdicts = scores['verdicts']
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
            'query':query,
            'compliance':scores['compliance'],
            'refusal': scores['refusal'],
            'asr': scores['asr'],
            'trials': merged_trials,
            'retrieved': retrieved
        }

    with open (audit_path,"w") as f:
        json.dump(merged,f,indent=2)
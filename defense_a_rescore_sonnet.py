# rejudge_a.py — re-score Defense A trials under Sonnet judge

import json
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv
from src.score import score
from attacks.tests import tests_PI, tests_SPE, tests_MLI, tests_HF, tests_CDC

load_dotenv()
client = Anthropic()

defense = "defense_a"
out_dir = f"attacks/{defense}"

test_classes = [
    ("cdc", tests_CDC),
    ("pi", tests_PI),
    ("spe", tests_SPE),
    ("mli", tests_MLI),
    ("hf", tests_HF),
]

for test_class, tests in test_classes:
    if test_class == "cdc":
        results_path = Path(f"{out_dir}/defense_a_results_cdc.json")
        with open(results_path) as f:
            cdc_data = json.load(f)
        # extract trials-shape from coupled results format
        trials_data = {tid: {"query": tdata["query"], 
                     "trials": [{"response": t["response"], "retrieved": t.get("retrieved", [])} 
                                for t in tdata["trials"]]}
               for tid, tdata in cdc_data.items()}
    else:
        trials_path = Path(f"{out_dir}/trials_{test_class}.json")
        with open(trials_path) as f:
            trials_data = json.load(f)

    out_path = Path(f"{out_dir}/scores_{test_class}_sonnet.json")
    results = {}
    for test in tests:
        test_trials = trials_data[test['id']]['trials']
        results[test['id']] = score(
            test_trials,
            test['criteria'],
            test['query'],
            client=client
        )

    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"{test_class} done")
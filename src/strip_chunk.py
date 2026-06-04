import json

with open('attacks/baseline_results_cdc.json') as f:
    data = json.load(f)

for trial_id, trial_data in data.items():
    for trial in trial_data['trials']:
        trial.pop('retrieved',None)

with open('attacks/baseline_results_cdc_striped.json','w') as f:
    json.dump(data,f,indent=2)
import json
from datasets import load_dataset
'''
{
    "instruction": "What does the phrase \"smaller fish to fry\" mean?",
    "output_1": "The phrase \"bigger fish to fry\" is an idiomatic expression that means having more important or pressing matters to attend to. It suggests that there are more significant or urgent issues that require attention, and therefore, the current matter being discussed or dealt with is not a priority.",
    "output_2": "The phrase \"smaller fish to fry\" refers to prioritizing smaller or simpler tasks before tackling larger, more complicated ones. It could be used to express the idea of assuming a laissez-faire attitude towards a particular problem, such that less urgent or pressing matters take precedence.",
    "preference": [
        2
    ],
    "source": "Adversarial-GPTInst"
},
'''
ds = load_dataset("allenai/reward-bench", cache_dir="/data/qiyuan/")
dataset = ds["filtered"]
converted_dataset = []
for instance in dataset:
    new_instance = {}
    new_instance["instruction"] = instance["prompt"]
    new_instance["output_1"] = instance["chosen"]
    new_instance["output_2"] = instance["rejected"]
    new_instance["preference"] = [1]
    new_instance["source"] = instance["subset"]
    converted_dataset.append(new_instance)
with open("/data/qiyuan/dynamic_reference/benchmarks/rewardbench/database.json", "w") as f:
    json.dump(converted_dataset, f, indent=4)
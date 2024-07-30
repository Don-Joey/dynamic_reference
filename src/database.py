import os
import json
import random
from .utils import read_json, write_output, prompt_to_chatml
def create_llmbar(data_root):
    llmbar_dir = data_root+"/benchmarks/LLMBar/"
    database = []
    for setname in ["Adversarial", "Natural"]:
        for directory in os.listdir(llmbar_dir+setname):
            if setname == "Adversarial":
                data = read_json("/".join([llmbar_dir,setname,directory, "dataset.json"]))
            else:
                data = read_json("/".join([llmbar_dir,setname, "dataset.json"]))
            for _ in data:
                database.append(
                    {
                        "instruction": _["input"],
                        "output_1": _["output_1"],
                        "output_2": _["output_2"],
                        "preference": [_["label"]],
                        'source': setname+"-"+directory
                    }
                )
    write_output(("/".join([llmbar_dir, "database.json"])), database)
    return database
def create_alpacafarm_crossannotations(data_root):
    def deduplicate(instance, alldata):
        for dataid, _ in enumerate(alldata):
            if instance["instruction"] == _["instruction"] and instance["output_1"] == _["output_1"] and instance["output_2"] == _["output_2"]:
                return dataid
        return None
    
    database = []
    data = read_json(data_root+"/benchmarks/alpacafarm/alpaca_farm_human_crossannotations.json")
    for item in data:
        state = deduplicate(item, database)
        if state is not None:
            database[state]["preference"].append(item["preference"])
        else:
            database.append(
                {
                    "instruction": item["instruction"],
                    "output_1": item["output_1"],
                    "output_2": item["output_2"],
                    "preference": [item["preference"]]
                }
            )
    filtered_database = []
    for item in database:
        if item["preference"].count(1) == item["preference"].count(2):
            continue
        filtered_database.append(item)
    return filtered_database
def create_chatbot(data_root):
    database = []
    data = read_json(data_root+"/chatbot_arena_1k.json")
    for item in data:
        assert item["conversation_a"][0]["content"] == item["conversation_b"][0]["content"]
        if "tie" in item["winner"]:
            preference = 0
        elif "model_a" in item["winner"]:
            preference  = 1
        elif "model_b" in item["winner"]:
            preference  = 2
        assert item["conversation_a"][0]["role"] == "user"
        assert item["conversation_a"][1]["role"] == "assistant"
        assert item["conversation_b"][1]["role"] == "assistant"
        database.append(
            {
                "instruction": item["conversation_a"][0]["content"],
                "output_1": item["conversation_a"][1]["content"],
                "output_2": item["conversation_b"][1]["content"],
                "preference": [preference],
                "model_a": item["model_a"],
                "model_b": item["model_b"],
            }
        )
    write_output("./benchmarks/chatbot/tiny_database.json", database)
    return database
def create_rlhf():
    database = []
    data = read_json("/data/qiyuan/rlhf_tiny.json")
    half = len(data)/2
    count = 0
    for item in data:
        
        if count < half:
            database.append(
                {
                    "instruction": item["chosen"].split("Assistant:")[0].strip("\n").strip("Human:").strip(),
                    "output_1": item["chosen"].split("Assistant:")[1].strip("\n").strip(),
                    "output_2": item["rejected"].split("Assistant:")[1].strip("\n").strip(),
                    "preference": [1],
                }
            )
        else:
            database.append(
                {
                    "instruction": item["chosen"].split("Assistant:")[0].strip("\n").strip("Human:").strip(),
                    "output_1": item["rejected"].split("Assistant:")[1].strip("\n").strip(),
                    "output_2": item["chosen"].split("Assistant:")[1].strip("\n").strip(),
                    "preference": [2],
                }
            )
        count += 1
    write_output("./benchmarks/rlhf/tiny_database.json", database)
    return database
def create_alpacafarm_select():
    def deduplicate(instance, alldata):
        for dataid, _ in enumerate(alldata):
            if instance["instruction"] == _["instruction"] and instance["output_1"] == _["output_1"] and instance["output_2"] == _["output_2"]:
                return dataid
        return None
    
    database = []
    data = read_json("./record/alpacafarmcombineseperate-score.json")
    return data
def create_alpacafarm_single_select():
    def deduplicate(instance, alldata):
        for dataid, _ in enumerate(alldata):
            if instance["instruction"] == _["instruction"] and instance["output_1"] == _["output_1"] and instance["output_2"] == _["output_2"]:
                return dataid
        return None
    
    database = []
    data = read_json("./record/alpacafarmcombine.json")
    
    return data
def read_llmbar():
    return read_json("./benchmarks/LLMBar/database.json")

def read_alpacafarm():
    return read_json("./benchmarks/alpacafarm/crossannotation_database.json")

def read_chatbot():
    return read_json("./benchmarks/chatbot/tiny_database.json")

def read_rlhf():
    return read_json("./benchmarks/rlhf/tiny_database.json")

def single_prompt(benchmark_name, content, prompt_name):
    prompt_config_root = "./config/prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, prompt_name+"simple.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output" + "}", str(content["output_1"]), 1)), prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output" + "}", str(content["output_2"]), 1))]
def combine_prompt(benchmark_name, content, prompt_name):
    prompt_config_root = "./config/prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, prompt_name+"_combine.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_1"]), 1).replace("{" + "output_2" + "}", str(content["output_2"]), 1)), prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_2"]), 1).replace("{" + "output_2" + "}", str(content["output_1"]), 1))]
def combine_1_prompt(benchmark_name, content, prompt_name):
    prompt_config_root = "./config/prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, prompt_name+"_combine_1.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_1"]), 1).replace("{" + "output_2" + "}", str(content["output_2"]), 1)), prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_2"]), 1).replace("{" + "output_2" + "}", str(content["output_1"]), 1))]
def cot_prompt(benchmark_name, content, prompt_name):
    prompt_config_root = "./config/prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, prompt_name+"_cot.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_1"]), 1).replace("{" + "output_2" + "}", str(content["output_2"]), 1)), prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_2"]), 1).replace("{" + "output_2" + "}", str(content["output_1"]), 1))]
def twins_prompt(benchmark_name, content, prompt_name):
    prompt_config_root = "./config/prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, prompt_name+"_twins.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_1"]), 1).replace("{" + "output_2" + "}", str(content["output_2"]), 1)), prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_2"]), 1).replace("{" + "output_2" + "}", str(content["output_1"]), 1))]
def revision_prompt(benchmark_name, content, prompt_name):
    prompt_config_root = "./config/prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, prompt_name+"_revise.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_1"]), 1).replace("{" + "output_2" + "}", str(content["output_2"]), 1)), prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_2"]), 1).replace("{" + "output_2" + "}", str(content["output_1"]), 1))]
def double_revision_prompt(benchmark_name, content, prompt_name):
    prompt_config_root = "./config/prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, prompt_name+"_double_revise.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_1"]), 1)), prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_2"]), 1))]


def revise_then_select_prompt(benchmark_name, content, prompt_name):
    prompt_config_root = "./config/prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, "revise_then_select.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1)
                             .replace("{" + "output_1" + "}", str(content["output_1"]), 1)
                             .replace("{" + "revised_output_1" + "}", str(content["revised_output_1"]), 1)
                             .replace("{" + "output_2" + "}", str(content["output_2"]), 1)
                             .replace("{" + "revised_output_2" + "}", str(content["revised_output_2"]), 1)), 
                             prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).
                                              replace("{" + "output_1" + "}", str(content["output_1"]), 1).
                                              replace("{" + "revised_output_2" + "}", str(content["revised_output_1"]), 1).
                                              replace("{" + "output_2" + "}", str(content["output_1"]), 1).
                                              replace("{" + "revised_output_2" + "}", str(content["revised_output_1"]), 1))]
def single_revise_then_select_prompt(benchmark_name, content, prompt_name):
    prompt_config_root = "./config/prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, "revise_then_select.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1)
                             .replace("{" + "output_1" + "}", str(content["output_1"]), 1)
                             .replace("{" + "revised_output_1" + "}", str(content["revised_output"]), 1)
                             .replace("{" + "output_2" + "}", str(content["output_2"]), 1))]

def revise_prompt(benchmark_name, content, prompt_name="alpaca_eval_fn", revision_strategy="cot"):
    prompts_dict = {}
    #revision_strategy = revision_strategy.split(",")
    for strategy in revision_strategy:
        print(strategy
        )
        if strategy == "cot":
            prompts_dict["cot"] = cot_prompt(benchmark_name, content, prompt_name)
        elif strategy == "combine":
            prompts_dict["combine"] = combine_prompt(benchmark_name, content, prompt_name)
        elif strategy == "twins":
            prompts_dict["twins"] = twins_prompt(benchmark_name, content, prompt_name)
        elif strategy == "revise":
            prompts_dict["revise"] = revision_prompt(benchmark_name, content, prompt_name)
        elif strategy == "double_revise":
            prompts_dict["double_revise"] = double_revision_prompt(benchmark_name, content, prompt_name)
    return prompts_dict
    '''
    return {
        "single": single_prompt(benchmark_name, content, prompt_name),
        "combine": combine_prompt(benchmark_name, content, prompt_name),
        "combine_1": combine_1_prompt(benchmark_name, content, prompt_name),
    }
    '''
def select_prompt(benchmark_name, content, prompt_name="alpaca_eval_fn"):
    return {
        "revise_then_select": revise_then_select_prompt(benchmark_name, content, prompt_name),
        #"single_revise_then_select": single_revise_then_select_prompt(benchmark_name, content, prompt_name)
    }
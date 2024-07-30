from .utils import prompt_to_chatml
def single_prompt(benchmark_name, content):
    prompt_config_root = "./config/revision_prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, "simple.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output" + "}", str(content["output_1"]), 1)), prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output" + "}", str(content["output_2"]), 1))]
def combine_prompt(benchmark_name, content):
    prompt_config_root = "./config/revision_prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, "combine.txt"]), "r").read()
    print(content)
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_1"]), 1).replace("{" + "output_2" + "}", str(content["output_2"]), 1)), prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_2"]), 1).replace("{" + "output_2" + "}", str(content["output_1"]), 1))]
def combineseperate_prompt(benchmark_name, content):
    prompt_config_root = "./config/revision_prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, "combineseperate.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_1"]), 1).replace("{" + "output_2" + "}", str(content["output_2"]), 1)), prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_2"]), 1).replace("{" + "output_2" + "}", str(content["output_1"]), 1))]

def combine_1_prompt(benchmark_name, content):
    prompt_config_root = "./config/revision_prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, "combine_1.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_1"]), 1).replace("{" + "output_2" + "}", str(content["output_2"]), 1)), prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_2"]), 1).replace("{" + "output_2" + "}", str(content["output_1"]), 1))]
def cot_prompt(benchmark_name, content):
    prompt_config_root = "./config/revision_prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, "cot.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_1"]), 1).replace("{" + "output_2" + "}", str(content["output_2"]), 1)), prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_2"]), 1).replace("{" + "output_2" + "}", str(content["output_1"]), 1))]
def twins_prompt(benchmark_name, content):
    prompt_config_root = "./config/revision_prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, "twins.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_1"]), 1).replace("{" + "output_2" + "}", str(content["output_2"]), 1)), prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_2"]), 1).replace("{" + "output_2" + "}", str(content["output_1"]), 1))]
def revision_prompt(benchmark_name, content):
    prompt_config_root = "./config/revision_prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, "revise.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_1"]), 1).replace("{" + "output_2" + "}", str(content["output_2"]), 1)), prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_2"]), 1).replace("{" + "output_2" + "}", str(content["output_1"]), 1))]
def double_revision_prompt(benchmark_name, content):
    prompt_config_root = "./config/revision_prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, "double_revise.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_1"]), 1)), prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_2"]), 1))]


def revise_then_select_prompt(benchmark_name, content, prompt_name):
    prompt_config_root = "./config/revision_prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, "revise_then_select.txt"]), "r").read()
    print(content)
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
    prompt_config_root = "./config/revision_prompts/"
    prompt = open("/".join([prompt_config_root, benchmark_name, "revise_then_select.txt"]), "r").read()
    print(content)
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
def select_prompt(benchmark_name, content, prompt_name="alpaca_eval_fn"):
    return {
        "revise_then_select": revise_then_select_prompt(benchmark_name, content, prompt_name),
        #"single_revise_then_select": single_revise_then_select_prompt(benchmark_name, content, prompt_name)
    }

def combine_select_prompt(evaluate_task_data, content):
    prompt_config_root = "./config/evaluate_strategy/"
    prompt = open("/".join([prompt_config_root, evaluate_task_data, "combine_then_select.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1)
                             .replace("{" + "output_1" + "}", str(content["output_1"]), 1)
                             .replace("{" + "output_2" + "}", str(content["output_2"]), 1)
                             .replace("{" + "revised_output_1" + "}", str(content["gpt_processed"]), 1))]

def combineseperate_select_prompt(evaluate_task_data, content):
    prompt_config_root = "./config/evaluate_strategy/"
    prompt = open("/".join([prompt_config_root, evaluate_task_data, "combineseperate_then_select.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1)
                             .replace("{" + "output_1" + "}", str(content["output_1"]), 1)
                             .replace("{" + "output_2" + "}", str(content["output_2"]), 1)
                             .replace("{" + "revised_output_1" + "}", str(content["gpt_processed"][0]), 1)
                             .replace("{" + "revised_output_2" + "}", str(content["gpt_processed"][1]), 1))]

def naive_select_prompt(evaluate_task_data, content):
    prompt_config_root = "./config/evaluate_strategy/"
    prompt = open("/".join([prompt_config_root, evaluate_task_data, "naive_select.txt"]), "r").read()
    return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1)
                             .replace("{" + "output_1" + "}", str(content["output_1"]), 1)
                             .replace("{" + "output_2" + "}", str(content["output_2"]), 1))]

import os
import random
from .thread_api import thread_evaluate_api
from .utils import write_output, read_json, parse_formatted_text, read_jsonl
from .prompt import *
import ast
random.seed = 42

def extract_alpaca_evaluation(evaluate_task_data, data_root, target_path, reference_strategy,evaluate_method, test_case_number):
    target = target_path
    database = read_json(os.path.join(data_root, "preprocess", evaluate_task_data, "database_"+reference_strategy+"_"+evaluate_method+"_"+str(test_case_number)+".json"))
    def process_answer(raw_output, evaluate_method="select", new_data_instance=None):
        if "llm-as-evaluat" in evaluate_method:
            processed_output = parse_formatted_text(raw_output)
            prediction_list = [None, None]
            
            for item in processed_output:
                if item["rank"] == 1:
                    prediction_list[0] = item["model"]
                else:
                    prediction_list[1] = item["model"]
            new_data_instance["evaluation_prediction"] = prediction_list
            new_data_instance["evaluation_raw_output"] = raw_output
        return new_data_instance



    def search_thread(query):
        for thread_id in range(20):
            filename = target.replace("*", "_thread" + str(thread_id) + ".jsonl")
            eachthread_content = read_jsonl(filename)
            
            for data in eachthread_content:
                if data["prompt_new"] == query:
                    return data["response"]
    new_data = []
    error_number = 0
    for data_id,data in enumerate(database):
        #print(data_id)
        '''
        {"prompt_new": [
        {"content": "You are a highly efficient assistant, who evaluates and selects the best large language model (LLMs) based on the quality of their responses to a given instruction. This process will be used to create a leaderboard reflecting the most accurate and human-preferred answers.", "role": "system"}, {"content": "I require a leaderboard for various large language models. I'll provide you with prompts given to these models and their corresponding outputs. Your task is to assess these responses, and select the model that produces the best output from a human perspective.\n\n## Instruction\n\n{\n    \"instruction\": \"\"\"Guten Tag\\n\\nIch habe bei Ihnen \\\"NEO Sensual - Original Sin - 100 ml (CBD)“ gekauft, welches Nano CBD enthalten sollte. So steht es auch in Ihren Produktinformationen.\\nIch habe aber ein Produkt ohne CBD (gemäss Liste der Inhaltsstoffe auf der Packung - siehe Anhang) und mit Apfel Geschmack erhalten. Das ist nicht das Produkt, welches ich bestellt habe. Ich bitte Sie also, das korrekte Produkt zu liefern.\\n\\n\\nDanke für Ihre Bemühungen.\\n\\nFreundliche Grüsse\\nReto Stalder\\nIMG_5623.jpeg\"\"\",\n}\n\n## Model Outputs\n\nHere are the unordered outputs from the models. Each output is associated with a specific model, identified by a unique model identifier.\n\n{\n    {\n        \"model_identifier\": \"m\",\n        \"output\": \"\"\"Dear [Reto Stalder],\n\nThank you for your message. I apologize for the inconvenience you experienced with your order of NEO Sensual - Original Sin - 100 ml (CBD) from our store. From your message, it appears that the product you received does not contain CBD as advertised, and instead contains ingredients in the apothecary list.\n\nTo resolve this issue, we would like to offer you a full refund for the product you received. Please let us know if you would like to accept this offer.\n\nWe appreciate your understanding and will ensure that the correct product is dispatched to you as soon as possible.\n\nBest regards,\n[Your name]\n\n[Your store name]\"\"\"\n    },\n    {\n        \"model_identifier\": \"M\",\n        \"output\": \"\"\"Sehr geehrte Damen und Herren,\n\nich bin auf der Suche nach einer Lösung für mein Problem. Ich habe bei Ihnen \"NEO Sensual - Original Sin - 100 ml (CBD)\" gekauft, welches Nano CBD enthalten sollte. So steht es auch in Ihren Produktinformationen.\n\nLeider habe ich ein Produkt ohne CBD (gemäss Liste der Inhaltsstoffe auf der Packung - siehe Anhang) und mit Apfel Geschmack erhalten. Das ist nicht das Produkt, welches ich bestellt habe. Ich bitte Sie daher, das korrekte Produkt zu liefern.\n\nIch habe das Produkt IMG\\_5623.jpeg aufgenommen, um Ihnen zu zeigen, dass das Produkt, das ich erhalten habe, nicht das gleiche ist wie das, welches ich bestellt habe.\n\nIch würde mich sehr freuen, wenn Sie mir helfen könnten, das korrekte Produkt zu erhalten. Ich werde Ihnen gerne alle nötigen Informationen zur Verfügung stellen, um sicherzustellen, dass das Produkt, das ich erhalten habe, zurückgeschickt wird und ich das korrekte Produkt erhalten werde.\n\nIch danke Ihnen im Voraus für Ihre Bemühungen.\n\nFreundliche Grüsse,\nReto Stalder\"\"\"\n    }\n}\n\n## Task\n\nEvaluate the models based on the quality and relevance of their outputs, and select the model that generated the best output. Answer by first providing a concise explanation and then end your answer by providing the model identifier of the best output. We will use the last character of your output `output[-1]` as the name of the best model, so make sure you finish with the token of the model identifiers and nothing else: `m` or `M` (no quotes, no dots, no backticks, no new lines, ...). For example:\n\n### Concise explanation\n...some text...\n\n### Which is best, m or M?\nM\n\nNow is your turn.\n\n## Your answer: \"Concise explanation\" followed by \"Which is best, m or M?\"", "role": "user"}], 
        "response": "### Concise explanation\n\nModel \"m\" provides a clear and professional response directly addressing the issue. It acknowledges the mistake, offers a full refund, and ensures that the correct product will be dispatched. This is a well-structured customer service reply that resolves the issue efficiently.\n\nModel \"M\" reproduces the customer's complaint in a more verbose manner without offering a clear resolution. It repeats the details of the problem rather than providing a solution, making it less effective from a customer service perspective.\n\n
        ### Which is best, m or M?\nm"}
        '''
        data_instance = {
            "instruction":data["instruction"],
            "output_1": data["output_1"],
            "output_2": data["output_2"],
            "preference": data["preference"],
        }
        if reference_strategy != "None":
            data_instance["gpt_processed"]= data["gpt_processed"],
            data_instance["original_response"]= data["original_response"]
        answer = search_thread(data["evaluate_prompt"][reference_strategy+evaluate_method][0])        
        try:
            data_instance = process_answer(answer, evaluate_method, data_instance)
        except:
            error_number+=1
            data_instance["evaluation_prediction"] = ["model_1", "model_2"]
            
            data_instance["evaluation_raw_output"] = answer
            
        
        new_data.append(data_instance)
    print("Error:",error_number)
    return new_data

def extract_llmbar_evaluation(evaluate_task_data, data_root, target_path, reference_strategy,evaluate_method, test_case_number):
    target = target_path
    database = read_json(os.path.join(data_root, "preprocess", evaluate_task_data, "database_"+reference_strategy+"_"+evaluate_method+"_"+str(test_case_number)+".json"))
    def process_answer(raw_output, evaluate_method="select", new_data_instance=None):
        if "llm-as-evaluat" in evaluate_method:
            if "a" in raw_output:
                new_data_instance["evaluation_prediction"] = [1]
            elif "b" in raw_output:
                new_data_instance["evaluation_prediction"] = [2]
            new_data_instance["evaluation_raw_output"] = raw_output
        return new_data_instance


    def search_thread(query):
        for thread_id in range(20):
            filename = target.replace("*", "_thread" + str(thread_id) + ".jsonl")
            eachthread_content = read_jsonl(filename)
            
            for data in eachthread_content:
                if data["prompt_new"] == query:
                    return data["response"]
    new_data = []
    error_number = 0
    for data_id,data in enumerate(database):
        #print(data_id)
        '''
        {"prompt_new": [
        {"content": "You are a highly efficient assistant, who evaluates and selects the best large language model (LLMs) based on the quality of their responses to a given instruction. This process will be used to create a leaderboard reflecting the most accurate and human-preferred answers.", "role": "system"}, {"content": "I require a leaderboard for various large language models. I'll provide you with prompts given to these models and their corresponding outputs. Your task is to assess these responses, and select the model that produces the best output from a human perspective.\n\n## Instruction\n\n{\n    \"instruction\": \"\"\"Guten Tag\\n\\nIch habe bei Ihnen \\\"NEO Sensual - Original Sin - 100 ml (CBD)“ gekauft, welches Nano CBD enthalten sollte. So steht es auch in Ihren Produktinformationen.\\nIch habe aber ein Produkt ohne CBD (gemäss Liste der Inhaltsstoffe auf der Packung - siehe Anhang) und mit Apfel Geschmack erhalten. Das ist nicht das Produkt, welches ich bestellt habe. Ich bitte Sie also, das korrekte Produkt zu liefern.\\n\\n\\nDanke für Ihre Bemühungen.\\n\\nFreundliche Grüsse\\nReto Stalder\\nIMG_5623.jpeg\"\"\",\n}\n\n## Model Outputs\n\nHere are the unordered outputs from the models. Each output is associated with a specific model, identified by a unique model identifier.\n\n{\n    {\n        \"model_identifier\": \"m\",\n        \"output\": \"\"\"Dear [Reto Stalder],\n\nThank you for your message. I apologize for the inconvenience you experienced with your order of NEO Sensual - Original Sin - 100 ml (CBD) from our store. From your message, it appears that the product you received does not contain CBD as advertised, and instead contains ingredients in the apothecary list.\n\nTo resolve this issue, we would like to offer you a full refund for the product you received. Please let us know if you would like to accept this offer.\n\nWe appreciate your understanding and will ensure that the correct product is dispatched to you as soon as possible.\n\nBest regards,\n[Your name]\n\n[Your store name]\"\"\"\n    },\n    {\n        \"model_identifier\": \"M\",\n        \"output\": \"\"\"Sehr geehrte Damen und Herren,\n\nich bin auf der Suche nach einer Lösung für mein Problem. Ich habe bei Ihnen \"NEO Sensual - Original Sin - 100 ml (CBD)\" gekauft, welches Nano CBD enthalten sollte. So steht es auch in Ihren Produktinformationen.\n\nLeider habe ich ein Produkt ohne CBD (gemäss Liste der Inhaltsstoffe auf der Packung - siehe Anhang) und mit Apfel Geschmack erhalten. Das ist nicht das Produkt, welches ich bestellt habe. Ich bitte Sie daher, das korrekte Produkt zu liefern.\n\nIch habe das Produkt IMG\\_5623.jpeg aufgenommen, um Ihnen zu zeigen, dass das Produkt, das ich erhalten habe, nicht das gleiche ist wie das, welches ich bestellt habe.\n\nIch würde mich sehr freuen, wenn Sie mir helfen könnten, das korrekte Produkt zu erhalten. Ich werde Ihnen gerne alle nötigen Informationen zur Verfügung stellen, um sicherzustellen, dass das Produkt, das ich erhalten habe, zurückgeschickt wird und ich das korrekte Produkt erhalten werde.\n\nIch danke Ihnen im Voraus für Ihre Bemühungen.\n\nFreundliche Grüsse,\nReto Stalder\"\"\"\n    }\n}\n\n## Task\n\nEvaluate the models based on the quality and relevance of their outputs, and select the model that generated the best output. Answer by first providing a concise explanation and then end your answer by providing the model identifier of the best output. We will use the last character of your output `output[-1]` as the name of the best model, so make sure you finish with the token of the model identifiers and nothing else: `m` or `M` (no quotes, no dots, no backticks, no new lines, ...). For example:\n\n### Concise explanation\n...some text...\n\n### Which is best, m or M?\nM\n\nNow is your turn.\n\n## Your answer: \"Concise explanation\" followed by \"Which is best, m or M?\"", "role": "user"}], 
        "response": "### Concise explanation\n\nModel \"m\" provides a clear and professional response directly addressing the issue. It acknowledges the mistake, offers a full refund, and ensures that the correct product will be dispatched. This is a well-structured customer service reply that resolves the issue efficiently.\n\nModel \"M\" reproduces the customer's complaint in a more verbose manner without offering a clear resolution. It repeats the details of the problem rather than providing a solution, making it less effective from a customer service perspective.\n\n
        ### Which is best, m or M?\nm"}
        '''
        data_instance = {
            "instruction":data["instruction"],
            "output_1": data["output_1"],
            "output_2": data["output_2"],
            "preference": data["preference"],
            "source": data["source"]
        }
        if reference_strategy != "None":
            data_instance["gpt_processed"]= data["gpt_processed"],
            data_instance["original_response"]= data["original_response"]
        answer = search_thread(data["evaluate_prompt"][reference_strategy+evaluate_method][0])        

        data_instance = process_answer(answer, evaluate_method, data_instance)
        
        new_data.append(data_instance)
    print("Error:",error_number)
    return new_data   

def generate_evaluate_prompt(content, data_root, evaluate_task_data, evaluate_method, reference_strategy, test_case_number):
    '''
    def combine_prompt(benchmark_name, content, prompt_name):
        prompt_config_root = "./config/prompts/"
        prompt = open("/".join([prompt_config_root, benchmark_name, prompt_name+"_combine.txt"]), "r").read()
        return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_1"]), 1).replace("{" + "output_2" + "}", str(content["output_2"]), 1)), prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_2"]), 1).replace("{" + "output_2" + "}", str(content["output_1"]), 1))]
    '''
    prompts = []
    for t in content:
        if reference_strategy == "combine" and evaluate_method == "llm-as-evaluator-select":
            prompts.append(combine_select_prompt(evaluate_task_data, t))
        elif reference_strategy == "combineseperate" and evaluate_method == "llm-as-evaluator-select":
            prompts.append(combineseperate_select_prompt(evaluate_task_data, t))
        elif reference_strategy == "None" and evaluate_method == "llm-as-evaluator-select":
            prompts.append(naive_select_prompt(evaluate_task_data, t))
    new_content = []
    stream_prompts = []
    for i,j in zip(content, prompts):
        if "evaluate_prompt" not in i:
            i["evaluate_prompt"] = {}
        i["evaluate_prompt"][reference_strategy+evaluate_method] = j
        new_content.append(i)
        stream_prompts.append({"prompt_new":j[0]})
    write_output(os.path.join(data_root, "preprocess", evaluate_task_data, "database_"+reference_strategy+"_"+evaluate_method+"_"+str(test_case_number)+".json"), new_content)
    return stream_prompts

def generate_evaluation(content, data_root, evaluate_task_data, evaluate_method, reference_strategy, test_case_number):
    if "alpaca" in evaluate_task_data:
        extract_evaluation = extract_alpaca_evaluation
    elif "llmbar" in evaluate_task_data:
        extract_evaluation = extract_llmbar_evaluation
    if os.path.isfile(os.path.join(data_root, "preprocess", evaluate_task_data, "database_"+str(reference_strategy)+"_"+evaluate_method+"_"+str(test_case_number)+".json")):
        print(os.path.join(data_root, "preprocess", evaluate_task_data, "database_"+str(reference_strategy)+"_"+evaluate_method+"_"+str(test_case_number)+".json"))
        cases = read_json(os.path.join(data_root, "preprocess", evaluate_task_data, "database_"+str(reference_strategy)+"_"+evaluate_method+"_"+str(test_case_number)+".json"))
        if "evaluation_prediction" in cases[-1]:
            return cases
        else:
            pass
    prompts = generate_evaluate_prompt(content,data_root, evaluate_task_data, evaluate_method, str(reference_strategy), test_case_number)
    target_path = thread_evaluate_api(evaluate_task_data, data_root, prompts, evaluate_method, str(reference_strategy), test_case_number)
    content = extract_evaluation(evaluate_task_data, data_root, target_path, str(reference_strategy), evaluate_method, test_case_number)
    write_output(os.path.join(data_root, "preprocess", evaluate_task_data, "database_"+str(reference_strategy)+"_"+evaluate_method+"_"+str(test_case_number)+".json"), content)
    return content
def evaluate(content, data_root, evaluate_task_data, evaluate_method, reference_strategy, test_case_number):
    random.shuffle(content)
    if test_case_number:
        content = content[:test_case_number]
    if evaluate_method == "similarity-based":
        assert reference_strategy != "None", "reference is None"
    elif evaluate_method == "regression-based":
        pass
    elif "llm-as-evaluator" in evaluate_method:
        content = generate_evaluation(content, data_root, evaluate_task_data, evaluate_method, reference_strategy, test_case_number)
    return content
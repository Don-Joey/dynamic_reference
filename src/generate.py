import os
from .utils import *
from .thread_api import thread_reference_api
from .prompt import *
def generate_reference_prompt(evaluate_task_data, data_root, reference_strategy):
    '''
    def combine_prompt(benchmark_name, content, prompt_name):
        prompt_config_root = "./config/prompts/"
        prompt = open("/".join([prompt_config_root, benchmark_name, prompt_name+"_combine.txt"]), "r").read()
        return [prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_1"]), 1).replace("{" + "output_2" + "}", str(content["output_2"]), 1)), prompt_to_chatml(prompt.replace("{" + "instruction" + "}", str(content["instruction"]), 1).replace("{" + "output_1" + "}", str(content["output_2"]), 1).replace("{" + "output_2" + "}", str(content["output_1"]), 1))]
    '''
    content = read_json(os.path.join(data_root, "preprocess",evaluate_task_data, "database.json"))
    prompts = []
    for t in content:
        if reference_strategy == "combine":
            prompts.append(combine_prompt(evaluate_task_data, t))
        elif reference_strategy == "combineseperate":
            prompts.append(combineseperate_prompt(evaluate_task_data, t))
    
    new_content = []
    stream_prompts = []
    for i,j in zip(content, prompts):
        if "reference_prompt" not in i:
            i["reference_prompt"] = {}
        i["reference_prompt"][reference_strategy] = j
        new_content.append(i)
        stream_prompts.append({"prompt_new":j[0]})
    write_output(os.path.join(data_root, "preprocess", evaluate_task_data, "database_"+reference_strategy+"_prompt.json"), new_content)
    return stream_prompts
def extract_reference(evaluate_task_data, data_root, target_path, reference_strategy):
    target = target_path
    database = read_json(os.path.join(data_root, "preprocess",evaluate_task_data, "database_"+reference_strategy+"_prompt.json"))
    def process_answer(raw_output, revision_strategy = "cot", new_data_instance=None):
        if revision_strategy == "cot":
            pattern = r'Concise explanation(.*?)(?=Which is best, m or M?)'
            raw_output = raw_output.replace("Which is defines best, m or M?", "Which is best, m or M?")
            raw_output = raw_output.replace("Which is Is best, m or M?", "Which is best, m or M?")
            raw_output = raw_output.replace("Which is the best, m or M?", "Which is best, m or M?")
            raw_output = raw_output.replace("Which is best, \"m\" or \"M\"?", "Which is best, m or M?")
            raw_output = raw_output.replace("Which is there, m, or M?", "Which is best, m or M?")
            raw_output = raw_output.replace("Which is was best, m or M?", "Which is best, m or M?")
            raw_output = raw_output.replace("Which is generaly better, m or M?", "Which is best, m or M?")
            # Use re.search to extract data (re.findall could be used if multiple sections are expected)
            final_choice = raw_output.split("Which is best, m or M?")[1]
            explanation = raw_output.split("Which is best, m or M?")[0]
            processed_answer = [explanation.strip("\n").strip("#").strip("\n").strip(), final_choice.strip("\n").strip("#").strip("\n").strip()]
        elif revision_strategy == "combine" or revision_strategy == "revise":
            raw_output = raw_output.strip("Revised Response")
            processed_answer = raw_output.strip("\n").strip()
            
        elif revision_strategy == "twins":
            if "Revised(M)" in raw_output:
                raw_output = raw_output.split("Revised(M)")
            else:
                raw_output = raw_output.split("Revised (M)")
            processed_answer = [raw_output[0].strip("Revised (m)").strip("\n").strip(), raw_output[1].strip("\n").strip()]
        elif revision_strategy == "combineseperate":
            processed_answer=[]
            if raw_output.find("Revised (2)") > raw_output.find("Revised (1)"):
                if "\nRevised (2)\n" in raw_output:
                    processed_answer.append(raw_output.split("\nRevised (2)\n")[0].strip())
                    processed_answer[0] = processed_answer[0].replace("Revised (1)", "").strip("\n").strip()
                    processed_answer.append(raw_output.split("\nRevised (2)\n")[1].strip())
                else:
                    processed_answer.append(raw_output.split("Revised (2)")[0].strip("\n").strip())
                    processed_answer[0] = processed_answer[0].replace("Revised (1)", "").strip("\n").strip()
                    processed_answer.append(raw_output.split("Revised (2)")[1].strip("\n").strip())
            else:
                if "\nRevised (1)\n" in raw_output:
                    processed_answer.append(raw_output.split("\nRevised (1)\n")[0].strip())
                    processed_answer[0] = processed_answer[0].replace("Revised (2)", "").strip("\n").strip()
                    processed_answer.append(raw_output.split("\nRevised (1)\n")[1].strip())
                else:
                    processed_answer.append(raw_output.split("Revised (1)")[0].strip("\n").strip())
                    processed_answer[0] = processed_answer[0].replace("Revised (2)", "").strip("\n").strip()
                    processed_answer.append(raw_output.split("Revised (1)")[1].strip("\n").strip())


        new_data_instance["gpt_processed"] = processed_answer
        new_data_instance["original_response"] = raw_output
        return new_data_instance

    def search_thread(query):
        for thread_id in range(20):
            filename = target.replace("*", "_thread" + str(thread_id) + ".jsonl")
            eachthread_content = read_jsonl(filename)
            
            for data in eachthread_content:
                if data["prompt_new"] == query:
                    return data["response"]
    new_data = []
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
            "preference": data["preference"]
        }
        if "source" in data:
            data_instance["source"] = data["source"]
        answer = search_thread(data["reference_prompt"][reference_strategy][0])
        if answer is None:
            continue
        
        data_instance = process_answer(answer, reference_strategy, data_instance)            
        
        new_data.append(data_instance)
    return new_data

def generate_reference(evaluate_task_data, data_root, database_file_path, reference_strategy):
    prompts = generate_reference_prompt(evaluate_task_data, data_root, reference_strategy)
    target_path = thread_reference_api(evaluate_task_data, data_root, prompts, reference_strategy)
    content = extract_reference(evaluate_task_data, data_root, target_path, reference_strategy)
    #write_output(database_file_path, content)
    write_output(os.path.join(data_root, "preprocess", evaluate_task_data, "database_"+reference_strategy+"_prompt.json"), content)
    return content
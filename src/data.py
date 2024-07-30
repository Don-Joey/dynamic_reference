import os
import json

from .database import create_alpacafarm_crossannotations, create_chatbot, create_llmbar
from .generate import generate_reference
from .utils import *

def preprocess_data(data_root, evaluate_task_data, database_file_path):
    #我们希望是一个unified data structure
    
    if evaluate_task_data == "alpacafarm-crossannotation":
        content = create_alpacafarm_crossannotations(data_root)
    elif evaluate_task_data == "llmbar":
        content = create_llmbar(data_root)
    elif evaluate_task_data == "rewardbenchmark":
        pass
    elif evaluate_task_data == "chatbot":
        content = create_chatbot(data_root)
    write_output(database_file_path, content)
    return content

def read_evaluate_task(evaluate_task_data, data_root):
    database_file_path = os.path.join(data_root, "preprocess", evaluate_task_data, "database.json")
    if os.path.isfile(database_file_path): #判断预处理的database是否存在
        return read_json(database_file_path)
    else:
        if os.path.isdir(os.path.join(data_root, "preprocess", evaluate_task_data)):
            return preprocess_data(data_root, evaluate_task_data, database_file_path)
        else:
            os.mkdir(os.path.join(data_root, "preprocess", evaluate_task_data))
            return preprocess_data(data_root, evaluate_task_data, database_file_path)
        

def read_evaluate_reference_for_task(evaluate_task_data, data_root, reference_strategy):
    database_file_path = os.path.join(data_root, "preprocess", evaluate_task_data, "database_"+reference_strategy+"_prompt.json")
    if os.path.exists(database_file_path): #判断reference是否存在
        print("存在")
        return read_json(database_file_path)
    else:
        return generate_reference(evaluate_task_data, data_root, database_file_path, reference_strategy)
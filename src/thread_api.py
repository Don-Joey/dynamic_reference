import glob

import requests, random
from queue import Queue
import threading
import json
import openai, time, os

from openai import OpenAI
from src.utils import read_jsonl
import httpx
httpx_client = httpx.Client(verify=False)
os.environ["OPENAI_API_KEY"] = 'sk-MT7gdbB9BCIfBPwT8f9eB0A2FdEc4215811a83Ac5fA9F2C0'
os.environ["OPENAI_BASE_URL"] = "https://open.xiaoai.plus/v1" 
def thread_reference_api(evaluate_task_data, data_root, prompts, strategy):
    client = OpenAI(http_client=httpx_client)
    #all_keys = ['sk-MT7gdbB9BCIfBPwT8f9eB0A2FdEc4215811a83Ac5fA9F2C0']  # ['sk-li5XOVuNuDHBiups0aA969Ef2a2340569978498a1cF41982']
    #client.base_url = "https://open.xiaoai.plus/v1"  # 'http://rerverseapi.workergpt.cn/v1'
    
    if not os.path.isdir(data_root + "/preprocess/" + evaluate_task_data + "/thread_output_buffer"):
        os.mkdir(data_root + "/preprocess/" + evaluate_task_data + "/thread_output_buffer")
    
    target = data_root + "/preprocess/" + evaluate_task_data + "/thread_output_buffer/" + strategy + "_reference_GPT4_OUTPUT*"
    
    class CrawlThread(threading.Thread):
        def __init__(self, thread_id, queue):
            threading.Thread.__init__(self)
            self.thread_id = thread_id
            self.filename = target.replace("*", "_thread" + str(self.thread_id) + ".jsonl")
            self.queue = queue
        
        def run(self):
            print("start thread:", self.thread_id)
            self.crawl_spider()
            print("quit thread:", self.thread_id)
        
        def crawl_spider(self):
            global all_get_data3, candidate_key
            while True:
                if self.queue.empty():
                    break
                else:
                    row = self.queue.get()
                    msgs = row["prompt_new"]
                    try:
                        success = False
                        for attempt in range(5):
                            try:
                                #client.api_key = random.choice(all_keys)
                                response = client.chat.completions.create(
                                    model="gpt-4-turbo-2024-04-09", #gpt-4-turbo-2024-04-09
                                    messages=msgs, 
                                    temperature=0.0
                                )
                            except Exception as e:
                                time.sleep(random.randint(1, 30))
                                print(f'{e}')
                                '''
                                if str(e) == "Connection error.":
                                    print(str(e))
                                    success = True
                                    break
                                '''
                            except openai.error.APIError:
                                time.sleep(random.randint(1, 30))
                                print(f"API GG")
                            else:
                                success = True
                                break
                        if success:
                            res = response.choices[0].message.content
                            row["response"] = res
                            with open(self.filename, "a+", encoding='utf-8') as f_a:
                                f_a.write(json.dumps(row, ensure_ascii=False) + "\n")
                    except:
                        pass

    all_data = prompts
    page_queue = Queue(len(all_data))
    for p in all_data:
        page_queue.put(p)
    print(page_queue.qsize())

    crawl_threads = []
    crawl_name_list = range(20)
    for thread_id in crawl_name_list:
        thread = CrawlThread(thread_id, page_queue)
        time.sleep(0.5)
        thread.start()
        crawl_threads.append(thread)

    for thread in crawl_threads:
        thread.join()  # Wait for each thread to finish
    
    return target
def thread_evaluate_api(evaluate_task_data, data_root, prompts, evaluate_method, reference_strategy, test_case_number):
    client = OpenAI(api_key='<KEY>')
    all_keys=['sk-MT7gdbB9BCIfBPwT8f9eB0A2FdEc4215811a83Ac5fA9F2C0']#'sk-xjjFRPlzLCE6jnrx3bB825D69d3a4838A7BaDf760b331363']#['sk-li5XOVuNuDHBiups0aA969Ef2a2340569978498a1cF41982']
    client.base_url = "https://open.xiaoai.plus/v1"#'http://rerverseapi.workergpt.cn/v1'
    if os.path.isdir(data_root+"/preprocess/"+evaluate_task_data+"/thread_output_buffer"):
        pass
    else:
        os.mkdir(data_root+"/preprocess/"+evaluate_task_data+"/thread_output_buffer")
    target = data_root+"/preprocess/"+evaluate_task_data+"/thread_output_buffer/"+reference_strategy+"_"+evaluate_method+"_evaluate_GPT4_OUTPUT*"
    
    class Crawl_thread(threading.Thread):
        def __init__(self, thread_id, queue):
            threading.Thread.__init__(self)
            self.thread_id = thread_id
            self.filename = target.replace("*", "_thread" + str(self.thread_id) + ".jsonl")
            self.queue = queue
        def run(self):
            print("start thread:", self.thread_id)
            self.crawl_spider()
            print("quit thread:", self.thread_id)
        
        def crawl_spider(self):
            global all_get_data3, candidate_key
            while True:
                if self.queue.empty():
                    break
                else:
                    row= self.queue.get()
                    msgs=row["prompt_new"]
                    try:
                        success = False
                        for attempt in range(5):
                            try:
                                client.api_key = random.choice(all_keys)
                                response = client.chat.completions.create(
                                    model = "gpt-4-turbo-2024-04-09",
                                    messages=msgs, 
                                    temperature=0.0
                                )
                            except Exception as e:
                                time.sleep(random.randint(1, 30))
                                print(f'{e}')
                            except openai.error.APIerror:
                                time.sleep(random.randint(1, 30))
                                print(f"API GG")
                            else:
                                success=True
                                break
                        if success:
                            res = response.choices[0].message.content
                            row["response"] = res

                            with open(self.filename, "a+", encoding = 'utf-8') as f_a:
                                f_a.write(json.dumps(row, ensure_ascii=False)+"\n")
                    except:
                        pass
    all_data = prompts
    pageQueue = Queue(len(all_data))
    for p in all_data:
        pageQueue.put(p)
    print(pageQueue.qsize())

    crawl_threads = []
    crawl_name_list = range(20)
    for thread_id in crawl_name_list:
        thread = Crawl_thread(thread_id, pageQueue)
        time.sleep(0.5)
        thread.start()
        crawl_threads.append(thread)
    for thread in crawl_threads:
        thread.join()  # Wait for each thread to finish
    
    return target
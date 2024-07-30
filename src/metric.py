from .utils import write_output
import statistics
def alpacafarm_crossannotation_acc_metric(content, test_case_number):
    truth = 0
    total_num = 0
    miss_num = 0
    for case in content:
        try:
            if "1" in case["evaluation_prediction"][0] and statistics.mode(case["preference"]) == 1:
                truth += 1
            elif "2" in case["evaluation_prediction"][0] and statistics.mode(case["preference"]) == 2:
                truth += 1
        except:
            miss_num+=1
            pass
        total_num += 1
    #assert total_num == test_case_number, "case的数量不对"
    print("alpacafarm_crossannotation: ", truth/total_num, total_num, miss_num)

def llmbar_acc_metric(content, test_case_number):
    truth = 0
    total_num = 0
    miss_num = 0
    all_dict = {}
    for case in content:
        print(case)
        if case["source"] not in all_dict:
            all_dict[case["source"]] = [0, 0]
        try:
            if case["evaluation_prediction"][0] == case["preference"][0]:
                truth += 1
                all_dict[case["source"]][0] += 1 
        except:
            miss_num+=1
        total_num += 1
        all_dict[case["source"]][1] += 1 
    #assert total_num == test_case_number, "case的数量不对"

    print("llmbar: ", truth/total_num, total_num, miss_num)
    for key,value in all_dict.items():
        print("     ", key, value[0]/value[1])

def compute_metric(content, evaluate_task_data, evaluate_method, reference_strategy, test_case_number, metrics):
    if evaluate_task_data == "alpacafarm-crossannotation":
        for metric in metrics:
            if metric == "acc":
                alpacafarm_crossannotation_acc_metric(content, test_case_number)
    elif evaluate_task_data == "llmbar":
        for metric in metrics:
            if metric == "acc":
                llmbar_acc_metric(content, test_case_number)

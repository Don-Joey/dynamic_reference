import fire
from src.data import read_evaluate_task, read_evaluate_reference_for_task
from src.evaluate import evaluate
from src.metric import compute_metric

DATA_POOL_ROOT="/data/qiyuan/dynamic_reference/"

def main(evaluate_task_data, evaluate_method, reference_strategy, test_case_number, metrics):
    #读取要评测的数据，并convert到一个同一的格式
    content = read_evaluate_task(evaluate_task_data, DATA_POOL_ROOT)
    print("items:", len(content))
    #是否生成reference，或者本身自带reference
    
    if reference_strategy:
        print("begin reference...")
        content = read_evaluate_reference_for_task(evaluate_task_data, DATA_POOL_ROOT, reference_strategy)
    #进入评测
    print("begin evaluate...")
    content = evaluate(content,DATA_POOL_ROOT, evaluate_task_data, evaluate_method, reference_strategy, test_case_number)
    #对评测进行打分
    compute_metric(content, evaluate_task_data, evaluate_method, reference_strategy, test_case_number, metrics)

if __name__ == "__main__":
    fire.Fire(main)
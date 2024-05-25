import random
import math

def calculate_completion_time(schedule, processing_time):
    """计算给定调度方案的总完工时间"""
    n = len(schedule)
    m = len(processing_time[0])
    completion_time = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            completion_time[i][j] = processing_time[schedule[i - 1]][j - 1] + max(completion_time[i - 1][j], completion_time[i][j - 1])
    return completion_time[n][m]

def shuffle_array(array):
    """随机打乱数组顺序"""
    random.shuffle(array)

def anneal(n, processing_time, initial_temperature=1000, stopping_temperature=10, cooling_rate=0.95, iterations=100):
    """模拟退火算法求解工件调度问题"""
    current_schedule = list(range(n))
    shuffle_array(current_schedule)
    current_cost = calculate_completion_time(current_schedule, processing_time)

    temperature = initial_temperature
    while temperature > stopping_temperature:
        for _ in range(iterations):
            # 产生邻域解
            index1, index2 = random.sample(range(n), 2)
            new_schedule = current_schedule[:]
            new_schedule[index1], new_schedule[index2] = new_schedule[index2], new_schedule[index1]
            new_cost = calculate_completion_time(new_schedule, processing_time)
            # Metropolis准则
            if new_cost < current_cost or random.random() < math.exp(- (new_cost - current_cost) / temperature):
                current_schedule = new_schedule
                current_cost = new_cost
        # 降温
        temperature *= cooling_rate

    # 输出最优解和总完工时间
    print("Optimal Schedule:", current_schedule)
    print("Total Completion Time:", current_cost)

if __name__ == "__main__":
    # 读取用例并处理数据
    with open("test.txt", "r") as file:
        lines = file.readlines()
        num_cases = len(lines) // 4
        cases = []
        i = 0
        while i < len(lines):
            if lines[i].startswith('instance'):
                i += 1  # 跳过标题行
                n, m = map(int, lines[i].split())
                processing_time = [list(map(int, lines[i + 1 + j].split())) for j in range(n)]
                cases.append((n, processing_time))
            i += 1

    # 依次计算每个用例
    for i, (n, processing_time) in enumerate(cases):
        print(f"Instance {i}:")
        anneal(n, processing_time)

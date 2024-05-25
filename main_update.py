import random
import math

def generate_initial_solution(num_jobs):
    """生成初始解"""
    return list(range(num_jobs))

def evaluate_schedule(schedule, machine_times):
    """计算给定调度方案的总完工时间"""
    machine_finish_times = [0] * len(machine_times[0])
    for job_index in schedule:
        for machine_index, time in enumerate(machine_times[job_index]):
            machine_finish_times[machine_index] += time
    return max(machine_finish_times)

def generate_neighbour(current_solution):
    """生成当前解的邻居解"""
    neighbour = current_solution[:]
    index1, index2 = random.sample(range(len(neighbour)), 2)
    neighbour[index1], neighbour[index2] = neighbour[index2], neighbour[index1]
    return neighbour

def acceptance_probability(old_cost, new_cost, temperature):
    """接受新解的概率"""
    if new_cost < old_cost:
        return 1.0
    return math.exp((old_cost - new_cost) / temperature)

def simulated_annealing(machine_times, initial_temperature, cooling_rate, num_iterations):
    """模拟退火算法求解工件调度问题"""
    num_jobs = len(machine_times)
    current_solution = generate_initial_solution(num_jobs)
    best_solution = current_solution
    current_cost = evaluate_schedule(current_solution, machine_times)
    best_cost = current_cost
    temperature = initial_temperature

    for _ in range(num_iterations):
        neighbour = generate_neighbour(current_solution)
        neighbour_cost = evaluate_schedule(neighbour, machine_times)
        if acceptance_probability(current_cost, neighbour_cost, temperature) > random.random():
            current_solution = neighbour
            current_cost = neighbour_cost
        if current_cost < best_cost:
            best_solution = current_solution
            best_cost = current_cost
        temperature *= cooling_rate

    return best_solution, best_cost

def read_data_from_file(filename):
    """从文件中读取数据"""
    data = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith('instance'):
                m, n = map(int, lines[i + 1].split())
                instance_data = [[int(x) for x in lines[i + j + 2].split()[1:]] for j in range(m)]
                # 转置数据
                machine_times = list(map(list, zip(*instance_data)))
                data.append((m, n, machine_times))
                i += m + 2
            else:
                i += 1
    return data

def main():
    filename = "test.txt"
    instances = read_data_from_file(filename)

    for idx, (m, n, machine_times) in enumerate(instances):
        initial_temperature = 1000  # 初始温度
        cooling_rate = 0.99  # 冷却率
        num_iterations = 1000  # 迭代次数

        best_solution, best_cost = simulated_annealing(machine_times, initial_temperature, cooling_rate, num_iterations)

        print("实例", idx)
        print("最优调度方案:", best_solution)
        print("总完工时间:", best_cost)
        print()

if __name__ == "__main__":
    main()

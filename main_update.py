import random
import math


def evaluate_schedule(schedule, machine_times):
    """计算给定调度方案的总完工时间"""
    machine_finish_times = [0] * len(machine_times[0])
    for job_index in schedule:
        for machine_index, time in enumerate(machine_times[job_index]):
            machine_finish_times[machine_index] += time
    return max(machine_finish_times)

def generate_initial_solution(n):
    """生成随机的初始解"""
    return random.sample(range(n), n)

def generate_neighbor_solution(solution):
    """生成邻域内的随机新解"""
    neighbor_solution = solution[:]
    index1, index2, index3 = random.sample(range(len(solution)), 3)
    neighbor_solution[index1], neighbor_solution[index2], neighbor_solution[index3] = neighbor_solution[index2], neighbor_solution[index3], neighbor_solution[index1]
    return neighbor_solution

def simulated_annealing(machine_times, initial_temperature, cooling_rate, max_iterations):
    """使用优化后的模拟退火算法求解工件调度问题"""
    n = len(machine_times)
    current_solution = generate_initial_solution(n)
    best_solution = current_solution[:]
    best_time = evaluate_schedule(best_solution, machine_times)
    current_temperature = initial_temperature

    for iteration in range(max_iterations):
        new_solution = generate_neighbor_solution(current_solution)
        new_time = evaluate_schedule(new_solution, machine_times)
        current_time = evaluate_schedule(current_solution, machine_times)

        # 计算接受概率
        delta_energy = new_time - current_time
        if delta_energy < 0:
            accept_probability = 1
        else:
            accept_probability = math.exp(-delta_energy / current_temperature)

        # 接受或拒绝新解
        if random.random() < accept_probability:
            current_solution = new_solution

        # 更新最优解
        if new_time < best_time:
            best_solution = new_solution
            best_time = new_time

        # 更新温度
        current_temperature *= cooling_rate

    return best_solution, best_time

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
    """主函数"""
    filename = "test.txt"
    instances = read_data_from_file(filename)
    for idx, (m, n, machine_times) in enumerate(instances):
        initial_temperature = sum(sum(machine_times, [])) / (m * n)  # 初始温度设定为平均加工时间
        cooling_rate = 0.99  # 降低冷却率
        max_iterations = 1000  # 增加最大迭代次数
        best_schedule, best_time = simulated_annealing(machine_times, initial_temperature,
                                                       cooling_rate, max_iterations)
        print("实例", idx)
        print("最优调度方案:", best_schedule)
        print("总完工时间:", best_time)
        print(
)
if __name__ == "__main__":
    main()

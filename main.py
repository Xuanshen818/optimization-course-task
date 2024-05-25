import random
import math
import time

start_time = time.time()


def evaluate_schedule(schedule, machine_times):
    """计算给定调度方案的总完工时间"""
    machine_finish_times = [0] * len(machine_times[0])
    for job_index in schedule:
        for machine_index, time in enumerate(machine_times[job_index]):
            machine_finish_times[machine_index] += time
    return max(machine_finish_times)


def simulated_annealing(machine_times, initial_schedule, initial_temperature, cooling_rate, max_iterations):
    """使用优化后的模拟退火算法求解工件调度问题"""
    current_schedule = initial_schedule
    current_temperature = initial_temperature
    best_schedule = initial_schedule
    best_schedule_time = evaluate_schedule(initial_schedule, machine_times)
    iteration = 0

    while iteration < max_iterations:
        new_schedule = current_schedule[:]
        # 产生新解：随机交换两个工件的位置
        index1, index2 = random.sample(range(len(new_schedule)), 2)
        new_schedule[index1], new_schedule[index2] = new_schedule[index2], new_schedule[index1]

        new_schedule_time = evaluate_schedule(new_schedule, machine_times)
        current_schedule_time = evaluate_schedule(current_schedule, machine_times)

        # 计算接受概率
        if new_schedule_time < current_schedule_time:
            accept_probability = 1.0
        else:
            delta_energy = current_schedule_time - new_schedule_time
            accept_probability = math.exp(delta_energy / current_temperature)

        # 接受或拒绝新解
        if random.random() < accept_probability:
            current_schedule = new_schedule

        # 更新最优解
        if new_schedule_time < best_schedule_time:
            best_schedule = new_schedule
            best_schedule_time = new_schedule_time

        # 更新温度
        current_temperature *= cooling_rate
        iteration += 1

    return best_schedule, best_schedule_time


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
        initial_schedule = list(range(n))
        initial_temperature = sum(sum(machine_times, [])) / (m * n)  # 初始温度设定为平均加工时间
        cooling_rate = 0.99
        max_iterations = 1000  # 最大迭代次数
        best_schedule, best_time = simulated_annealing(machine_times, initial_schedule, initial_temperature,
                                                       cooling_rate, max_iterations)
        print("实例", idx)
        print("最优调度方案:", best_schedule)
        print("总完工时间:", best_time)
        print()


if __name__ == "__main__":
    main()

end_time = time.time()
execution_time = end_time - start_time
print("代码运行时间：", execution_time, "秒")

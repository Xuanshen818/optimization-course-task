import random


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


def evaluate_schedule(schedule, machine_times):
    """计算给定调度方案的总完工时间"""
    machine_finish_times = [0] * len(machine_times[0])
    for job_index in schedule:
        for machine_index, time in enumerate(machine_times[job_index]):
            machine_finish_times[machine_index] += time
    return max(machine_finish_times)


def selection(population, fitness, num_parents):
    """选择操作：根据适应度选择父代"""
    parents = []
    for _ in range(num_parents):
        # 使用轮盘赌算法选择父代
        total_fitness = sum(fitness)
        pick = random.uniform(0, total_fitness)
        cumulative_fitness = 0
        for i in range(len(population)):
            cumulative_fitness += fitness[i]
            if cumulative_fitness >= pick:
                parents.append(population[i])
                break
    return parents


def crossover(parents, num_offsprings):
    """交叉操作：对父代进行交叉，生成后代"""
    offsprings = []
    for _ in range(num_offsprings):
        parent1, parent2 = random.sample(parents, 2)  # 随机选择两个父代
        crossover_point = random.randint(1, len(parent1) - 1)  # 随机选择交叉点
        offspring = parent1[:crossover_point] + parent2[crossover_point:]
        offsprings.append(offspring)
    return offsprings


def mutation(offsprings, mutation_rate):
    """变异操作：对后代进行变异"""
    for offspring in offsprings:
        if random.random() < mutation_rate:
            index1, index2 = random.sample(range(len(offspring)), 2)  # 随机选择两个基因进行变异
            offspring[index1], offspring[index2] = offspring[index2], offspring[index1]
    return offsprings


def generate_initial_population(population_size, num_jobs):
    """生成初始种群"""
    population = []
    for _ in range(population_size):
        individual = list(range(num_jobs))  # 初始个体为工件的顺序
        random.shuffle(individual)  # 随机打乱工件的顺序
        population.append(individual)
    return population


def genetic_algorithm(machine_times, population_size, num_parents, num_offsprings, mutation_rate, num_iterations):
    """遗传算法求解工件调度问题"""
    num_jobs = len(machine_times)
    population = generate_initial_population(population_size, num_jobs)

    for _ in range(num_iterations):
        fitness = [evaluate_schedule(individual, machine_times) for individual in population]

        parents = selection(population, fitness, num_parents)
        offsprings = crossover(parents, num_offsprings)
        offsprings = mutation(offsprings, mutation_rate)

        # 更新种群
        population = parents + offsprings

    # 找到最优解
    best_individual = min(population, key=lambda x: evaluate_schedule(x, machine_times))
    best_time = evaluate_schedule(best_individual, machine_times)

    return best_individual, best_time


def main():
    filename = "test.txt"
    instances = read_data_from_file(filename)

    for idx, (m, n, machine_times) in enumerate(instances):
        population_size = 50  # 种群大小
        num_parents = 20  # 父代数量
        num_offsprings = 30  # 后代数量
        mutation_rate = 0.1  # 变异率
        num_iterations = 100  # 迭代次数

        best_individual, best_time = genetic_algorithm(machine_times, population_size, num_parents, num_offsprings,
                                                       mutation_rate, num_iterations)

        print("实例", idx)
        print("最优调度方案:", best_individual)
        print("总完工时间:", best_time)
        print()


if __name__ == "__main__":
    main()

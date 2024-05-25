import random

# 计算每个工件在每台机器上的完成时间
def calculate_completion_time(schedule, processing_time):
    n = len(schedule)
    m = len(processing_time[0])
    completion_time = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            completion_time[i][j] = processing_time[schedule[i - 1]][j - 1] + max(completion_time[i - 1][j], completion_time[i][j - 1])
    return completion_time[n][m]

# 随机生成初始种群
def generate_initial_population(population_size, n):
    population = []
    for _ in range(population_size):
        individual = list(range(n))
        random.shuffle(individual)
        population.append(individual)
    return population

# 选择适应度较高的个体
def selection(population, processing_time, fitness_function):
    population_with_fitness = [(individual, fitness_function(individual, processing_time)) for individual in population]
    population_with_fitness.sort(key=lambda x: x[1])
    return [individual for individual, _ in population_with_fitness[:len(population) // 2]]

# 交叉操作：使用部分映射交叉（PMX）
def crossover(parent1, parent2):
    n = len(parent1)
    child1 = [-1] * n
    child2 = [-1] * n
    start = random.randint(0, n - 2)
    end = random.randint(start + 1, n - 1)

    # 将父代的一部分复制到子代中
    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]

    # 处理未被复制的部分
    for i in range(n):
        if i < start or i >= end:
            while parent2[i] in child1[start:end]:
                idx = parent2.index(parent1[parent2.index(parent2[i])])
                child1[i] = parent1[idx]
                child2[i] = parent2[idx]
            else:
                child1[i] = parent2[i]
                child2[i] = parent1[i]

    return child1, child2

# 变异操作：随机交换两个位置上的工件
def mutate(individual):
    n = len(individual)
    idx1, idx2 = random.sample(range(n), 2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]

# 遗传算法主函数
def genetic_algorithm(n, processing_time, population_size=100, generations=50):
    population = generate_initial_population(population_size, n)
    for _ in range(generations):
        population = selection(population, processing_time, calculate_completion_time)
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1)
            mutate(child2)
            new_population.extend([child1, child2])
        population = new_population
    best_individual = min(population, key=lambda x: calculate_completion_time(x, processing_time))
    return best_individual, calculate_completion_time(best_individual, processing_time)

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
        best_individual, best_time = genetic_algorithm(n, processing_time)
        print("Optimal Schedule:", best_individual)
        print("Total Completion Time:", best_time)
        print()

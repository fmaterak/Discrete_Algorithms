import math
import random
import numpy as np
import johnson_for_tabu
import NEH_for_tabu


def read_from_file(filename):
    f = open(filename, 'r')
    line = f.readline().split()
    nm_of_jobs = int(line[0])
    nm_of_machines = int(line[1])
    pij = np.zeros((nm_of_jobs + 1, nm_of_machines + 1))
    for i in range(1, nm_of_jobs + 1):
        temp = f.readline().split()
        for j in range(1, nm_of_machines + 1):
            pij[i][j] = int(temp[j - 1])
    f.close()
    return pij


def count_cmax(schedule, times):
    tmp = [[None for _ in range(len(times[0]))] for _ in range(len(times))]
    for i in range(0, len(times)):
        for j in range(len(times[0])):
            if i == 0:
                if j == 0:
                    tmp[i][j] = times[schedule[i] - 1][j]
                else:
                    tmp[i][j] = (tmp[i][j - 1] + times[schedule[i] - 1][j])
            else:
                if j == 0:
                    tmp[i][j] = tmp[i - 1][j] + times[schedule[i] - 1][j]
                else:
                    tmp[i][j] = max(tmp[i - 1][j], tmp[i][j - 1]) + times[schedule[i] - 1][j]
    return tmp[len(times) - 1][len(times[0]) - 1]


def swap_neighbourhoods(schedule, neighbourhoods):
    for i in range(0, len(schedule)):
        temp_schedule = schedule[:]
        for j in range(i + 1, len(schedule)):
            temp_schedule[i], temp_schedule[j] = temp_schedule[j], temp_schedule[i]
            if temp_schedule not in neighbourhoods:
                neighbourhoods.append(temp_schedule[:])
            temp_schedule[i], temp_schedule[j] = temp_schedule[j], temp_schedule[i]
    return neighbourhoods


def neighbourhoods_generator(schedule, function="swap"):
    neighbourhoods_list = []
    neighbourhoods_list = swap_neighbourhoods(schedule, neighbourhoods=neighbourhoods_list)
    return neighbourhoods_list


def best_neighbourhood(schedules, times, tabu):
    cmin = math.inf
    tmp = schedules[0]
    for schedule in schedules:
        if schedule not in tabu:
            cmax = count_cmax(schedule, times)
            if cmax < cmin:
                cmin = cmax
                tmp = schedule
    if cmin == math.inf:
        for schedule in tabu:
            cmax = count_cmax(schedule, times)
            if cmax < cmin:
                cmin = cmax
                tmp = schedule

    return cmin, tmp


# Generowanie rozwiazania poczatkowego
def initialize_shedule(times, method="random"):
    if method == "neh":
        return NEH_for_tabu.run()
    if method == "johnson":
        return johnson_for_tabu.run()
    if method == "random":
        tmp = list(range(1, len(times) + 1))
        random.shuffle(tmp)
        return tmp
    if method == "order":
        return list(range(1, len(times) + 1))


def make_search(times, tabu, max_tabu, current, best_cmax, best_schedule, method):
    neighbourhoods = neighbourhoods_generator(current, function=method)
    tmp_tabu = tabu[-max_tabu:]
    current_cmax, current = best_neighbourhood(neighbourhoods, times, tmp_tabu[:])
    tabu.append(current)
    if current_cmax < best_cmax:
        best_schedule = current
        best_cmax = current_cmax

    return best_schedule, best_cmax, tabu, current


def tabu_search(times, max_tabu=20, iterations=500, init_function="random", neighbourhoods_function="swap"):
    schedule = initialize_shedule(times, method=init_function)
    best_schedule = schedule
    best_cmax = count_cmax(schedule, times)
    tabu = [schedule]
    current = schedule[:]
    for i in range(0, iterations):
        tmp = make_search(times, tabu[:], max_tabu, current, best_cmax, best_schedule, neighbourhoods_function)
        best_schedule = tmp[0]
        best_cmax = tmp[1]
        tabu = tmp[2]
        current = tmp[3]

    return best_schedule, best_cmax

def run():
    data = read_from_file("test.txt")
    best_schedule, best_cmax = tabu_search(data)
    return best_schedule, best_cmax

if __name__ == "__main__":
    best_schedule, best_cmax = run()
    print(best_cmax)
    print(best_schedule)

import numpy as np
from itertools import permutations
import time


def read_file(filename):
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
    return pij, nm_of_machines, nm_of_jobs


# zwraca wartosc czasu wyknywania danego zadania na wszystkich maszynach
def w_value(pij, nm_of_machines, nm_of_job):
    w = 0
    for i in range(1, nm_of_machines + 1):
        w += pij[nm_of_job][i]
    return w


# zwraca kolejnosc zadan na podstawie czasu wykonywania na wszystkich maszynach
# w kolejnosci od najdluzszego do najkrotszego
def neh_order(pij, nm_of_machines, nm_of_jobs):
    seq = []
    for i in range(1, nm_of_jobs + 1):
        seq.append(i)
    return sorted(seq, key=lambda x: w_value(pij, nm_of_machines, x), reverse=True)


# wstawia wybrana wartosc pod wybrany indeks w danej liscie
def insertion(seq, index, value):
    tmp = seq[:]
    tmp.insert(index,value)
    return tmp

# zwraca wartosc cmax dla wybranej sekwencji zadan
def makespan(pij, nm_of_machines, nm_of_jobs, seq):
    Cmax = 0
    Cij = np.zeros((nm_of_machines + 1, nm_of_jobs + 1))
    for x in range(1,len(seq)):
        for i in range(1, nm_of_machines + 1):
            Cij[i][seq[x]] = max(Cij[i][seq[x - 1]], Cij[i - 1][seq[x]]) + pij[seq[x]][i]
        #Cmax = Cij.max()
        Cmax = Cij[nm_of_machines][seq[x]]
    return Cmax


p_ij, machines, jobs = read_file("data110.txt")

start = time.time()
order = neh_order(p_ij,machines,jobs)
seq = [0, order[0]]
for i in range (1, jobs):
    cmax = float("inf")
    for j in range(1, i + 2):
        seq_tmp = insertion(seq, j, order[i])
        cmax_tmp = makespan(p_ij, machines, jobs, seq_tmp)
        if cmax_tmp < cmax:
            cmax = cmax_tmp
            seq_opt = seq_tmp[:]
    seq = seq_opt[:]
    if i%10 == 0:
        print(i)
end = time.time()

print("sekwencja"+str(seq))
print("cmax"+str(cmax))
print("czas"+str(end-start))

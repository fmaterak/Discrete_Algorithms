import numpy as np
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
    Cij = np.zeros((nm_of_machines + 1, nm_of_jobs + 1))
    for x in range(1,len(seq)):
        for i in range(1, nm_of_machines + 1):
            Cij[i][seq[x]] = max(Cij[i][seq[x - 1]], Cij[i - 1][seq[x]]) + pij[seq[x]][i]
    Cmax = Cij[nm_of_machines][seq[x]]
    return Cmax

def makespan1(pij, nm_of_machines, seq):
    Cij = np.zeros((nm_of_machines + 1, len(seq)))
    for x in range(1,len(seq)):
        for i in range(1, nm_of_machines + 1):
            Cij[i][x] = max(Cij[i][x - 1], Cij[i - 1][x]) + pij[seq[x]][i]
    Cmax = Cij[nm_of_machines][x]
    return Cmax, Cij

def r(Cij, pij, seq, i, imax, j, jmax):
    R = Cij[i][j]
    if i < imax and j < jmax:
        if Cij[i + 1][j] - pij[seq[j]][i + 1] == R and Cij[i][j+1] - pij[seq[j+1]][i] == R:
            R = r(Cij, pij, seq, i + 1, imax, j, jmax)
            if R == np.max(Cij):
                return R
            R = r(Cij, pij, seq, i, imax, j + 1, jmax)
            if R == np.max(Cij):
                return R
    if i < imax:
        if Cij[i + 1][j] - pij[seq[j]][i + 1] == R:
            R = r(Cij, pij, seq, i + 1, imax, j, jmax)
    if j < jmax:
        if Cij[i][j+1] - pij[seq[j+1]][i] == R:
            R = r(Cij, pij, seq, i, imax, j+1, jmax)

    return R


p_ij, machines, jobs = read_file("Data/ta051.txt")

start = time.time()
order = neh_order(p_ij, machines, jobs)
seq = [0, order[0]]
for i in range(1, jobs):
    cmax = float("inf")
    for j in range(1, i + 2):
        seq_tmp = insertion(seq, j, order[i])
        cmax_tmp, cij_tmp = makespan1(p_ij, machines, seq_tmp)
        #cmax_tmp = makespan(p_ij, machines, jobs, seq_tmp)
        if cmax_tmp < cmax:
            cmax = cmax_tmp
            seq_opt = seq_tmp[:]
            cij_opt = cij_tmp[:]

    # cmax = float("inf")
    # seq = seq_opt[:]
    # k = seq.pop()
    # for j in range(1, i + 2):
    #     seq_tmp = insertion(seq, j, k)
    #     cmax_tmp, cij_tmp = makespan1(p_ij, machines, seq_tmp)
    #     if cmax_tmp < cmax:
    #         cmax = cmax_tmp
    #         seq_opt = seq_tmp[:]
    #         cij_opt = cij_tmp[:]

    seq = seq_opt[:]
    #if (i + 1) % 10 == 0:
        #print(i + 1)
end = time.time()

print("sekwencja" + str(seq))
print("czas " + str(end - start))
print("cmax " + str(cmax))

#R = r(cij_opt, p_ij, seq, 1, machines, 1, jobs)
#print(R)

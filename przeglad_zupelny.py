import numpy as np
from itertools import permutations
import time

f = open("test.txt", 'r')
line = f.readline().split()
nm_of_jobs = int(line[0])
nm_of_machines = int(line[1])
pij = np.zeros((nm_of_jobs+1, nm_of_machines+1))
for i in range(1, nm_of_jobs+1):
    temp = f.readline().split()
    for j in range(1, nm_of_machines+1):
        pij[i][j] = int(temp[j-1])
f.close()

seq = [0]*(nm_of_jobs+1)
for i in range(nm_of_jobs+1):
    seq[i] = i

perm = permutations(seq)
p = list(perm)

Cmax = float('inf')
pi_opt = [0]*len(seq)
Cij = np.zeros((nm_of_machines+1, nm_of_jobs+1))
Cij_opt = np.zeros((nm_of_machines+1, nm_of_jobs+1))

start = time.time()
for x in range(int(len(p)/(nm_of_jobs+1))):
    for i in range(1, nm_of_machines + 1):
        for j in range(1, nm_of_jobs + 1):
            Cij[i][p[x][j]] = max(Cij[i][p[x][j - 1]], Cij[i - 1][p[x][j]]) + pij[p[x][j]][i]
    if Cij.max() < Cmax:
        Cmax = Cij.max()
        pi_opt = p[x]
        for i in range(1, nm_of_machines + 1):
            for j in range(1, nm_of_jobs + 1):
                Cij_opt[i][j] = Cij[i][j]
end = time.time()

print(pi_opt)
print(Cij_opt)
print(Cmax)
print(end-start)

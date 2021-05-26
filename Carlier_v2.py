import numpy as np
import copy

class Task:
    r = 0
    q = 0
    p = 0
    order = 0

    def __init__(self, r, p, q, order):
        self.r = r
        self.p = p
        self.q = q
        self.order = order


def read_from_file(filename):
    with open(filename, "r") as fic:
        x = fic.readline().split()
        nm_jobs = int(x[0])
        ListOfTasks = []
        for i in range(nm_jobs):
            line = fic.readline().split()
            T = Task(int(line[0]), int(line[1]), int(line[2]),i+1)
            ListOfTasks.append(T)
    return ListOfTasks


def schrage(ListOfTasks):
    G = []
    N = ListOfTasks
    t = minR(N)
    pi = []
    cmax = 0

    while( len(G)!=0 or len(N)!=0):
        while(len(N)!=0 and minR(N) <= t):
            minIndex = minRindex(N)
            G.append(N[minIndex])
            N.remove(N[minIndex])
        if(len(G) == 0):
            t = minR(N)
        elif (G != 0):
            maxIndex = maxQindex(G)
            pi.append(G[maxIndex])
            t += G[maxIndex].p
            cmax = max(cmax, t + G[maxIndex].q)
            G.remove(G[maxIndex])
    return cmax, pi


def schrageWithDivision(ListOfTasks):
    G = []
    N = ListOfTasks
    t = minR(N)
    cmax = 0

    taskOnMachine = Task(N[0].r, N[0].p, N[0].q, 0)
    taskOnMachine.q = maxQindex(N)

    while(len(G)!=0 or len(N)!=0):
        while(len(N)!=0 and minR(N) <= t):
            minIndex = minRindex(N)
            G.append(N[minIndex])
            N.remove(N[minIndex])
            if G[-1].q > taskOnMachine.q:
                taskOnMachine.p = t - G[-1].r
                t = G[-1].r
                if taskOnMachine.p > 0:
                    G.append(taskOnMachine)
        if(len(G) == 0):
            t = minR(N)
        else:
            max_index = maxQindex(G)
            taskOnMachine = G[max_index]
            t += G[max_index].p
            cmax = max(cmax, t + G[max_index].q)
            G.remove(G[max_index])
    return cmax


def minR(ListOfTasks):
    minR = ListOfTasks[0].r
    for task in ListOfTasks:
        if (task.r < minR):
            minR = task.r
    return minR


def minRindex(ListOfTasks):
    minR = ListOfTasks[0].r
    minRindex = 0
    for i in range(len(ListOfTasks)):
        if (ListOfTasks[i].r < minR):
            minR = ListOfTasks[i].r
            minRindex = i
    return minRindex


def maxQindex(ListOfTasks):
    maxQ = ListOfTasks[0].q
    maxQindex = 0
    for i in range(len(ListOfTasks)):
        if (ListOfTasks[i].q > maxQ):
            maxQ = ListOfTasks[i].q
            maxQindex = i
    return maxQindex

def printPI(pi, cmax):
    print("Schrage task order: ")
    orderTab = []
    for i in range(len(pi)):
         orderTab.append(pi[i].order)
    print(orderTab)
    print("Schrage cmax = " + str(cmax))

def h_K(K):
    rK = 1000000
    for i in K:
        if i.r < rK:
            rK = i.r
    qK = 1000000
    for i in K:
        if i.q < qK:
            qK = i.q
    pK = 0
    for i in K:
        pK += i.p
    hK = rK + pK + qK
    return hK, rK, pK, qK

def Carlier(ListOfTasks,UB):
    # List1 = ListOfTasks.copy()
    # List2 = ListOfTasks.copy()
    # List3 = ListOfTasks.copy()
    # List4 = ListOfTasks.copy()
    U, pi = schrage(ListOfTasks)
    List1 = pi.copy()
    List2 = pi.copy()
    List3 = pi.copy()
    List4 = pi.copy()

    if U < UB:
        UB = U
        PI = pi.copy()

    Cij = np.zeros([len(pi) + 1, 2])

    for i in range(len(pi)):
        Cij[i+1, 0] = max(Cij[i, 0], pi[i].r) + pi[i].p
        Cij[i+1, 1] = pi[i].q + Cij[i+1, 0]
    ## Wyznaczanie indeksow a, b, c
    b = -1
    for i in range(len(pi)):
        if Cij[i+1, 1] == U:
            if i > b:
                b = i

    a = 1000000
    for i in range(b + 1):
        sum = pi[i].r
        for j in range(i, b+1):
            sum += pi[j].p
        sum += pi[b].q
        if sum == U and i<a:
            a = i

    c = -1
    for i in range(a, b+1):
        if pi[i].q < pi[b].q:
            if i > c:
                c = i

    if c == -1:
        return UB, PI

    ## Zbior K
    K = []
    for i in range(c+1, b+1):
        K.append(pi[i])
    K1 = K.copy()
    hK, rK, pK, qK = h_K(K)

    r_temp = pi[c].r
    pi[c].r = max(pi[c].r, rK+pK)

    List1[c].r = pi[c].r
    LB = schrageWithDivision(List1)
    if LB < UB:
        List2[c].r = pi[c].r
        UB, PI = Carlier(List2, UB)

    pi[c].r = r_temp      # odtworzenie r

    q_temp = pi[c].q
    pi[c].q = max(pi[c].q, pK+qK)

    List3[c].q = pi[c].q
    LB = schrageWithDivision(List3)
    if LB < UB:
        List4[c].q = pi[c].q
        UB, PI = Carlier(List4, UB)

    pi[c].q = q_temp      # odtworzenie q
    return UB, pi



#############################################

ListOfTasks1 = read_from_file("in50.txt")
ListOfTasks2 = read_from_file("in100.txt")
ListOfTasks3 = read_from_file("in200.txt")
ListOfTasks4 = read_from_file("data.001.txt")
ListOfTasks44 = read_from_file("data.001.txt")
ListOfTasks5 = read_from_file("data.002.txt")
ListOfTasks55 = read_from_file("data.002.txt")
ListOfTasks6 = read_from_file("data.003.txt")
ListOfTasks66 = read_from_file("data.003.txt")
ListOfTasks7 = read_from_file("data.004.txt")
ListOfTasks77 = read_from_file("data.004.txt")
ListOfTasks8 = read_from_file("data.005.txt")
ListOfTasks88 = read_from_file("data.005.txt")
ListOfTasks9 = read_from_file("data.000.txt")
ListOfTasks10 = read_from_file("data.00x.txt")

# cmax1, pi = schrage(ListOfTasks9)
# pmtncmax1 = schrageWithDivision(ListOfTasks88)
# printPI(pi,cmax1)
# print("Schrage Pmtn cmax = " + str(pmtncmax1))

U, PI = Carlier(ListOfTasks10, 1000000)
print('\n'+str(U))

orderTab = []
for i in range(len(PI)):
     orderTab.append(PI[i].order)
print(orderTab)

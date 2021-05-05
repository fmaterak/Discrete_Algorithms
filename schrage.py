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
    print("Schrange task order: ")
    orderTab = []
    for i in range(len(pi)):
         orderTab.append(pi[i].order)
    print(orderTab)
    print("Schrange cmax = " + str(cmax))


ListOfTasks1 = read_from_file("in50.txt")
ListOfTasks2 = read_from_file("in50.txt")
ListOfTasks3 = read_from_file("in100.txt")
ListOfTasks4 = read_from_file("in100.txt")
ListOfTasks5 = read_from_file("in200.txt")
ListOfTasks6 = read_from_file("in200.txt")


print("in50:")
cmax1, pi = schrage(ListOfTasks1)
pmtncmax1 = schrageWithDivision(ListOfTasks2)
printPI(pi,cmax1)
print("Schrage Pmtn cmax = " + str(pmtncmax1))

print("\nin100:")
cmax2, pi = schrage(ListOfTasks3)
pmtncmax2 = schrageWithDivision(ListOfTasks4)
printPI(pi,cmax2)
print("Schrage Pmtn cmax = " + str(pmtncmax2))

print("\nin200:")
cmax3, pi = schrage(ListOfTasks5)
pmtncmax3 = schrageWithDivision(ListOfTasks6)
printPI(pi,cmax3)
print("Schrage Pmtn cmax = " + str(pmtncmax3))

print("\nsum:")
print("Schrange cmax = " + str(cmax1+cmax2+cmax3))
print("Schrage Pmtn cmax = " + str(pmtncmax1+pmtncmax2+pmtncmax3))

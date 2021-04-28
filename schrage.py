class Task:
    r = 0
    q = 0
    p = 0

    def __init__(self, r, p, q):
        self.r = r
        self.p = p
        self.q = q


def read_from_file(filename):
    with open(filename, "r") as fic:
        x = fic.readline().split()
        nm_jobs = int(x[0])
        ListOfTasks = []
        for i in range(nm_jobs):
            line = fic.readline().split()
            T = Task(int(line[0]), int(line[1]), int(line[2]))
            ListOfTasks.append(T)
    return ListOfTasks


def schrage(ListOfTasks):
    G = []
    N = ListOfTasks
    t = minR(N)
    cmax = 0
    pi = []

    while( len(G)!=0 or len(N)!=0):
        while(len(N)!=0 and minR(N) <= t):
            min_index = minRtask(N)
            G.append(N[min_index])
            N.remove(N[min_index])
        if(len(G) == 0):
            t = minR(N)
        elif (G != 0):
            max_index = maxQtask(G)
            pi.append(G[max_index])
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


def minRtask(ListOfTasks):
    minR = ListOfTasks[0].r
    minRtask = 0
    for i in range(len(ListOfTasks)):
        if (ListOfTasks[i].r < minR):
            minR = ListOfTasks[i].r
            minRtask = i
    return minRtask


def maxQtask(ListOfTasks):
    maxQ = ListOfTasks[0].q
    maxQtask = 0
    for i in range(len(ListOfTasks)):
        if (ListOfTasks[i].q > maxQ):
            maxQ = ListOfTasks[i].q
            maxQtask = i
    return maxQtask


ListOfTasks = read_from_file("data1.txt")
print("cmax = " + str(schrage(Li

import matplotlib.pyplot as plt

def Gantt(imp, machineCount):
    fig, ax = plt.subplots()
    color = ['red','blue','green','yellow','orange','pink','brown','magenta','purple','cyan']
    xlim = 0
    lbl_pool = []
    lbl = []
    for x in range(len(imp)):
        if not (("Zadanie " + str(imp[x][3])) in lbl): lbl.append("Zadanie " + str(imp[x][3]))

    #dodawanie do wykresu
    for x in range(len(imp)):
        if xlim < (imp[x][2]): xlim = (imp[x][2])
        data = (imp[x][1],imp[x][2]-imp[x][1])
        #ochora przed powtarzaniem sie legendy
        if color[imp[x][3]-1] in lbl_pool:
            prefix = '_'
        else:
            lbl_pool.append(color[imp[x][3]-1])
            prefix = ''
        ax.broken_barh([(data)], (((machineCount+1-(imp[x][0])) * 10)-2, 4), facecolors=color[imp[x][3]-1], label=prefix+lbl[imp[x][3]-1])

    print(lbl_pool)
    #obliczenia do wykresu
    ylim = machineCount * 10 + 10
    yticklabels = list(range(1, machineCount+1))
    yticks = [i * 10 for i in yticklabels]
    yticklabels.reverse()

    #wykres
    ax.set_ylim(0, ylim)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_xlim(0, xlim+2)
    ax.set_title('Wykres Gantta')
    ax.set_ylabel('maszyny')
    ax.set_xlabel('czas')
    ax.legend()
    ax.grid(True)
    plt.show()

#przykład
# maszyna, rozpoczecie, zakończenie, zadanie
imp = [[1,6,10,1],
       [1,3,6,2],
       [1,1,3,3],

       [2,10,14,1],
       [2,7,9,2],
       [2,3,7,3],

       [3,14,18,1],
       [3,9,12,2],
       [3,7,9,3]]

machineCount = 3

Gantt(imp, machineCount)

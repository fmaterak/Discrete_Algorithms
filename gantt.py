import matplotlib.pyplot as plt

def Gantt(imp, lmaszyn, lzadan):
    fig, ax = plt.subplots()
    color = ['red','blue','green','yellow','orange','pink']
    xlim = 0

    #dodawanie do wykresu
    for x in range(len(imp)):
        if xlim < (imp[x][1] + imp[x][2]): xlim = (imp[x][1] + imp[x][2])
        data = (imp[x][1],imp[x][2])
        ax.broken_barh([(data)], (((lmaszyn+1-(imp[x][0])) * 10)-2, 4), facecolors=color[imp[x][3]], label=color[imp[x][3]])

    #obliczenia do wykresu
    ylim = lmaszyn * 10 + 10
    yticklabels = list(range(1, lmaszyn+1))
    yticks = [i * 10 for i in yticklabels]
    yticklabels.reverse()
    legend = []
    for x in range(lzadan):
        legend.append("Zadanie " + str(imp[x][3]))

    #wykres
    ax.set_ylim(0, ylim)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_xlim(0, xlim+2)
    ax.set_title('Wykres Gantta')
    ax.set_ylabel('maszyny')
    ax.set_xlabel('czas')
    ax.legend(legend)
    ax.grid(True)
    plt.show()

#przykład
# maszyna, rozpoczecie, trwanie, zadanie
imp = [[1,6,4,1],
       [1,3,3,2],
       [1,1,2,3],

       [2,10,4,1],
       [2,7,2,2],
       [2,3,4,3],

       [3,14,4,1],
       [3,9,3,2],
       [3,7,2,3]]

lmaszyn = 3
lzadan = 3

Gantt(imp, lmaszyn, lzadan)

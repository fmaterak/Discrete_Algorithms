import numpy


# read the data from file
def read_from_file(filename):
    with open(filename, "r") as fic:
        my_nbm = int(fic.readline())
        my_nbj = int(fic.readline())
        my_p_ij = numpy.zeros((my_nbm, my_nbj))
        for i in range(my_nbm):
            p_i = fic.readline().split()
            for j in range(my_nbj):
                my_p_ij[i][j] = int(p_i[j])
    return my_nbm, my_nbj, my_p_ij


# calculate the c_ij table.
def makespan(my_seq, processing_time, machines):
    c_ij = numpy.zeros((machines, len(my_seq) + 1))

    for j in range(1, len(my_seq) + 1):
        c_ij[0][j] = c_ij[0][j - 1] + processing_time[0][my_seq[j - 1]]

    for i in range(1, machines):
        for j in range(1, len(my_seq) + 1):
            c_ij[i][j] = max(c_ij[i - 1][j], c_ij[i][j - 1]) + processing_time[i][my_seq[j - 1]]
    print(c_ij)
    return c_ij


def u(data, jobs):
    my_u = []
    for j in range(jobs):
        if data[0][j] <= data[1][j]:
            my_u.append(j)
    return sorted(my_u, key=lambda x: data[0][x])


# processing_time should be a two dimension array
def v(data, jobs):
    my_v = []
    for j in range(jobs):
        if data[0][j] > data[1][j]:
            my_v.append(j)
    return sorted(my_v, key=lambda x: data[1][x], reverse=True)


def johnson(data, nb_machines, nb_jobs):
    seq_current = u(data, nb_jobs) + v(data, nb_jobs)
    return seq_current, makespan(seq_current, processing_time, nb_machines)[nb_machines - 1][nb_jobs]


# run Johnson
machines, jobs, processing_time = read_from_file("example.txt")
seq, cmax = johnson(processing_time, machines, jobs)
seq = [x+1 for x in seq]
print("Machines:", machines)
print("Jobs:", jobs)
print("Johnson Algorithm:", "\n--------------" "\nOrder:", seq, "\nCmax:", cmax)

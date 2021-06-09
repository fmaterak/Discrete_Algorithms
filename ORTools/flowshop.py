from ortools.sat.python import cp_model
import os
import collections

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def readData(name):
    matrix = []
    with open(os.path.join(THIS_FOLDER, name), "r") as data:
        line = data.readline().split()
        tasks,  machines = int(line[0]), int(line[1])
        for _ in range(0, tasks):
            matrix.append([int(x) for x in next(data).split()])

        return matrix,tasks,machines

def read_datest(name):
    data_sets = []
    is_reading = True
    with open(os.path.join(THIS_FOLDER, name), "r") as data:
        while is_reading:
            line = data.readline()
            if "data" in line:
                line = data.readline().split()
                tasks_amount, machines_amount = int(line[0]), int(line[1])

                matrix = []

                for _ in range(0, tasks_amount):
                    matrix.append([int(x) for x in next(data).split()])

                data.readline()
                data.readline()
                cmax = int(data.readline())
                result = [int(x) for x in next(data).split()]
                data_sets.append(matrix)

            if line == "END":
                is_reading = False

    return data_sets

def solve_flow_shop_with_ortools(filename):
    data,tasks,machines = readData(filename)
    model = cp_model.CpModel()

    max_variable_cmax = sum(task for job in data for task in job)

    # Named tuple to store information about created variables.
    task_type = collections.namedtuple('task_type', 'start end interval')
    assigned_task_type = collections.namedtuple('assigned_task_type', 'start job index')

    # Creates job intervals and add to the corresponding machine lists.
    all_tasks = {}
    machine_to_intervals = collections.defaultdict(list)

    for job_id, job in enumerate(data):
        for task_id, task in enumerate(job):
            duration=task

            start_var = model.NewIntVar(0, max_variable_cmax, 'start task: '+str(job_id)+' machine: '+str(task_id))
            end_var = model.NewIntVar(0, max_variable_cmax, 'end task: '+str(job_id)+' machine: '+str(task_id))
            interval_var = model.NewIntervalVar(start_var, duration, end_var, 'interval'+str(job_id)+' machine: '+str(task_id))
            all_tasks[job_id, task_id] = task_type(start=start_var, end=end_var, interval=interval_var)
            machine_to_intervals[task_id].append(interval_var)

    for machine in range(0, machines):
        model.AddNoOverlap(machine_to_intervals[machine])

    for job_id, job in enumerate(data):
        for task_id in range(0, machines - 1):
            model.Add(all_tasks[job_id, task_id + 1].start >= all_tasks[job_id, task_id].end)


    c_max = model.NewIntVar(0, max_variable_cmax, 'cmax-makespan')
    model.AddMaxEquality(c_max,
                         [all_tasks[job_id, machines-1].end
                          for job_id in range(0, tasks)])
    model.Minimize(c_max)
    
    # Inicjalizujemy solver, który spróbuje znaleźć rozwiązanie w ramach naszego modelu:
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 300.0  # dodatkowo ograniczmy czas wykonywania obliczeń do maksymalnie 5 min

    # Wszystkie ograniczenia dodane! pora odpalić solver!
    status = solver.Solve(model)  # solver zwróci status, ale jako typ wyliczeniowy, więc troche nieczytelnie dla nas

    if (status is not cp_model.OPTIMAL):  # sprawdzamy status, aby określić czy solver znalazł rozwiązanie optymalne
        status_readable = "not optimal solution :("
    else:
        status_readable = "optimum found!"
    pi_order = []
    for task_number in range(0, tasks):
        pi_order.append((task_number+1, solver.Value(all_tasks[task_number, 0].start)))
    pi_order.sort(key=lambda x: x[1])
    pi_order = [x[0] for x in pi_order]  # modyfikujemy naszą listę, aby przechowywać tylko numer zadań, bez czasów rozpocz

    print('C_Max: %i' % solver.ObjectiveValue())
    print("Kolejność: " + str(pi_order))
    print(status_readable)
    return solver.ObjectiveValue(), pi_order, status_readable

solve_flow_shop_with_ortools("flowshop_test.txt")

import collections

# Import Python wrapper for or-tools CP-SAT solver.
from ortools.sat.python import cp_model
# https://developers.google.com/optimization/scheduling/job_shop na podstawie tego zostało zrobione

def load_Data(file_name):

    try:
        with open(file_name, "r") as file:
            data_set = str(next(file).split())
            _, data_set_number = data_set.split('.')
            data_set_number, _ = data_set_number.split(':')
            data_set_number = int(data_set_number)
            tasks, machines, operations = [int(x) for x in next(file).split()]
            jobshop_matrix = []
            for task in range(0, tasks):
                row = next(file).split()
                operation_in_task = int(row[0])
                job_matrix = []
                for i in range(1,operation_in_task*2,2):
                    m = int(row[i])
                    p = int(row[i+1])
                    job_matrix.append((m, p))
                jobshop_matrix.append(job_matrix)

            return jobshop_matrix, tasks, machines
    except FileNotFoundError:
        print("File not found.")
        raise FileNotFoundError

def solve_job_shop(filename):
    jobs_data,task,machines = load_Data(filename)
    model = cp_model.CpModel()

    max_variable = sum(task[1] for job in jobs_data for task in job)

    # Named tuple to store information about created variables.
    task_type = collections.namedtuple('task_type', 'start end interval')
    assigned_task_type = collections.namedtuple('assigned_task_type', 'start job index')

    # Creates job intervals and add to the corresponding machine lists.
    all_tasks = {}
    machine_to_intervals = collections.defaultdict(list)

    for job_id, job in enumerate(jobs_data):
        for task_id, task in enumerate(job):
            machine = task[0]
            duration = task[1]
            start_var = model.NewIntVar(0, max_variable, 'start')
            end_var = model.NewIntVar(0, max_variable, 'end' )
            interval_var = model.NewIntervalVar(start_var, duration, end_var,'interval' )
            all_tasks[job_id, task_id] = task_type(start=start_var,end=end_var, interval=interval_var)
            machine_to_intervals[machine].append(interval_var)

    # Create and add disjunctive constraints.
    for machine in range(1, machines+1):
        model.AddNoOverlap(machine_to_intervals[machine])

    # Precedences inside a job.
    for job_id, job in enumerate(jobs_data):
        for task_id in range(len(job) - 1):
            model.Add(all_tasks[job_id, task_id + 1].start >= all_tasks[job_id, task_id].end)

    # Makespan objective.
    c_max = model.NewIntVar(0, max_variable, 'cmax-makespan')
    model.AddMaxEquality(c_max,
        [all_tasks[job_id, len(job) - 1].end
        for job_id, job in enumerate(jobs_data)
    ])
    model.Minimize(c_max)

    # Solve model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        # Create one list of assigned tasks per machine.
        assigned_jobs = collections.defaultdict(list)
        for job_id, job in enumerate(jobs_data):
            for task_id, task in enumerate(job):
                machine = task[0]
                assigned_jobs[machine].append(
                    assigned_task_type(start=solver.Value(
                        all_tasks[job_id, task_id].start),
                                       job=job_id,
                                       index=task_id,))

        # Create per machine output lines.
        output = ''
        for machine in range(1,machines+1):
            # Sort by starting time.
            assigned_jobs[machine].sort()
            sol_line_tasks = 'Machine ' + str(machine) + ': '

            for assigned_task in assigned_jobs[machine]:
                name = assigned_task.job * machines + assigned_task.index + 1
                sol_line_tasks += '%i ' % name
            sol_line_tasks += '\n'
            output += sol_line_tasks
        # Finally print the solution found.
        print('Optimal C_Max: %i' % solver.ObjectiveValue())
        print(output)
        return solver.ObjectiveValue()


solve_job_shop("jobshop_test.txt")

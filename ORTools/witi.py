import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
class WiTi_Task:
    def __init__(self, task_number, duration, weight, completion_time):
        self.id: int = task_number
        self.duration: int = duration
        self.weight: int = weight
        self.completion_time: int = completion_time

class WiTi_Instance:
    tasks: list # lista wszystkich zadań, będą po kolei dla wygody
    tasks_number: int # liczba wszystkich zadań

    @staticmethod
    def load_from_file(name):
        """ Metoda wczytująca instancje z pliku - to zostawiam Państwu, na razie na sztywno dodana mała instancja."""
        instance = WiTi_Instance()
        with open(os.path.join(THIS_FOLDER, name), "r") as data:
            line = int(data.readline())
            instance.tasks_number = line
            instance.tasks = []
            for id in range(line):
                duration, weight, completion_time = data.readline().split()
                instance.tasks.append(WiTi_Task(id, int(duration), int(weight), int(completion_time)))
        return instance

    def get_duration(self, task_number):
        return self.tasks[task_number].duration

    def get_weight(self, task_number):
        return self.tasks[task_number].weight

    def get_completion_time(self, task_number):
        return self.tasks[task_number].completion_time

def solve_witi_with_solver(file):
    from ortools.sat.python import cp_model  # importujemy model CP z biblioteki or-tools

    instance = WiTi_Instance.load_from_file(file)

    model = cp_model.CpModel()  # inicjalizacja modelu - przechowa nasze zmienne oraz ograniczenia naszego problemu
    sum_duration = 0
    sum_weight_time = 0
    for task_number in range(instance.tasks_number):  # iterujemy po wszystkich zadaniach:
        sum_duration = sum_duration + instance.get_duration(task_number)
        sum_weight_time = sum_weight_time + (instance.get_weight(task_number) * instance.get_completion_time(task_number))

    Cmax_max_value = sum_duration  
    WTsum_max_value = sum_weight_time
    cmax_min_value = WTsum_min_value = 0  # nie ma ujemnych wag
    WT_sum = model.NewIntVar(WTsum_min_value, WTsum_max_value, 'Witi objective')

    model_start_vars = []
    model_ends_vars = []
    model_interval_vars = []
    model_late_vars = []


    for task_number in range(instance.tasks_number):
        suffix = f"completion_time:{task_number}"
        start_var = model.NewIntVar(cmax_min_value, Cmax_max_value, 'start_' + suffix)
        end_var = model.NewIntVar(cmax_min_value, Cmax_max_value, 'end_' + suffix)
        interval_var = model.NewIntervalVar(start_var, instance.get_duration(task_number), end_var, 'interval_' + suffix)
        late_var = model.NewIntVar(WTsum_min_value, WTsum_max_value, 'late_' + suffix)

        model_start_vars.append(start_var)
        model_ends_vars.append(end_var)
        model_interval_vars.append(interval_var)
        model_late_vars.append(late_var)

    model.AddNoOverlap(model_interval_vars)

    for task_number in range(instance.tasks_number):
        model.Add(model_late_vars[task_number] >= 0)
        model.Add(model_late_vars[task_number] >= (model_ends_vars[task_number] - instance.get_completion_time(task_number)) * instance.get_weight(task_number))

    model.Add(WT_sum >= sum(model_late_vars))

    model.Minimize(WT_sum) #Minimalizujemy sumę ważonych spóźnień

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 300.0

    status = solver.Solve(model)

    if (status is not cp_model.OPTIMAL):
        status_readable = "not optimal solution :( "
    else:
        status_readable = "optimum found!"

    pi_order = []
    for task_number in range(instance.tasks_number):
        pi_order.append((task_number +1, solver.Value(model_start_vars[task_number])))
    pi_order.sort(key=lambda x: x[1])
    pi_order = [x[0] for x in pi_order] 

    print(f"Script ended\nSuma ważonych spóżnień: {solver.ObjectiveValue()}\norder: {pi_order}\nis optimal? {status_readable}")
    return solver.ObjectiveValue(), pi_order, status_readable

solve_witi_with_solver("witi_test2.txt")

import math
import numpy as np

def decode_solution(solution):
    assign_set = []

    for key, value in solution.items():
        if value == 1:
            assign_set.append(key)

#Graph it to the console
    n = int(math.sqrt(len(assign_set)))
    final_solution = np.zeros((n, n))
    for item in assign_set:
        row = int(item[0]) - 1
        colum = int(item[1]) - 1
        sym_value = item[2]
        try:
            final_solution[row][colum] = sym_value
        except:
            print("Ah..... Turns out we didn't find all the answers :(")
            break

#Write to DIMACS file
    encode_to_DIMACS(assign_set)
    return final_solution

def encode_to_DIMACS(solution_list):
    print("\nSolution found! Please name the file you want to use to save the solution: ")
    file_name = input()
    with  open(file_name, 'a') as f:
        variable_count = int(math.pow(len(solution_list), 3))
        clause_count = int(len(solution_list))
        f.writelines("p cnf {}  {}\n".format(variable_count, clause_count))
        solution_list_iter = solution_list.__iter__()
        while True:
            try:
                i = next(solution_list_iter) + " " + "0\n"
                f.write(i)
            except StopIteration:
                break





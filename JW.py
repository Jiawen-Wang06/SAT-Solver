import copy
import settings
from time import process_time


'''
@clauses: the CNF need to be resolved --> list of list of dictionaries. Eg: [[{'111':-1}, {'123':1}], [{'111': -1}]]
@symbols: the values that can be put in each clause
@solution: final assignment of the whole CNF that can satisfy each clause
Return: the final solution or 0 when there is no solution found

This function is the main part of the SAT solver, first, evaluate if all the clauses has been satisfied, then, find all the unit 
clauses in the  CNF set, so the CNF can be simplified for further processing, last, if there is no unit clauses anymore, split part 
comes in, each value from the @symbols  will be assigned to each variable as to make it true or false to test if the clause can 
be satisfied.
'''
def JW_dp_process(clauses, symbols, solution):
   

    #If CNF has 0 clauses in it, all clauses has been removed due to the fact they has been satisfied
    if (len(clauses) == 0):
        return solution

    #Find all unit clauses first to simplify the clause for futher process
    while (JW_find_unit_clause(clauses)!= False):
        unit_clause_symbol = JW_find_unit_clause(clauses)
        if(JW_check_polarity_clause(unit_clause_symbol, clauses) == False):
            key = next(iter(unit_clause_symbol.keys()))
            value = next(iter(unit_clause_symbol.values()))
            JW_simplify_clauses(unit_clause_symbol,clauses)
            settings.unit_clause_found += 1
            solution[key] = value
        else:
            settings.conflict_count += 1
            return False

    if (len(clauses) == 0):
        return solution

    # No unit clause exist and there are still some clauses that hasn't been satisfied, split part comes in
    
    #jeroslow_wang_oneside_heuristic(clauses, symbols, solution)
    clauses_backup = copy.deepcopy(clauses)
    exsit = jeroslow_wang_oneside(clauses,weight = 2)
    settings.search_count+= 1
    solution[exsit] = 1
    if (JW_check_polarity_clause({exsit: 1}, clauses) == False):
        if (JW_dp_process(JW_simplify_clauses({exsit: 1}, clauses), symbols, solution)):
            return solution
        else:
            settings.backtrack_count += 1
            solution[exsit] = -1
            if (JW_check_polarity_clause({exsit: -1}, clauses_backup) == False):
                return JW_dp_process(JW_simplify_clauses({exsit: -1}, clauses_backup), symbols, solution)








def JW_find_unit_clause(clauses):
    unit_clause = False


    for clause in clauses:
        if len(clause) == 1:
            unit_clause = clause[0]
            return unit_clause
    return False
  

def JW_check_polarity_clause(unit_clause, clauses):
    key = next(iter(unit_clause.keys()))
    value = next(iter(unit_clause.values()))

    for clause in clauses:
        if len(clause) == 1:
            for variable in clause:
                if key in variable:
                    if variable[key] == -value:
                        return True
    return False

def JW_simplify_clauses(symbol_to_test, clauses):
    clauses_to_delete  = []
    key = next(iter(symbol_to_test.keys()))
    value = next(iter(symbol_to_test.values()))
    for clause in clauses:
        for variable in clause:
            if key in variable:
                if variable[key] == value:
                    clauses_to_delete.append(clause)
                    break
                elif variable[key] == -value:
                    clause.remove(variable)
    for item in clauses_to_delete:
        clauses.remove(item)
    return clauses



def jeroslow_wang_oneside(clauses,weight = 2):
    exsit = {}
    for clause in clauses:
        for varible in clause:
            for key in varible.keys():
                if key in exsit:
                    exsit[key] += pow(weight,-len(clause))
                else:
                    exsit[key] = pow(weight,-len(clause))
    return max(exsit,key = exsit.get)


   





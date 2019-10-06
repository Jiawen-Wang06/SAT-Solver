import copy
import random
import settings
from time import process_time

'''
@clauses: the CNF need to be resolved --> list of list of dictionaries. Eg: [[{'111':-1}, {'123':1}], [{'111': -1}]]
@symbols: the values that can be put in each clause
@solution: final assignment of the whole CNF that can satisfy each cause
Return: the final solution or 0 when there is no solution found

This function is the main part of the SAT solver, first, evaluate if all the clauses has been satisfied, then, find all the unit 
clauses in the  CNF set, so the CNF can be simplified for futher processing, last, if there is no unit clauses anymore, split part 
comes in, each value from the @symbols  will be assinged to each variable as to make it ture of false to test if the clause can 
be satisfied.
'''
def VSIDS_dp_process(clauses, solution, symbol_counter = None):
    #If CNF has 0 clauses in it, all clauses has been removed due to the fact they has been satisfied
    if (len(clauses) == 0):
        return solution

    #Find all unit clauses first to simplify the clause for futher process
    while (VSIDS_find_unit_clause(clauses)):
        unit_clause_symbol = VSIDS_find_unit_clause(clauses)
        if(VSIDS_check_polarity_clause(unit_clause_symbol, clauses) == False):
            key = next(iter(unit_clause_symbol.keys()))
            value = next(iter(unit_clause_symbol.values()))
            VSIDS_simplify_clauses(unit_clause_symbol,clauses,symbol_counter)
            settings.unit_clause_found += 1
            solution[key] = value
        else:
            settings.conflict_count += 1
            return False

    if (len(clauses) == 0):
        return solution

    # No unit clause exist and there are still some clauses that hasn't been satisfied, split part comes in

    if settings.COUNTER  == 1000:
        settings.COUNTER = 0
        for key, value in symbol_counter:
            symbol_counter[key]  = value * 0.5
    
    deleted_item = []
    for key, value in symbol_counter.items():
        if key in list(solution.keys()):
            deleted_item.append(key)

    for item in deleted_item:
        symbol_counter.pop(item)

    if len(list(symbol_counter.values())) != 0:
        max_symbol = max(list(symbol_counter.values()))
    else:
        max_symbol = 0
    max_key = []
    assign_symbol = ""

    for key, value in symbol_counter.items():
        if value == max_symbol:
            max_key.append(key)
    if len(max_key) > 1:
        assign_symbol = random.choice(max_key)
        settings.search_count += 1
    else:
        
        assign_symbol = max_key[0]
        settings.search_count += 1
        

    settings.COUNTER += 1
    clauses_backup = copy.deepcopy(clauses)
    if assign_symbol not in list(solution.keys()):
        if assign_symbol[0] != '-':
            solution[assign_symbol] = 1
            if (VSIDS_check_polarity_clause({assign_symbol:1}, clauses) == False):
                VSIDS_simplify_clauses({assign_symbol:1}, clauses, symbol_counter)
                if(VSIDS_dp_process(clauses, solution, symbol_counter)):
                    return solution
                else:
                    settings.backtrack_count += 1
                    solution[assign_symbol] = -1
                    if (VSIDS_check_polarity_clause({assign_symbol:-1}, clauses_backup) == False):
                        VSIDS_simplify_clauses({assign_symbol:-1}, clauses_backup, symbol_counter)
                        return VSIDS_dp_process(clauses_backup, solution, symbol_counter)

        if assign_symbol[0] == '-':
             solution[assign_symbol] = -1
             if (VSIDS_check_polarity_clause({assign_symbol:-1}, clauses_backup) == False):
                 VSIDS_simplify_clauses({assign_symbol:-1}, clauses_backup, symbol_counter)
                 return VSIDS_dp_process(clauses_backup, solution, symbol_counter)






def VSIDS_find_unit_clause(clauses):
    unit_clause = False
    cnf = clauses.__iter__()
    while True:
        try:
            clause = next(cnf)
            if len(clause) == 1:
                unit_clause = clause[0]
                return unit_clause
        except StopIteration:
                return unit_clause


def VSIDS_check_polarity_clause(unit_clause, clauses):
    key = next(iter(unit_clause.keys()))
    value = next(iter(unit_clause.values()))

    for clause in clauses:
        if len(clause) == 1:
            for variable in clause:
                if key in variable:
                    if variable[key] == -value:
                        return True
    return False

def VSIDS_simplify_clauses(symbol_to_test, clauses, symbol_counter = None):
    clauses_to_delete  = []
    key = next(iter(symbol_to_test.keys()))
    value = next(iter(symbol_to_test.values()))
    for clause in clauses:
        for variable in clause:
            if  key in variable:
                if variable[key] == value:
                    clauses_to_delete.append(clause)
                    if key not in list(symbol_counter.keys()):
                        symbol_counter[key] = 0
                    else:
                        symbol_counter[key] += 1
                    #break
                elif variable[key] == -value:
                    clause.remove(variable)
    for item in clauses_to_delete:
        clauses.remove(item)












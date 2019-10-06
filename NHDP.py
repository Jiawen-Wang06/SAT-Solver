import copy
from time import process_time
import settings

'''
@clauses: the CNF need to be resolved --> list of list of dictionaries. Eg: [[{'111':-1}, {'123':1}], [{'111': -1}]]
@symbols: the values that can be put in each clause
@solution: final assignment of the whole CNF that can satisfy each cause
Return: the final solution or 0 when there is no solution found

This function is the main part of the SAT solver, first, evaluate if all the clauses has been satisfied, then, find all the unit clauses in the  CNF set, so the CNF can be simplified for futher processing, last, if there is no unit clauses anymore, split part comes in, each value from the @symbols  will be assigned to each variable as to make it true of false to test if the clause can be satisfied.
'''
def NH_dp_process(clauses, symbols, solution):
    #If CNF has 0 clauses in it, all clauses has been removed due to the fact they has been satisfied
    if (len(clauses) == 0):
        return solution

    #Find all unit clauses first to simplify the clause for futher process
    while (NH_find_unit_clause(clauses)):
        unit_clause_symbol = NH_find_unit_clause(clauses)
        if(NH_check_polarity_clause(unit_clause_symbol, clauses) == False):
            key = next(iter(unit_clause_symbol.keys()))
            value = next(iter(unit_clause_symbol.values()))
            NH_simplify_clauses(unit_clause_symbol,clauses)
            settings.unit_clause_found += 1
            solution[key] = value
        else:
            settings.conflict_count += 1
            return False
            
    #Evaluate after all unit clauses has been spotted and simplified, will there still any clauses are not satisfied
    if (len(clauses) == 0):
        return solution

    # No unit clause exist and there are still some clauses that hasn't been satisfied, split part comes in
    '''
    This is  none_heuristic way to assign true or false to the variable in each clause
    '''
    #None_heuristic(clauses, symbols, solution)
    for symbol in symbols:
         #Counting process time, if took too long, the process will terminated
        settings.search_count += 1
        if process_time() >= 1200.000:
            solution = {}
            return solution 
        clauses_backup = copy.deepcopy(clauses)
        if symbol not in list(solution.keys()):
            solution[symbol] = 1
            if (NH_check_polarity_clause({symbol:1}, clauses) == False):
                NH_simplify_clauses({symbol:1}, clauses)
                if(NH_dp_process(clauses, symbols, solution)):
                    return solution
                else:
                    settings.backtrack_count += 1
                    solution[symbol] = -1
                    if (NH_check_polarity_clause({symbol:-1}, clauses_backup) == False):
                        NH_simplify_clauses({symbol:-1}, clauses_backup)
                        return NH_dp_process(clauses_backup, symbols, solution)

'''
@clauses: the CNF need to be resolved --> list of list of dictionaries. Eg: [[{'111':-1}, {'123':1}], [{'111': -1}]]
Return: the unit clause found in the CNF 

This function is  used for finding the unit clause in all the clauses, after finding it, return the unit clause, if failed to find any unit clause, will return false.
'''
def NH_find_unit_clause(clauses): #Using iterator instead of for_loop, aiming to improve the efficiency, not so sure though......
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

'''
@clauses: the CNF need to be resolved --> list of list of dictionaries. Eg: [[{'111':-1}, {'123':1}], [{'111': -1}]]
@unit_clause: the unit clause found in the CNF
Return: return true if find out both positive (true) and negative (false) of a same symbol existed in the clauses, which means this clauses cannot be fully satisfied, otherwise, return false

This function is  used for finding if the polarity of a symbol in the unit clause  also exist, and if its also an unit clause.  if exists,
the CNF cannot be fully resolved, since you cannot be both true and false.
'''
def NH_check_polarity_clause(unit_clause, clauses):
    key = next(iter(unit_clause.keys()))
    value = next(iter(unit_clause.values()))

    for clause in clauses:
        if len(clause) == 1:
            for variable in clause:
                if key in variable:
                    if variable[key] == -value: # Verify if the opposite value for a symbol also exists as a unit clause
                        return True
    return False

'''
@clauses: the CNF need to be resolved --> list of list of dictionaries. Eg: [[{'111':-1}, {'123':1}], [{'111': -1}]]
@unit_clause:  the unit_clause  that could be set to true
Return: None

This function is  used for simplifying the CNF clauses,  for each unit_clause, it can be set to true to remove the clause. if the value in the clause is the same with the unit clause, then remove the whole clause,  cuz the whole clause can be satisfied once any of the variable is set to true; if the value in the clause is opposite of the unit clause, means that variable has been set to false, the whole clause cannot be removed since we haven't decide which variable is true, but that variable can be removed cuz its true or false has been decided.
'''
def NH_simplify_clauses(unit_clause, clauses):
    clauses_to_delete  = []
    key = next(iter(unit_clause.keys()))
    value = next(iter(unit_clause.values()))
    for clause in clauses:
        for variable in clause:
            if  key in variable:
                if variable[key] == value:
                    clauses_to_delete.append(clause)
                    break
                elif variable[key] == -value:
                    clause.remove(variable)
    for item in clauses_to_delete:
        clauses.remove(item)

'''
@clauses: the CNF need to be resolved --> list of list of dictionaries. Eg: [[{'111':-1}, {'123':1}], [{'111': -1}]]
@symbols: the values that can be put in each clause
@solution: final assignment of the whole CNF that can satisfy each cause
Return: the final solution 

This is the none heuristic way for spliting the rest of the clauses. Just loop through the whole symbols list, try each symbol in order. First try set each symbol as true to see if the clauses can be satisfied, if after all the symbols has been tried but CNF still cannot be satisfied, then trace back to try to set that value as false.
'''
def None_heuristic (clauses, symbols, solution):
    pass
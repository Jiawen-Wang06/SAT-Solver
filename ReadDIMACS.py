import copy

'''
Read cnf file for rules
@dimacs_final: return the clauses for rules as list of lists, each list is a clause
'''
def Read_files(inputfilename):

    dimacs_list = []
    dimacs_final = []
    dimacs_list_copy = []
    data = [] 
    try:
        with open(inputfilename) as file:
            data = list(file)
    except:
        print("Sorry, cannot find the file")
        exit()

    for records in data:
        if not records.startswith("p"): # skip the firstline in the cnf file
            newrecords = records.split(" ")
            for item in newrecords:
                temp_va = '\n'
                if item == temp_va:
                    continue
                if not item.startswith('0'): # skip the last 0 marker
                    temp = {}
                    if int(item) > 0:
                        temp[item] = 1
                    else:
                        temp[item[1:]] = -1
                    dimacs_list.append(temp)
            dimacs_list_copy = copy.deepcopy(dimacs_list)
            dimacs_final.append(dimacs_list_copy)
            dimacs_list  *= 0
            
    return dimacs_final

def Find_symbols(clauses):
    symbols = []
    for clause in clauses:
        for variable in clause:
            temp = list(variable.keys())
            if temp[0] not in symbols:
                symbols.append(temp[0])
    return symbols

def set_symbol_counter(clauses):
    sym_counter = {}
    for clause in clauses:
        for variable in clause:
            for key, value in variable.items():
                if value < 0:
                    sym_counter['-'+ key] = 0
                else:
                    sym_counter[key] = 0
            #sym_counter[next(iter(variable.keys()))] = 0
    return sym_counter





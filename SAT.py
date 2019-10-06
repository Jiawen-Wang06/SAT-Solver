import NHDP
import VSIDS
import MOM
import JW
import settings
import sys
import ReadDIMACS as FileHandle
import decodesolution as Decoding
from time import process_time


def main(argv):
    settings.init()
    method = sys.argv[1]
    inputfilename = sys.argv[2]
    solution = {}
    cnf = FileHandle.Read_files(inputfilename)
    symbols = sorted(FileHandle.Find_symbols(cnf))
    
    
    if method == '-S1':
        
        print("We are trying to find the solution, just a moment : )")
        print("******************************************\n")
        time_start = process_time()
        NHDP.NH_dp_process(cnf, symbols, solution)
        time_stop = process_time()
        time_took = time_stop - time_start
        if solution != {}:
            solution_found = Decoding.decode_solution(solution)
            print("\nTada! Took {} seconds, using None-heuristic solution found as below: \n".format(time_took))
            print(solution_found)
            print("Conflict count: {}\nUnit clauses count: {}\nSearch symbols count: {}\n BackTrack count:{}\n".format(settings.conflict_count, settings.unit_clause_found, settings.search_count, settings.backtrack_count))
        else:
            print("No solution was found")

    if method == '-S2':
       
        print("We are finding the solution, just seconds : )")
        print("******************************************\n")
        time_start = process_time()
        MOM.MOM_dp_process(cnf, symbols, solution)
        time_stop = process_time()
        time_took = time_stop - time_start
        if solution != {}:
            solution_found = Decoding.decode_solution(solution)
            print("\nTada! Took {} seconds, using MOM heuristic solution found as below: \n".format(time_took))
            print(solution_found)
            print("Conflict count: {}\nUnit clauses count: {}\nSearch symbols count: {}\n BackTrack count:{}\n".format(settings.conflict_count, settings.unit_clause_found, settings.search_count, settings.backtrack_count))
        else:
            print("No solution was found")




    if method == '-S4':
        
        #solution = {}
        #cnf = FileHandle.Read_files(inputfilename)
        symbol_counter = FileHandle.set_symbol_counter(cnf)
        print("We are trying to find the solution, just a moment : )")
        print("******************************************\n")
        time_start = process_time()
        VSIDS.VSIDS_dp_process(cnf, solution, symbol_counter)
        time_stop = process_time()
        time_took = time_stop - time_start

        if solution != {}:
            solution_found = Decoding.decode_solution(solution)
            print("\nTada! Took {} seconds using VSIDS heuristic, solution found as below: \n".format(time_took))
            print(solution_found)
            print("Conflict count: {}\nUnit clauses count: {}\nSearch symbols count: {}\n BackTrack count:{}\n".format(settings.conflict_count, settings.unit_clause_found, settings.search_count, settings.backtrack_count))
        else:
            print("No solution was found")


    if method == '-S3':
        print("We are finding the solution, just seconds : )")
        print("******************************************\n")
        time_start = process_time()
        JW.JW_dp_process(cnf, symbols, solution)
        time_stop = process_time()
        time_took = time_stop - time_start


        if solution != {}:
            solution_found = Decoding.decode_solution(solution)
            print("\nTada! Took {} seconds using JW heuristic, solution found as below: \n".format(time_took))
            print(solution_found)
            print("Conflict count: {}\nUnit clauses count: {}\nSearch symbols count: {}\n BackTrack count:{}\n".format(settings.conflict_count, settings.unit_clause_found, settings.search_count, settings.backtrack_count))

        else:
            print("No solution was found")








main(sys.argv[1:])
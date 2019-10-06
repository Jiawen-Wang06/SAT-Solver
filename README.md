#### 1. How to use?
1.) Open a terminal, navigate to the folder that contains the SAT.py file
2.) Use command line below to run the script
$ SAT -S{n} {InputFileName} 
n: 1,2,3,4
* 1 --> No heuristic method
* 2 --> MOM heuristic method
* 3 --> Jeroslow Wang heuristic method
* 4 --> VSIDS heuristic method (buggy....)

Example:
SAT -S1 1000_9x9sudoku45.cnf
!!notice: when input the file name, the extension need to be included also.

####2. Tips
* Each run, the program can only solve one sudoku, the inputfile should contains DIMACS file in cnf format, the content should be rules+sudoku.
* The input file need to be located in the same directory of the SAT.py file
* After the Solver find the solution, it will graph the result to the console and ask the user to create a name for the file to store the solution in DIMAS format
* File 1000_9x9sudoku45 - 1000_9x9sudoku65 is the sudoku data set encoded from 1000sudoku.txt
* File Top100_9x9sudoku8 - Top100_9x9sudoku18 is the sudoku data set encoded from top100sudoku.txt
* -S4 VSIDS heuristic is still buggy..... it can solve 1000_9x9sudoku, but when comes to harder sudoku, it will failed, sometimes, for the same sudoku, first it will fail, but running again, it will find the solution, still working on fixing this.
* We had a really hard time to turn the logic into code, therefore, we looked into some example code and borrowed some ideas from Github
 https://github.com/DRTooley/PythonSatSolver/blob/master/DPLL.py
 https://github.com/bwconrad/DPLL-SAT-Solver
 https://github.com/Robbie-Luo/KR-SAT/blob/522a6427775b8eff1109c8beff3035300a108045/Analysis/SAT.py


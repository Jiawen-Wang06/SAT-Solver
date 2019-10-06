import math
import sys
import fileinput

def readfilename():
    filename = input()
    return filename

def encodeTXT(argv):
    rule_pattern = sys.argv[1]
    inputfile = sys.argv[2]

    #onemodel = []
    #filename = inputfile
    
    #filename = readfilename()
    with open(inputfile) as file:
        data = file.read()
        listdata = data.split("\n")

    #print(type(listdata))
    #print(listdata)
    sukudofileval = 0
    for sukudo in listdata:
        numcount = len(sukudo) - sukudo.count(".")
        sukudofileval += 1
        filename =  "Top100sukudo" + str(sukudofileval)+".cnf"
        f = open(filename, 'w+')
        f.write("p cnf " + str(len(sukudo)) + " "+ str(numcount) + "\n")
        if len(sukudo) != 0:
            rowlist = [sukudo[x:x + int(math.sqrt(len(sukudo)))] for x in range(0, len(sukudo), int(math.sqrt(len(sukudo))))]
            #print(rowlist)
            for i in range(len(rowlist)):
                for j in range(len(rowlist[0])):
                    #print(listdata[i][j])
                    if rowlist[i][j] != '.':
                        numcount += 1
                        row = i + 1
                        cul = j + 1
                        numstr = str(row) + str(cul) + str(rowlist[i][j])
                        f.write(numstr + ' 0'+ '\n')
        with fileinput.input(files=rule_pattern) as inputs:
            for line in inputs:
                f.write(line)
        f.close()
    #print(onemodel)

encodeTXT(sys.argv[1:])


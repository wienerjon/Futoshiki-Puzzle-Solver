def readInput(filename):  # reads the input file and returns the initial board
                          # and the inequality constraints
    f = open(filename, "r")
    initialValues = []
    
    for x in range(5):  # get the initial board
        line = f.readline()
        lineArray = line.split()
        lineArray = [int(y) for y in lineArray]
        initialValues.append(lineArray)
        
    f.readline()
    
    horizontalIneq = []  # get the horizontal inequalities constraints
    for x in range(5):
        line = f.readline()
        lineArray = line.split()
        horizontalIneq.append(lineArray)
        
    f.readline()
        
    verticalIneq = []  # get the vertical inequalities constraints
    for x in range(4):
        line = f.readline()
        lineArray = line.split()
        verticalIneq.append(lineArray)
        
    return initialValues, horizontalIneq, verticalIneq
# end readInput

def createDomains(values): # create the domain for each variable based off the initial board
    domains = {}
    for i in range(5):
        for j in range(5):
            if (values[i][j] != 0): # if a value is not assigned, domain is that value
                domains[(i, j)] = [values[i][j]]
            else: # else it is 1-5
                domains[(i, j)] = [1, 2, 3, 4, 5]
    return domains
# end createDomains

def setUpConstraints(horizontalIneq, verticalIneq):  # compiles the constraints for each variable
    constraints = []
    for k in range(5):
        constraints.append([' ', ' ', ' ', ' ', ' '])
        
    for i in range(5): # adds constrains from horizontal inequalities
        for j in range(4):
            if horizontalIneq[i][j] == '<': # <
                constraints[i][j] += 'ltR '
                constraints[i][j+1] += 'gtL '
            elif horizontalIneq[i][j] == '>': # >
                constraints[i][j] += 'gtR '
                constraints[i][j+1] += 'ltL '

    for i in range(4): # adds constrains from vartical inequalities
        for j in range(5):
            if verticalIneq[i][j] == '^': # ^
                constraints[i][j] += 'ltD '
                constraints[i+1][j] += 'gtU '
            elif verticalIneq[i][j] == 'v': # v
                constraints[i][j] += 'gtD '
                constraints[i+1][j] += 'ltU '
    return constraints
# end setUpConstraints

def forwardChecking(values, domains): # applies forward checking to the initial board
    repeat = False # keeps track if forward checking needs to be applied again
    for i in range(5):
        for j in range(5):
            if len(domains[(i, j)]) == 1: # if value is assigned to variable
                currVal = values[i][j]
                # remove the value from the domain of other variables in the same row & col
                for k in range(5):
                    if k != i:
                        try:
                            domains[(k, j)].remove(currVal)
                            if len(domains[(k, j)]) == 0: # if a domain is empty, no solution
                                return False
                            elif len(domains[(k, j)]) == 1: # if domain has one value, rerun forward checking
                                repeat = True
                        except:
                            pass
                    if k != j:
                        try:
                            domains[(i, k)].remove(currVal)
                            if len(domains[(i, k)]) == 0: # if a domain is empty, no solution
                                return False
                            elif len(domains[(i, k)]) == 1: # if domain has one value, rerun forward checking
                                repeat = True
                        except:
                            pass
                        
            elif len(domains[(i, j)]) == 0: # if a domain is empty, no solution
                return False
    return domains, repeat
# end forwardChecking

def isConsistent(var, value, values, constraints): # check is assignment is consistent with constraints
    (i, j) = var
    for k in range(5): # check if value is already assigned to a variable in the same row or col
        if values[k][j] == value and k != i:
            return False
        if values[i][k] == value and k != j:
            return False
        
    if constraints[i][j] == ' ': # if no constraint, assignment is consistent
        return True
    
    # check if all constrains are consistent. if they are not, return false
    try: # x < y
        if 'ltR' in constraints[i][j] and values[i][j+1] != 0 and not(value < values[i][j+1]):
            return False
    except:
        pass
    try: # x > y
        if 'gtR' in constraints[i][j] and values[i][j+1] != 0 and not(value > values[i][j+1]):
            return False
    except:
        pass
    try: # y > x
        if 'ltL' in constraints[i][j] and values[i][j-1] != 0 and not(values[i][j-1] > value):
            return False
    except:
        pass
    try: # y < x
        if 'gtL' in constraints[i][j] and values[i][j-1] != 0 and not(values[i][j-1] < value):
            return False
    except:
        pass

    try: # x ^ y
        if 'ltD' in constraints[i][j] and values[i+1][j] != 0 and not(value < values[i+1][j]):
            return False
    except:
        pass
    try: # x v y
        if 'gtD' in constraints[i][j] and values[i+1][j] != 0 and not(value > values[i+1][j]):
            return False
    except:
        pass
    try: # y ^ x
        if 'gtU' in constraints[i][j] and values[i-1][j] != 0 and not(values[i-1][j] < value):
            return False
    except:
        pass
    try: # y v x
        if 'ltU' in constraints[i][j] and values[i-1][j] != 0 and not(values[i-1][j] > value):
            return False
    except:
        pass
    
    return True
# end isConsistent

def isCompleted(values): # checks if board is complete
    for i in range(5):
        for j in range(5):
            if values[i][j] == 0:
                return False
    return True
# end isCompleted 

def mostConstrained(values, i, j): # returns the amount that a variable is constrained
    domain = [1,2,3,4,5]
    for k in range(5):
        if k != i and values[k][j] != 0:
            try:
                domain.remove(values[k][j])
            except:
                pass
        if k != j and values[i][k] != 0:
            try:
                domain.remove(values[i][k])
            except:
                pass
    return len(domain) # returns the about of possible values
# end mostConstrained

def mostConstraining(values, i, j): # finds the amount of variables constrained by location (i, j)
    res = 0
    for k in range(5):
        if k != i and values[k][j] == 0:
            res += 1
        if k != j and values[i][k] == 0:
            res += 1
    return res
# end mostConstraining
        
def getBestHeuristic(values): # finds the variable with the best heuristic
    # finds most constrained
    remaining = 6
    best = ([], remaining)
    for i in range(5):
        for j in range(5):
            if values[i][j] == 0: 
                amtConstrained = mostConstrained(values, i, j)
                if (amtConstrained == best[1]):
                    best[0].append((i, j))
                elif amtConstrained < best[1]:
                    best = ([(i, j)], amtConstrained)
    #TODO
    # if there is no tie, return the most constrained variable
    if len(best[0]) == 1:
        return best[0][0]
    
    # else, find the most constraining variable
    
    # most constraining
    ties = best[0]
    mostConstaining = (None, -1)
    for location in ties:
        (i, j) = location
        currConstaints = mostConstraining(values, i, j)
        if currConstaints > mostConstaining[1]:
            mostConstaining = (location, currConstaints)
            
    return mostConstaining[0]
# end getBestHeuristic

def backtracking(assignments, domains, constraints): # backtracking algo
    if isCompleted(assignments): # check if board is complete
        return assignments # return solution
    
    var = getBestHeuristic(assignments) # get next variable to assign

    originalDomain = domains[var] # save original domain
    (i, j) = var

    for value in domains[var]: # loop through domain values for the variable
        if isConsistent(var, value, assignments, constraints): # check if domain value is consistent with constraints
            assignments[i][j] = value
            domains[var] = [value]
            result = backtracking(assignments, domains, constraints) # assign value and run backtracking again
            if result != False: # if the result is not a failure, return the solution
                return result
            
    assignments[i][j] = 0
    domains[var] = originalDomain
    
    return False # return failure
# end backtracking

def main(inputFilename, outputFile): 
    values, horizontalIneq, verticalIneq = readInput(inputFilename) # get values and constraints from input txt
    domains = createDomains(values) # get domain values
    try:
        domains, repeat = forwardChecking(values, domains) # run forward checking
    except:
        print("There is no solution")
        exit() 
    while (repeat): # repeat forwardChecking if necessary
        try:
            domains, repeat = forwardChecking(values, domains)
        except:
            print("There is no solution")
            exit()

    constraints = setUpConstraints(horizontalIneq, verticalIneq) # get constraints
    res = backtracking(values, domains, constraints) # run backtracking
        
    out = open(outputFile, "w") # write result to output file
    try:
        for row in res:
            line = ''
            for x in row:
                line += str(x)
                line += ' '
            out.write(line+'\n')
    except:
        out.write('No solution found')
    out.close()
# end main

main("input1.txt", "output1.txt")
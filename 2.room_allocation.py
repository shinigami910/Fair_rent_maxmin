from z3 import *

# read the bid matrix and total rent from a file
def read_bid_matrix_and_rent(filename):
    bids = []
    total_rents = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        #last line contains total rent values
        total_rents = list(map(int, lines[-1].split()))
        
        #lines except the last one contain the bids
        for line in lines[:-1]:
            bids.append(list(map(int, line.split())))
    
    return bids, total_rents

# write the allocation matrix to a file (with True/False values)
def write_allocation_matrix(filename, allocation, variables):
    with open(filename, 'w') as file:
        for i, row in enumerate(allocation):
            for j, value in enumerate(row):
                file.write(f"p{i+1}r{j+1}: {value}\n")

# read the bid matrix and total rents
filename = "bid_matrix.txt"
bids, total_rents = read_bid_matrix_and_rent(filename)

# persons and rooms
num_persons = len(bids)
num_rooms = len(bids[0])

# declare Boolean variables for allocation
variables = [[Bool(f"p{i+1}r{j+1}") for j in range(num_rooms)] for i in range(num_persons)]

# Create a Z3 optimizer
opt = Optimize()

# Each person is allocated exactly one room
for i in range(num_persons):
    opt.add(Sum([If(variables[i][j], 1, 0) for j in range(num_rooms)]) == 1)

# Each room is allocated to exactly one person
for j in range(num_rooms):
    opt.add(Sum([If(variables[i][j], 1, 0) for i in range(num_persons)]) == 1)

# Maximize social welfare (sum of selected bids)
social_welfare = Sum([If(variables[i][j], bids[i][j], 0) for i in range(num_persons) for j in range(num_rooms)])
opt.maximize(social_welfare)

# Solve and output the result
if opt.check() == sat:
    m = opt.model()
    allocation = [[m.evaluate(variables[i][j]) for j in range(num_rooms)] for i in range(num_persons)]
    
    # Save the allocation matrix to a file
    output_filename = "allocation.txt"
    write_allocation_matrix(output_filename, allocation, variables)
    print(f"Allocation Matrix written to {output_filename}")

    
else:
    print("No solution found.")

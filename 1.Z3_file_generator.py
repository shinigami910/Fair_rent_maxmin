def generate_z3_input(input_file, smt_file):
    with open(input_file, 'r') as f:
        # Read bid matrix and total rent from the input file
        lines = f.readlines()
        bid_matrix = [list(map(int, line.split())) for line in lines[:-1]]  # All but last line
        total_rent = int(lines[-1].strip())  # Last line as total rent

    num_people = len(bid_matrix)
    num_rooms = len(bid_matrix[0])

    # Define boolean variables for Z3
    boolean_variables = [[f"p{p+1}r{r+1}" for r in range(num_rooms)] for p in range(num_people)]

    with open(smt_file, 'w') as f:
        f.write(":-Z3 SMT Input File\n\n")
        
        # Declare variables
        f.write(":- Declare Boolean variables\n")
        for p in range(num_people):
            for r in range(num_rooms):
                f.write(f"({boolean_variables[p][r]}=false)\n")
        f.write("\n")
        
        # Add constraints
        f.write("; Constraints:\n")
        
        # Each person should be assigned to exactly one room
        f.write("; Constraint 1: Each person should be assigned to exactly one room\n\n")
        for p in range(num_people):
            room_vars = " ".join(boolean_variables[p])
            f.write(f"(allocated_to ({' '.join([f'( {var})+' for var in boolean_variables[p]])}) = 1)\n")
        
        # Each room should be assigned to at most one person
        f.write("; Constraint 2: Each room should be assigned to at most one person\n\n")
        for r in range(num_rooms):
            person_vars = [boolean_variables[p][r] for p in range(num_people)]
            f.write(f"(room_allocated ({' '.join([f'( {var})+' for var in person_vars])}) = 1)\n")
        
        # Constraint to ensure sum of bids for each person is equal to the total rent
        f.write("; Constraint 3: Sum of bids for each person should equal total rent\n\n")
        for p in range(num_people):
            bid_expr = " + ".join([f"({bid_matrix[p][r]} * {boolean_variables[p][r]})" for r in range(num_rooms)])
            f.write(f"(= (sum_bids_person{p+1} {bid_expr}) {total_rent})\n")

    print(f"Z3 input file written to {smt_file}")

input_file = "bid_matrix.txt"
intermediate_file = "z3_input.smt2"
generate_z3_input(input_file, intermediate_file) 

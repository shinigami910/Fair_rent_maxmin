from z3 import *
from fractions import Fraction

# Read matrix from file
def read_matrix_from_file(file_path, is_bid_matrix=True):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    if not lines:
        raise ValueError(f"The {'bid matrix' if is_bid_matrix else 'allocation'} file is empty.")

    if is_bid_matrix:
        bid_matrix = [list(map(int, line.split())) for line in lines[:-1]]
        total_rent = int(lines[-1].strip())
        return bid_matrix, total_rent
    else:
        num_people = len(set(line.split(":")[0][1] for line in lines))
        num_rooms = len(set(line.split(":")[0][3] for line in lines))
        allocation_matrix = [[0] * num_rooms for _ in range(num_people)]

        for line in lines:
            parts = line.strip().split(":")
            person, room = map(int, [parts[0][1], parts[0][3]])
            allocation_matrix[person - 1][room - 1] = 1 if parts[1].strip() == "True" else 0

        return allocation_matrix, num_people, num_rooms

# Function to maximize minimum utility with given matrices
def maximize_minimum_utility_with_allocation(bid_matrix_file, allocation_file, output_file):
    try:
        # Read bid matrix and allocation matrix
        bid_matrix, total_rent = read_matrix_from_file(bid_matrix_file)
        allocation_matrix, num_people, num_rooms = read_matrix_from_file(allocation_file, is_bid_matrix=False)

        # Prepare Z3 model and optimizer
        prices = [Real(f"price_room{r}") for r in range(num_rooms)]
        min_utility = Real("min_utility")
        opt = Optimize()

        # Add constraints
        opt.add(Sum(prices) == total_rent)  # Total rent
        for p in range(num_people):
            for r in range(num_rooms):
                if allocation_matrix[p][r]:
                    opt.add(min_utility <= bid_matrix[p][r] - prices[r])  # Minimum utility

        # Envy-freeness constraints
        for p in range(num_people):
            for r1 in range(num_rooms):
                for r2 in range(num_rooms):
                    if allocation_matrix[p][r1]:
                        opt.add(bid_matrix[p][r1] - prices[r1] >= bid_matrix[p][r2] - prices[r2])

        # Objective: Maximize minimum utility
        opt.maximize(min_utility)

        # Solve and write results
        if opt.check() == sat:
            model = opt.model()

            # Extract minimum utility and prices
            min_utility_value = float(Fraction(str(model.evaluate(min_utility))))
            price_vector = [round(float(Fraction(str(model.evaluate(prices[r])))), 2) for r in range(num_rooms)]

            # Calculate utilities for each person
            utilities = [
                round(bid_matrix[p][r] - price_vector[r], 2)
                for p in range(num_people)
                for r in range(num_rooms)
                if allocation_matrix[p][r]
            ]

            # Write results to file
            with open(output_file, 'w') as f:
                f.write(f"Room Prices: {' '.join(map(str, price_vector))}\n")
                f.write(f"\nPerson Utilities:\n")
                for p, utility in enumerate(utilities):
                    f.write(f"Person {p + 1}: {utility}\n")
                f.write(f"\nMinimum Utility: {min_utility_value:.2f}\n")

            print(f"Results written to {output_file}")
        else:
            print("No feasible solution found.")
            with open(output_file, 'w') as f:
                f.write("No feasible solution found.\n")

    except Exception as e:
        print(f"Error during maximize_minimum_utility_with_allocation: {str(e)}")

# File paths
bid_matrix_file = "bid_matrix.txt"
allocation_file = "allocation.txt"
output_file = "maximin_output.txt"

maximize_minimum_utility_with_allocation(bid_matrix_file, allocation_file, output_file)

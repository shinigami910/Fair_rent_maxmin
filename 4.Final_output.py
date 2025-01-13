def read_allocation_from_file(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Ensure there is at least one line in the file
        if not lines:
            raise ValueError("The allocation file is empty.")

        # Extract the allocation matrix from the file
        num_people = len(set(line.split(":")[0][1] for line in lines))  # Number of people
        num_rooms = len(set(line.split(":")[0][3] for line in lines))  # Number of rooms
        allocation_matrix = [[0 for _ in range(num_rooms)] for _ in range(num_people)]

        # Parse the allocation lines
        for line in lines:
            parts = line.strip().split(":")
            if len(parts) != 2:
                raise ValueError(f"Invalid format in line: {line.strip()}")
            try:
                person, room = map(int, [parts[0][1], parts[0][3]])  # Extract person and room indices
            except IndexError as e:
                raise ValueError(f"Error parsing line: {line.strip()}. Exception: {str(e)}")
            
            allocation_matrix[person - 1][room - 1] = 1 if parts[1].strip() == "True" else 0

        return allocation_matrix, num_people, num_rooms

    except Exception as e:
        print(f"Error reading the file: {str(e)}")
        raise

def get_allocation_details(allocation_file):
    try:
        allocation_matrix, num_people, num_rooms = read_allocation_from_file(allocation_file)

        # Prepare the output based on the allocation matrix
        allocations = []
        for p in range(num_people):
            for r in range(num_rooms):
                if allocation_matrix[p][r] == 1:  # If person is allocated to room
                    allocations.append(f"Person {p + 1} -> Room {r + 1}")
                    break  # Stop after assigning a person to one room

        # Write the final allocations to a file
        output_file = "final_room_allocation.txt"
        with open(output_file, 'w') as f:
            f.write("Final Room Allocations:\n")
            for allocation in allocations:
                f.write(allocation + "\n")

        print(f"\nRoom Allocations written to {output_file}")
    
    except Exception as e:
        print(f"Error during allocation details processing: {str(e)}")

# Input file
allocation_file = "allocation.txt"
get_allocation_details(allocation_file)

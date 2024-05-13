def convert_file(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r') as file:
            lines = file.readlines()

        with open(output_file_path, 'w') as file:
            for line in lines:
                if line.strip():  # Check if line is not empty
                    parts = line.split()
                    # Assume that each line has at least two nodes and a weight
                    if len(parts) >= 3:
                        node1, node2 = parts[0], parts[1]
                        file.write(f'{node1} {node2}\n')
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
convert_file('soc_pre.txt', 'soc.txt')

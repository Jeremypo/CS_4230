

def count_lines(file_path):
    with open(file_path, 'r') as file:
        line_count = sum(1 for line in file)
    return line_count

if __name__ == '__main__':
    file_path = 'twitter_combined.txt'
    print(count_lines(file_path))
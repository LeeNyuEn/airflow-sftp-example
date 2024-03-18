import random

num_columns = 100
target_file_size_bytes = 1024 * 1024 * 1024  # 1 GB


# Generate random data for the TSV file
def generate_random_data():
    return str(random.randint(0, 1000000))


def calculate_row_size():
    row_size = 0
    for _ in range(num_columns):
        row_size += len(generate_random_data()) + 1
    return row_size + 1


row_size_bytes = calculate_row_size()
num_rows = target_file_size_bytes // row_size_bytes

with open("../assets/data_1gb.tsv", "w") as file:
    headers = "\t".join([f"Column_{i}" for i in range(num_columns)]) + "\n"
    file.write(headers)

    for _ in range(num_rows):
        row_data = (
            "\t".join([generate_random_data() for _ in range(num_columns)]) + "\n"
        )
        file.write(row_data)

print("TSV file generated successfully.")

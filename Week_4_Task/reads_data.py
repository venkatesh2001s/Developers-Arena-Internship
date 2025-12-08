# Make a program that reads data from CSV file

import csv

def read_csv_file(filename):
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Read and print each row
            for row in reader:
                print(row)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    filename = 'sample_data.csv'  # replace with your CSV file name
    read_csv_file(filename)

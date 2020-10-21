import csv
from sys import stdin

def main():
    for file in stdin:
        for line in open_csv(file.strip()):
            print(line)

def open_csv(path: str):
    """Reads the text value of the csv blog line by line

    Args:
        path (str): path to the csv

    Yields:
        str: Text entry of a row in the csv
    """
    with open(path, mode='r') as csv_file:
        blogreader = csv.reader(csv_file)
        for row in blogreader:
            yield row[-1]

if __name__ == "__main__":
    main()
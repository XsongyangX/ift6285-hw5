import csv
from sys import stdin

def main():
    for file in stdin:
        open_csv(file.strip())

def open_csv(path: str):
    with open(path, mode='r') as csv_file:
        blogreader = csv.reader(csv_file)
        for row in blogreader:
            print(row[-1])

if __name__ == "__main__":
    main()
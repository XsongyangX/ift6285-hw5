import csv
from sys import stdin
import time
import pandas as pd

def main():
    for file in stdin:
        for line in open_csv(file.strip()):
            print(line)

csv.field_size_limit(pow(2,32))
def open_csv(path: str):
    """Reads the text value of the csv blog line by line

    Args:
        path (str): path to the csv

    Yields:
        str: Text entry of a row in the csv
    """
    log_time()
    # with open(path, mode='r') as csv_file:
    #     blogreader = csv.reader(csv_file)
    #     for row in blogreader:
    #         yield row[-1]
    dataframe = pd.read_csv(path, names=('ID', 'Gender', 'Age', 'Zodiac', 'Blog'))
    for row in dataframe['Blog']:
        yield row

start_time = time.time()
open("time.csv", 'w').close()
def log_time():
    with open("time.csv", 'a') as file:
        file.write("{}\n".format(time.time() - start_time))

if __name__ == "__main__":
    main()
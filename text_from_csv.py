import csv
from sys import stdin
import time
import pandas as pd

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
    Timer.get_current_timer().log()
    # with open(path, mode='r') as csv_file:
    #     blogreader = csv.reader(csv_file)
    #     for row in blogreader:
    #         yield row[-1]
    dataframe = pd.read_csv(path, names=('ID', 'Gender', 'Age', 'Zodiac', 'Blog'))
    for row in dataframe['Blog']:
        yield row

class Timer:
    __instance = None
    is_timing = False

    @staticmethod
    def get_current_timer():
        """
        Get a singleton instance of the timer
        """
        if Timer.__instance is None:
            raise Exception("No timer")
        return Timer.__instance

    def __init__(self, path: str):
        """Creates a timer instance

        Args:
            path (str): Path to the file where to put the time
        """
        self.start = time.time()
        self.path_to_log = path

        # clean up the log file
        open(self.path_to_log, 'w').close()

        Timer.is_timing = True
        Timer.__instance = self

    def log(self):
        """
        Logs the elapsed time since instantiation
        """
        with open(self.path_to_log, 'a') as time_log:
            time_log.write("{}\n".format(time.time() - self.start))

if __name__ == "__main__":
    main()
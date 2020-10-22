from queue import Queue
import threading
from sys import stdin
import time
from typing import List
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
    Timer.get_current_timer().log(path)
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

        # to keep track of progress in reading files
        self.__current_files: List[str] = []

        # multithreading
        self.queue : Queue = Queue()
        def background_logger():
            while True:
                self.queue.get()
                with open(self.path_to_log, 'a') as time_log:
                    time_log.write("{}\n".format(time.time() - self.start))
                self.queue.task_done()
        threading.Thread(target=background_logger, daemon=True).start()


    def log(self, current_file: str):
        """
        Logs the elapsed time since instantiation
        """
        if current_file in self.__current_files:
            return
        else:
            self.__current_files.append(current_file)
            self.__current_files = self.__current_files[-5:]

        # enqueue the request
        self.queue.put(None) # dummy value
    
    def block_until_logged(self):
        self.queue.join()

if __name__ == "__main__":
    main()
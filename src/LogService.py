import multiprocessing
import os
import datetime

import src.globals as GLOBALS


class LogService:
    def __init__(self, log_dir='logs'):
        """
        Initializes the LogService with a given directory for log files.

        :param log_dir: Directory where log files will be stored.
        """
        self.writer = None
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, f"log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
        self.queue = multiprocessing.Queue()
        self.stop_event = multiprocessing.Event()

    def _create_log_file(self, file):
        """
        Creates a new log file and writes the creation timestamp.
        """
        file.write(f"Logi symulacji utworzone {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    def _log_writer(self):
        with open(self.log_file, 'w') as file:
            self._create_log_file(file)
            while not self.stop_event.is_set() or not self.queue.empty():
                try:
                    record = self.queue.get(timeout=1)
                    file.write(record + '\n')
                    file.flush()
                except Exception as e:
                    continue

    def log(self, event):
        """
        Logs an event with a timestamp.

        :param event: The event message to log.
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.queue.put(f"{timestamp} - {event}")

    def error(self, error):
        """
        Logs an error event with a timestamp.

        :param error: The error event message to log.
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.queue.put(f"{timestamp} - [ERROR] {error}")

    @staticmethod
    def log_static(event, queue):
        """
        Logs an event with a timestamp.

        :param queue:
        :param event: The event message to log.
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        queue.put(f"{timestamp} - {event}")

    @staticmethod
    def error_static(error, queue):
        """
        Logs an error event with a timestamp.

        :param queue:
        :param error: The error event message to log.
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        queue.put(f"{timestamp} - [ERROR] {error}")

    def get_queue(self):
        return self.queue

    def start(self):
        """
        Starts the log writer process.
        """
        self.writer = multiprocessing.Process(target=self._log_writer)
        self.writer.start()

    def stop(self):
        """
        Closes the log file.
        """
        self.stop_event.set()
        self.writer.join()

class BaseLogger:
    def __init__(self, prefix: str):
        """
        Initializes the BaseLogger with a given prefix.

        :param prefix: Prefix to be used in log messages.
        """
        self.prefix = prefix

    def log(self, event):
        """
        Logs an event with the specified prefix.

        :param event: The event message to log.
        """
        GLOBALS.logger.log(f"[{self.prefix}] {event}")

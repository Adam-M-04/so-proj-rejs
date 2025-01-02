import os
import datetime
import src.globals as GLOBALS


class LogService:
    def __init__(self, log_dir='logs'):
        """
        Initializes the LogService with a given directory for log files.

        :param log_dir: Directory where log files will be stored.
        """
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, f"log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
        self.file = open(self.log_file, 'w')
        self._create_log_file()

    def _create_log_file(self):
        """
        Creates a new log file and writes the creation timestamp.
        """
        self.file.write(f"Logi symulacji utworzone {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    def log(self, event):
        """
        Logs an event with a timestamp.

        :param event: The event message to log.
        """
        self.file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {event}\n")
        self.file.flush()

    def error(self, error):
        """
        Logs an error event with a timestamp.

        :param error: The error event message to log.
        """
        self.file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - [ERROR] {error}\n")
        self.file.flush()

    def close(self):
        """
        Closes the log file.
        """
        self.file.close()

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

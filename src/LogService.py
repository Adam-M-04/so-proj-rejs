import os
import datetime
import threading

class LogService:
    def __init__(self, log_dir='logs'):
        """
        Initializes the LogService with a given directory for log files.

        :param log_dir: Directory where log files will be stored.
        """
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, f"log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
        self.pipe_r, self.pipe_w = os.pipe()
        self.stop_event = threading.Event()
        self.writer_thread = threading.Thread(target=self._log_writer)
        self.writer_thread.start()

    def _create_log_file(self, file):
        """
        Creates a new log file and writes the creation timestamp.
        """
        file.write(f"Logi symulacji utworzone {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.flush()

    def _log_writer(self):
        with open(self.log_file, 'w') as file:
            self._create_log_file(file)
            while not self.stop_event.is_set():
                try:
                    record = os.read(self.pipe_r, 1024).decode()
                    if record:
                        file.write(record)
                        file.flush()
                except Exception as e:
                    continue

    def log(self, event):
        """
        Logs an event with a timestamp.

        :param event: The event message to log.
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        os.write(self.pipe_w, f"{timestamp} - {event}\n".encode())

    def error(self, error):
        """
        Logs an error event with a timestamp.

        :param error: The error event message to log.
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        os.write(self.pipe_w, f"{timestamp} - [ERROR] {error}\n".encode())

    def stop(self):
        """
        Stops the log writer thread.
        """
        self.stop_event.set()
        os.write(self.pipe_w, b'\0')  # Ensure the writer exits the loop
        self.writer_thread.join()
        os.close(self.pipe_r)
        os.close(self.pipe_w)
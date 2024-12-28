import os
import datetime

class LogService:
    def __init__(self, log_dir='logs'):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, f"log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
        self.file = open(self.log_file, 'w')
        self._create_log_file()

    def _create_log_file(self):
        self.file.write(f"Log file created on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    def log(self, event):
        self.file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {event}\n")
        self.file.flush()

    def close(self):
        self.file.close()

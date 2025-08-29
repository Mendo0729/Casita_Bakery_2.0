import logging
import socket
import json


class JSONFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.host_ip = socket.gethostbyname(socket.gethostname())

    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
            "ip": self.host_ip
        }
        return json.dumps(log_data)

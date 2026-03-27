import json
import logging
import socket


class JSONFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        try:
            self.host_ip = socket.gethostbyname(socket.gethostname())
        except OSError:
            self.host_ip = "127.0.0.1"

    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
            "ip": self.host_ip,
        }
        return json.dumps(log_data)

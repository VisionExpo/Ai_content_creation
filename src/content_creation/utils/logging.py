import logging
import json
from datetime import datetime
from typing import Any

class CustomJSONFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.default_fields = {
            'timestamp': '',
            'level': '',
            'message': '',
            'module': '',
        }

    def format(self, record: logging.LogRecord) -> str:
        json_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'line_number': record.lineno
        }

        if hasattr(record, 'request_id'):
            json_record['request_id'] = record.request_id

        if record.exc_info:
            json_record['exception'] = self.formatException(record.exc_info)

        return json.dumps(json_record)

def setup_logging():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(CustomJSONFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

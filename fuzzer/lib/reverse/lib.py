
import logging
from threading import Lock
FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")
rlog = logging.getLogger('w13scan_reverse')
rlog.setLevel(logging.INFO)
LOGGER_HANDLER = logging.StreamHandler()
LOGGER_HANDLER.setFormatter(FORMATTER)
rlog.addHandler(LOGGER_HANDLER)
reverse_records = []
reverse_lock = Lock()
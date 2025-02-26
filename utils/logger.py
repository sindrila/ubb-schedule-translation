import logging
import colorlog

from config import LOGGING_LEVEL

logging_level = logging.INFO
if LOGGING_LEVEL.lower() == "debug":
    logging_level = logging.DEBUG

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)
logger.addHandler(handler)

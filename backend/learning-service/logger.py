import logging
import colorlog

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)

formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s:     커스텀 로그: %(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
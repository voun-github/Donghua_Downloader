import logging
import sys
from logging.handlers import TimedRotatingFileHandler, SysLogHandler
from pathlib import Path


def get_console_handler() -> logging.handlers:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    # The console sends only messages by default no need for formatter.
    return console_handler


def get_server_handler(log_format: logging.Formatter) -> logging.handlers:
    """
    Sends logs to the graylog server.
    """
    server_handler = SysLogHandler(address=('192.168.31.114', 1514))
    server_handler.setLevel(logging.INFO)
    server_handler.setFormatter(log_format)
    return server_handler


def get_file_handler(log_dir: Path, log_format: logging.Formatter) -> logging.handlers:
    log_file = log_dir / "runtime.log"
    file_handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=14, encoding='utf-8')
    file_handler.namer = my_namer
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    return file_handler


def setup_logging() -> None:
    """
    Use the following to add logger to other modules.
    import logging
    logger = logging.getLogger(__name__)

    The following suppress log messages. It will not log messages of given module unless they are at least warnings.
    logging.getLogger("").setLevel(logging.WARNING)
    """
    # Create folder for file logs.
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    # Create a custom logger.
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers.
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add handlers to the logger.
    logger.addHandler(get_console_handler())
    logger.addHandler(get_server_handler(log_format))
    logger.addHandler(get_file_handler(log_dir, log_format))


def my_namer(default_name: str) -> str:
    """
    This will be called when doing the log rotation
    default_name is the default filename that would be assigned, e.g. Rotate_Test.txt.YYYY-MM-DD
    Do any manipulations to that name here, for example this function changes the name to Rotate_Test.YYYY-MM-DD.txt
    """
    base_filename, ext, date = default_name.split(".")
    return f"{base_filename}.{date}.{ext}"

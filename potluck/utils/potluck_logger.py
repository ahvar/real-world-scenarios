import logging
import os, sys
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path


class LogFileCreationError(Exception):
    """
    Exception raised for errors when creating the log file.

    Attributes:
        filespec -- the log filespec that was requested
    """

    def __init__(self, filespec):
        self.filespec = filespec


class PotluckLogger:

    def __init__(
        self,
        application_name,
        log_file: str = None,
        file_level: int = logging.NOTSET,
        console_level: int = logging.NOTSET,
    ):
        self._file_name = log_file
        self._file_level = file_level
        self._console_level = console_level
        self._full_date_time_format = "%d%b%Y %H:%M:%S"
        self._time_with_milliseconds = "%H:%M:%S.%f"
        self._app_name = application_name
        self._potluck_logger = None
        self._file_handler = None
        self._console_handler = None
        self._start_date_time = datetime.now()
        self._finish_date_time = None
        formatter = logging.Formatter(
            "[%(asctime)s.%(msecs)03d] - %(module)s - %(levelname)s - %(message)s",
            self._full_date_time_format,
        )
        self._potluck_logger = logging.getLogger()
        self._potluck_logger.setLevel(logging.DEBUG)
        if file_level:
            if not self._file_name:
                self._file_name = Path(f"{self._app_name}.log")
            try:
                self._file_handler = RotatingFileHandler(
                    self._file_name, maxBytes=10240, backupCount=10, encoding="UTF-8"
                )
            except IOError:
                raise LogFileCreationError(self._file_name)

            self._file_handler.setLevel(self._file_level)
            self._potluck_logger.addHandler(self._file_handler)
            self._file_handler.setFormatter(formatter)
        if console_level:
            self._console_handler = logging.StreamHandler()
            self._console_handler.setLevel(self._console_level)
            self._console_handler.setFormatter(formatter)
            self._potluck_logger.addHandler(self._console_handler)

    def __del__(self):
        if self._file_handler:
            self._file_handler.close()
            self._potluck_logger.removeHandler(self._file_handler)
        if self._console_handler:
            self._console_handler.close()
            self._potluck_logger.removeHandler(self._console_handler)

        logging.shutdown()


def set_error_and_exit(error):
    """
    Reports the specified error and terminates the program..
    Parameters
    ----------
        error : str
            The error message to report.
    """
    sys.stderr.write(f"Error: {error} \n")


def init_potluck_logger():
    try:
        timestamp = datetime.now().strftime("%m%d%yT%H%M%S")
        log_dir = Path(__file__).parent / "logs" / timestamp
        log_file = log_dir / "pl_app.log"
        log_dir.mkdir(exist_ok=True, parents=True)

        potluck_logging_utils = PotluckLogger(
            application_name="Potluck",
            log_file=log_file,
            file_level=logging.DEBUG,
            console_level=logging.ERROR,
        )
        return potluck_logging_utils
    except LogFileCreationError as lfe:
        set_error_and_exit(f"Unable to create log file: {lfe.filespec}")

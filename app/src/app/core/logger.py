import logging


class CustomLogger:
    def __init__(self):
        # Global logger instance
        self.logger = logging.getLogger("multi_agent")
        self.logger.setLevel(logging.INFO)

        # Console handler with formatted output
        _handler = logging.StreamHandler()
        _handler.setLevel(logging.INFO)
        _handler.setFormatter(
            logging.Formatter("[%(asctime)s][%(levelname)s][%(name)s] %(message)s")
        )

        # Avoid duplicate handlers if re-imported
        if not self.logger.handlers:
            self.logger.addHandler(_handler)

    # Convenience functions
    def info(self, msg: str, *args, **kwargs) -> None:
        """Log a message with level INFO."""
        self.logger.info(msg, *args, **kwargs)

    def warn(self, msg: str, *args, **kwargs) -> None:
        """Log a message with level WARNING."""
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        """Log a message with level ERROR."""
        self.logger.error(msg, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs) -> None:
        """Log a message with level DEBUG."""
        self.logger.debug(msg, *args, **kwargs)

    def set_level(self, level: int) -> None:
        """Set the global logging level. Use logging.<LEVEL> constants."""
        self.logger.setLevel(level)
        for h in self.logger.handlers:
            h.setLevel(level)

import configparser
import logging.config
from logging.handlers import RotatingFileHandler


def configure_logging(config: configparser.SectionProxy):
    """
    Configures logging for the whole application

    Args:
        config (configparser.SectionProxy): the part of configuration file that consists of filename and logging level

    """
    log_format = config.get(
        "log_format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    log_date_format = config.get("date_format", "%Y-%m-%d %H:%M:%S")
    max_bytes = int(config.get("max_bytes") or 5 * 1024 * 1024)
    backup_count = config.get("backups") or 5
    level = config.get("level", "INFO")
    filename = config.get("filename")

    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt=log_date_format,
    )

    rotating_handler = RotatingFileHandler(
        filename, maxBytes=max_bytes, backupCount=backup_count
    )
    rotating_handler.setFormatter(logging.Formatter(log_format, log_date_format))

    root_logger = logging.getLogger()
    root_logger.addHandler(rotating_handler)


def read_config():
    """
    Read configuration file `config.ini` and returns the configuration values:
        - whatever
        - it's
        - gonna
        - be
    """
    config = configparser.ConfigParser()

    config.read("config.ini")

    if "LOGGING" in config:
        configure_logging(config["LOGGING"])

    pass


if __name__ == "__main__":
    read_config()

import configparser
import logging.config
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging(config: configparser.SectionProxy):
    """
    Configures logging for the whole application

    Args:
        config (configparser.SectionProxy): the part of configuration file that consists of filename and logging level

    """
    log_format = config.get(
        "log_format", "%(levelname)s - %(asctime)s - %(name)s - %(message)s"
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


def configure_repository(repo):
    url = repo.get("url")

    if url is None:
        raise ValueError("No url provided. Git repository could not be located.")

    file_path = repo.get("file_path")
    if file_path is not None and not os.path.isdir(file_path) or not os.listdir(file_path):
        file_path = None

    return url, file_path


def read_config():
    """
    Read configuration file `config.ini` and returns the configuration values:
        - whatever
        - it's
        - gonna
        - be
    """
    config = configparser.ConfigParser()

    script_dir = Path(__file__).parent

    config_path = script_dir / "config.ini"

    config.read(config_path)

    if "LOGGING" in config:
        configure_logging(config["LOGGING"])
    return configure_repository(config["REPOSITORY"])


if __name__ == "__main__":
    read_config()


def add_url(new_url: str):
    config = configparser.ConfigParser()

    script_dir = Path(__file__).parent

    config_path = script_dir / "config.ini"

    config.read(config_path)
    config.set('REPOSITORY', 'file_path', new_url)

    with open(config_path, 'w') as configfile:
        config.write(configfile)

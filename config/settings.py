import configparser


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

    pass

import userInterface
from config.settings import read_config

if __name__ == "__main__":
    read_config()
    userInterface.main()

import sys

from src.logger import logging
from src.exception import CustomeException


if __name__ == "__main__":
    try:
        logging.info("Testing the Logging and Exception Code")
        a = 1/0
    except Exception as e:
        raise CustomeException(e,sys)
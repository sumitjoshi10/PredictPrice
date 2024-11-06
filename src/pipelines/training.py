import sys
from src.logger import logging
from src.exception import CustomeException

from src.components.data_ingestion import DataIngestion


if __name__ == "__main__":
    try:
        logging.info("The training of the Model has been started")
        data_ingestion = DataIngestion()
        train_path, test_path = data_ingestion.initate_data_ingestion()
        
    except Exception as e:
        raise CustomeException(e, sys)
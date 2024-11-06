import sys
from src.logger import logging
from src.exception import CustomeException

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer


if __name__ == "__main__":
    try:
        logging.info("The training of the Model has been started")
        data_ingestion = DataIngestion()
        train_path, test_path = data_ingestion.initate_data_ingestion()
        
        data_transformation = DataTransformation()
        train_arr, test_arr, preprocessor_path = data_transformation.initiate_data_transformation(train_path,test_path)
        
        model_trainer = ModelTrainer()
        model_trainer.initiate_model_trainer(
            train_array=train_arr,
            test_array=test_arr
            )
        
    except Exception as e:
        raise CustomeException(e, sys)
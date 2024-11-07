import os
import sys
from src.logger import logging
from src.exception import CustomeException
from dataclasses import dataclass

from src.components.data_ingestion import DataIngestionConfig
from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainerConfig

from src.utils import load_json,load_object

import pandas as pd

@dataclass
class PredictionConfig:
    data_ingestion_config = DataIngestionConfig()
    location_path = data_ingestion_config.location_path
    
    data_transformation_config = DataTransformationConfig()
    preprocessor_path = data_transformation_config.preprocessor_path
    
    model_trainer_config = ModelTrainerConfig()
    model_path = model_trainer_config.trained_model_file_path
    

class Prediction:
    def __init__(self):
        self.preciction_config = PredictionConfig()
        
    def get_location(self):
        try:
            location_json = load_json(file_path=self.preciction_config.location_path)
            return location_json["location"]
        except Exception as e:
            raise CustomeException(e,sys)
    
    def predict(self,features):
        try:
            logging.info("Loading Preprocessor and perform Preprocessing")
            preprocessor = load_object(
                file_path=self.preciction_config.preprocessor_path
            )
            data_scaled = preprocessor.transform(features)
            logging.info("Preprocessoring Completed")
            
            logging.info("Loading Model and perform Prediction")
            model = load_object(
                file_path=self.preciction_config.model_path
            )
            pred = model.predict(data_scaled)
            logging.info(f"Prediction Completed and Price is {pred} Lakhs")
            return pred
        
        except Exception as e:
            raise CustomeException(e,sys)

class CustomeData:
    def __init__(self,
                 location:str,
                 total_sqft,
                 bath,
                 bhk
                 ):
        self.location = location
        self.total_sqft = total_sqft
        self.bath = bath
        self.bhk = bhk
        
    def get_data_as_data_frame(self):
        try:
            logging.info("Reading the value from the Webpage")
            custom_data_input_data = {
                "location" : [self.location],
                "total_sqft": [self.total_sqft],
                "bath" : [self.bath],
                "bhk": [self.bhk]
            }
            logging.info("Sucessfully Read the Value")
            
            return pd.DataFrame(custom_data_input_data)
        except Exception as e:
            CustomeException(e,sys)
        

if __name__ == "__main__":
    data = CustomeData("1St Block Jayanagar",1630.0,3,3)
    data_df = data.get_data_as_data_frame()
    prediction = Prediction()
    pred = prediction.predict(features=data_df)
    print(pred)
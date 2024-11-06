import sys
import os
from src.logger import logging
from src.exception import CustomeException

from dataclasses import dataclass

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

from category_encoders import TargetEncoder

from sklearn.compose import ColumnTransformer

from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_path = os.path.join("artifacts","preporcessor.pkl")
    
    
class DataTransformation:
    def __init__(self):
        self.data_transforamtion_congif = DataTransformationConfig()
    
    def get_preprocessor_obj(self):
        try:
            logging.info("Numberical and Categorical Column Preporcessing Started")
            numerical_column = ["total_sqft","bath","bhk"]
            categorical_column = ["location"]
            
            logging.info(f"Numerical Column: {numerical_column}")
            logging.info(f"Categorical Column: {categorical_column}")
            
            numerical_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )
            
            categorical_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("target_guided",TargetEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            
            logging.info("Numberical and Categorical Column Preporcessing Completed")
            
            preprocessor = ColumnTransformer([
                ("numerical_pipeline",numerical_pipeline,numerical_column),
                ("categorical_pipeline",categorical_pipeline,categorical_column)
            ])
            
            
            return preprocessor
            
        except Exception as e:
            raise CustomeException(e, sys)
    
    def initiate_data_transformation(self,train_path, test_path):
        try:
            logging.info("Reading the Train and Test CSV File")
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            target_column = "price"
            
            input_feature_train_df = train_df.drop(columns=[target_column],axis=1)
            target_feature_train_df = train_df[target_column]
            
            input_feature_test_df = test_df.drop(columns=[target_column],axis=1)
            target_feature_test_df = test_df[target_column]
            
            preprocessor_obj = self.get_preprocessor_obj()
            
            logging.info("Applying Preporcessing in Train and Test Data Set")
            
            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df , target_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)
           
            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)]
            
            save_object(
                self.data_transforamtion_congif.preprocessor_path,
                preprocessor_obj
            )
            logging.info("Saved Preprocessor Object")
            
            return(
                train_arr,
                test_arr,
                self.data_transforamtion_congif.preprocessor_path
            )
            
        except Exception as e:
            raise CustomeException(e, sys)
         
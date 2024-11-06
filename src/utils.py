import os
import sys
from src.logger import logging
from src.exception import CustomeException

import pandas as pd

import dill

def read_data():
    logging.info("Reading the data from the data Source")
    file_path = os.path.join(os.getcwd(),"notebook","data","Price.csv")
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise CustomeException(e, sys)
    
    
def save_object (file_path , obj):
    try:
        file_dir = os.path.dirname(file_path)
        
        os.makedirs(file_dir,exist_ok=True)
        
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
            
    except Exception as e:
        raise CustomeException(e , sys)
    
def target_guided_encoding():
    pass
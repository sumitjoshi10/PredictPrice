import os
import sys
from src.logger import logging
from src.exception import CustomeException

import pandas as pd

def read_data():
    logging.info("Reading the data from the data Source")
    file_path = os.path.join(os.getcwd(),"notebook","data","Price.csv")
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise CustomeException(e, sys)
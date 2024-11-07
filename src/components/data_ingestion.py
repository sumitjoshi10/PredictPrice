import os
import sys
from src.logger import logging
from src.exception import CustomeException

from dataclasses import dataclass

from src.utils import read_data,save_json

from src.data_cleaning_helper import convert_sqft_to_num, extracting_bhk, remove_pps_outliers, remove_bhk_outliers

from sklearn.model_selection import train_test_split

@dataclass
class DataIngestionConfig:
    raw_data_path = os.path.join("artifacts","raw.csv")
    clean_data_path = os.path.join("artifacts","clean.csv")
    train_data_path = os.path.join("artifacts","train.csv")
    test_data_path = os.path.join("artifacts","test.csv")
    location_path = os.path.join("artifacts","location.json")
    
class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
    
    def data_cleaning(self,df):
        try:
            # Cleaning the total_sqft data           
            logging.info("Cleaning the Total Square Feet Feature")
            df["total_sqft"] = df["total_sqft"].apply(convert_sqft_to_num)
            
            logging.info("Extracting the BHK Feature from the provided size feature")
            df["bhk"] = df["size"].apply(extracting_bhk)
            
            logging.info("Filling the missing valued for BHK, Bath, Total_sqft")
            df["bhk"] = df["bhk"].fillna(df["total_sqft"]//300) ### Assuming 300 sq. ft. is the minimum size
            df["bath"] = df["bath"].fillna(df["bhk"])
            df["total_sqft"] = df["total_sqft"].fillna(df["bhk"]*300)
            
            logging.info("Handling the Location Feature")
            df["location"] = df["location"].fillna("Others")
            df.location = df.location.apply(lambda x: x.strip().title())
            location_stats = df.groupby("location")["location"].agg("count").sort_values(ascending = False)
            location_stat_less_than_10 = location_stats[location_stats<=10]
            df.location = df.location.apply(lambda x: "Others" if x in location_stat_less_than_10 else x)
            
            df["Price_per_sqft"] = df["price"]*100000/df["total_sqft"]
            
            logging.info("Removing the Outliers for Total Sq. Feet and Bath using Domain Knowledge")
            #Removing the data that has 1BHK Sq. Ft. less than 300 As per domain knowledge
            df = df[df.bath<(df.bhk+2)]
            df_rm_sqft = df[~((df.total_sqft/df.bhk)<300)]
                        
            logging.info("Removing the Outliers for location and Price Per Sq. Ft.")
            
            df_rm_sqft_ppsqft = remove_pps_outliers(df_rm_sqft)
            
            
            logging.info("Removing the Outliers for BHK")
            df_rm_sqft_ppsqft_bhk = remove_bhk_outliers(df_rm_sqft_ppsqft)
            
            logging.info("Dropping the Unwanted Columns")
            df_final = df_rm_sqft_ppsqft_bhk.drop(["area_type","society","balcony","availability","size","Price_per_sqft"],axis=1)
            return df_final
        
        except Exception as e:
            raise CustomeException(e, sys)
    
    def initate_data_ingestion(self):
        try:
            df = read_data()
            logging.info("Data Reading Successful")
            
            os.makedirs(os.path.dirname(self.data_ingestion_config.raw_data_path),exist_ok=True)
            
            df.to_csv(self.data_ingestion_config.raw_data_path,index=False,header=True)
            
            logging.info("Data Cleaning Started")
            df_final = self.data_cleaning(df)
            logging.info("Data Cleaning Completed")
            
            df_final.to_csv(self.data_ingestion_config.clean_data_path,index=False, header=True)
            unique_location = list(df_final["location"].unique())
            location = {"location":unique_location}
            save_json(file_path=self.data_ingestion_config.location_path,json_file=location)
            
            
            train_set, test_set = train_test_split(df_final,test_size=0.2,random_state=10)
            
            train_set.to_csv(self.data_ingestion_config.train_data_path,index = False,header = True)   
            test_set.to_csv(self.data_ingestion_config.test_data_path,index = False,header = True) 
            
            return(
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.train_data_path
            )
            
            logging.info("Data Ingestion Completed")
        except Exception as e:
            raise CustomeException(e,sys)
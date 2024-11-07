import os
import sys
from src.logger import logging
from src.exception import CustomeException

import pandas as pd

import dill
import json

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import r2_score

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
    
def load_object (file_path):
    try:       
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
            
    except Exception as e:
        raise CustomeException(e , sys)
    
def save_json(file_path, json_file):
    try:
        dir_path = os.path.dirname(file_path)
        
        os.makedirs(dir_path,exist_ok=True)
        
        with open(file_path,"w") as file_json:
            json.dump(json_file,file_json,indent=4)
    except Exception as e:
        raise CustomeException(e,sys)
    
def load_json(file_path):
    try:
        with open(file_path,"r") as f:
            return json.load(f)
    except Exception as e:
        raise CustomeException(e,sys)
    
def evaluate_model(X_train,y_train,X_test,y_test, model_params):
    try:
        
        scores = {}
        cv = ShuffleSplit(n_splits=5,test_size=0.2,random_state=0)
        
        for model_name, mp in model_params.items():
            logging.info(f"Starting the Hyper parameter Tunnig for {model_name}")
            clf = GridSearchCV(mp["model"],mp["params"], cv = cv, return_train_score= False)
            clf.fit(X_train,y_train)
            
             # Store results
            best_params = clf.best_params_
            best_score = clf.best_score_
            
            # Calculate R² score on the test set
            best_model = clf.best_estimator_
            y_pred = best_model.predict(X_test)
            r2 = r2_score(y_test, y_pred)
          
            avg_score = best_score*0.6+r2*0.4
            # scores.append({
            #     "model" : model_name,
            #     "best_score" : best_score,
            #     "best_params": best_params,
            #     "test_r2_score": r2,
            #     "avg_best_score": avg_score
            # })
            scores[model_name]={
                "best_score" : best_score,
                "best_params": best_params,
                "test_r2_score": r2,
                "avg_best_score": avg_score
            }
            logging.info(f"Completed Hyper parameter Tunnig for {model_name} having scores as {best_score} and test R2 score as {r2} with the average best score as {avg_score}")
                   
        logging.info("Hyper parameter Tunning Complete")
        return scores
        
    except Exception as e:
        raise CustomeException(e,sys)
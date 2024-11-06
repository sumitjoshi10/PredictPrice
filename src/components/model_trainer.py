import os
import sys
from src.logger import logging
from src.exception import CustomeException

from dataclasses import dataclass

from src.utils import evaluate_model, save_json, save_object

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score

@dataclass
class ModelTrainerConfig():
    best_model_file_path = os.path.join("artifacts","best_model.json")
    trained_model_file_path = os.path.join("artifacts","model.pkl")
    
class ModelTrainer():
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        
    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Spliting the to Train and test data set")
            X_train, X_test, y_train, y_test = (
                train_array[:,:-1],
                test_array[:,:-1],
                train_array[:,-1],
                test_array[:,-1]
            )
            
            model_params = {
                "liner_regression":{
                    "model" : LinearRegression(),
                    "params":{
                    }
                },
                "lasso":{
                    "model" : Lasso(),
                    "params":{
                        "alpha" : [1,2],
                        "selection" : ["random", "cyclic"]
                    }
                },
                "decision_tree":{
                    "model" : DecisionTreeRegressor(),
                    "params":{
                        "criterion":["squared_error","friedman_mse"],
                        "splitter":["best","random"]
                    }
                }
            }
            
            scores = evaluate_model(X_train,y_train,X_test,y_test,model_params=model_params)
            save_json(
                file_path=self.model_trainer_config.best_model_file_path,
                json_file=scores
            )
            
            # Will get the best model name from the below.
            best_model_name = max(scores, key=lambda k: scores[k]['avg_best_score'])
            best_model_details = scores[best_model_name]
            
            # best_score_model = scores_df[scores_df['avg_best_score'] == scores_df['avg_best_score'].max()].to_dict(orient='records')[0]
            
            best_model = model_params[best_model_name]["model"]
            best_param = best_model_details["best_params"]
            
            best_model.set_params(**best_param)
            
            if best_model_details["test_r2_score"]<0.6:
                raise CustomeException("No best model found")
            
            logging.info("Best model found for both training and test data set")
            logging.info(f"{best_model} Model has been selected for model Training")
            
            best_model.fit(X_train,y_train)
            prediction = best_model.predict(X_test)
            r2 = r2_score(y_test,prediction)
            
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            
            
            logging.info(f"[{best_model}] Model with parameter [{best_model_details["best_params"]}] has been selected for model Training. It got [{r2}] score.")
            
        except Exception as e:
            raise CustomeException(e,sys)

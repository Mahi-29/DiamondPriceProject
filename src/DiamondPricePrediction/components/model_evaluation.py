import sys
import os
import pickle
import mlflow
from mlflow import sklearn
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
import numpy as np
from urllib.parse import urlparse
from src.DiamondPricePrediction.logger import logging
from src.DiamondPricePrediction.exception import customexception
from src.DiamondPricePrediction.utils.utils import load_object



class ModelEvaluation:
    def __init__(self) -> None:
        pass

    def eval_metrics(self,actual, predicted):
        mae = mean_absolute_error(actual, predicted)
        mse = mean_squared_error(actual, predicted)
        rmse = np.sqrt(mean_squared_error(actual, predicted))
        r2_square = r2_score(actual, predicted)
        return mae, rmse, r2_square

    def evaluate(self, test_array):
        try:
            X_test,y_test=(test_array[:,:-1], test_array[:,-1])

            model_path = os.path.join('artifacts','model.pkl')

            model = load_object(model_path)

            mlflow.set_registry_uri("https://dagshub.com/Mahi-29/DiamondPriceProject.mlflow")
                
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
            
            print(tracking_url_type_store)



            with mlflow.start_run():

                predicted_qualities = model.predict(X_test)

                (rmse, mae, r2) = self.eval_metrics(y_test, predicted_qualities)

                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("r2", r2)
                mlflow.log_metric("mae", mae)

                ## this condition is for dagshub
                # Model registry does not work with file store
                if tracking_url_type_store != "file":

                    # Register the model
                    # There are other ways to use the Model Registry, which depends on the use case,
                    # please refer to the doc for more information:
                    # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                    mlflow.sklearn.log_model(model, "model", registered_model_name="ml_model")
                else:
                    mlflow.sklearn.log_model(model, "model")
        except Exception as e:
            raise customexception(e, sys)


import os
import sys
from src.DiamondPricePrediction.logger import logging
from src.DiamondPricePrediction.exception import customexception
from src.DiamondPricePrediction.components.data_ingestion import DataIngestion
from src.DiamondPricePrediction.components.data_transformation import DataTransformation
from src.DiamondPricePrediction.components.model_trainer import ModelTrainer
import pandas as pd

obj=DataIngestion()

train_data_path,test_data_path=obj.initiate_data_ingestion()


transformation_obj = DataTransformation()
train_arr,test_arr = transformation_obj.initialize_data_transformation(train_data_path,test_data_path)

model_trainer_obj = ModelTrainer()
model_trainer_obj.initiate_model_training(train_arr, test_arr)

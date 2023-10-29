import pandas as pd
import numpy as np
from src.DiamondPricePrediction.logger import logging
from src.DiamondPricePrediction.exception import customexception
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from pathlib import Path
import os
import sys

@dataclass
class DataIngestionConfig:
    raw_data_path:str = os.path.join("artifacts","raw.csv")
    train_data_path:str = os.path.join("artifacts","train.csv")
    test_data_path:str = os.path.join("artifacts","test.csv")

class DataIngestion:

    def __init__(self) :
        self.ingestion_config = DataIngestionConfig
        
    def initiate_data_ingestion(self):
        logging.info("data ingestion Started")

        try:
            data = pd.read_csv(Path(os.path.join("notebooks/data","gemstone.csv")))

            logging.info("dataset read successfully as df")
            
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path,index=False)
            logging.info("Stored the Raw data in artifacts folder")

            logging.info("starting train test Split")
            train_data, test_data = train_test_split(data,test_size=0.25)
            
            logging.info("performed test train split")
            train_data.to_csv(self.ingestion_config.train_data_path,index = False )
            test_data.to_csv(self.ingestion_config.test_data_path, index=False)
            logging.info("Data ingestion completed")

        except Exception as e :
            logging.info("exception during occurred at data ingestion stage")
            raise customexception(e,sys)

import pandas as pd
import numpy as np 
import os
import sys
from dataclasses import dataclass
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from src.DiamondPricePrediction.logger import logging
from src.DiamondPricePrediction.exception import customexception
from src.DiamondPricePrediction.utils.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:

    def __init__(self) -> None:
        self.data_transformation_config = DataTransformationConfig()
        
    def get_data_transformation(self):
        try:
            logging.info("Initialized get_data_transformation")

            # Define which columns should be ordinal-encoded and which should be scaled
            categorical_cols = ['cut', 'color','clarity']
            numerical_cols = ['carat', 'depth','table', 'x', 'y', 'z']
            
            # Define the custom ranking for each ordinal variable
            cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']

            num_pipeline  = Pipeline(
                [
                    ('Missing_value_handler', SimpleImputer(strategy='median')),
                    ("Standard_scaler",StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                [
                    ('Imputer', SimpleImputer(strategy='most_frequent')),
                    ('Ordinal_encoder', OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories]))
                ]
            )

            preprocessor=ColumnTransformer(
                [
                    
                    ('num_pipeline',num_pipeline,numerical_cols),
                    ('cat_pipeline',cat_pipeline,categorical_cols)
                ]
            )

            logging.info("get_data_transformation initialized the preprocessor")

            return preprocessor

        except Exception as e:
            logging.info(f"Exception ocurred in the get_data_transformation : {e} ")
            raise customexception(e,sys)
        
    def initialize_data_transformation(self,train_path,test_path):
        try:
            
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Data Loading from csv file completed")

            logging.info(f'Train Dataframe Head : \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head : \n{test_df.head().to_string()}')

            preprocessing_obj = self.get_data_transformation()

            target_col_name = 'price'
            drop_columns = [target_col_name,'id']
            
            input_feature_train_df = train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df = train_df[target_col_name]

            input_feature_test_df = test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df = test_df[target_col_name]

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)

            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            logging.info("Successfully applied the preprocessor on test and train data")

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            logging.info("Preprocessing pickle file stored")

            return(
                train_arr,
                test_arr
            )



        except Exception as e:
            logging.info(f"Exception ocurred at the initialize_data_transformer : {e}")
            raise customexception(e,sys)
            

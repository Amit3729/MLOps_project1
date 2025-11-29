import sys
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer

from src.constants import TARGET_COLUMN, SCHEMA_FILE_PATH
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import  DataTransformationArtifact, DataIngestionArtifact, DataValidationArtifact
from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import save_object, save_numpy_arry_data,read_yaml_file


class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_tansformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_tansformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e,sys) from e
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e, sys)
        
    
    def get_data_tranformer_obj(self)->Pipeline:
        ''''
        Creates and returns a data transformer object for the data,
        including gender mapping,dummy variable creation, columns renaming, feature scaling and type adjustments.

        '''
        logging.info('Entere get_data_transformer_obj method of DtataTransformation class')

        try:
            #Initilize Tranformers
            numeric_transformer = StandardScaler()
            min_max_scaler = MinMaxScaler()
            logging.info("Transformers Initilized : StandardScaler-MinMaxScaler")

            #load schema configurations
            num_features = self._schema_config['num_features']
            mm_columns = self._schema_config['mm_columns']
            logging.info('cols loaded from schema.')

            #creating preprocessing pipeline
            preprocessor = ColumnTransformer(
                transformers=[
                    ("StandardScaler", numeric_transformer,num_features),
                    ("MinMAxScaler",min_max_scaler,mm_columns)
                ],
                remainder='passthrough' #leaves other columsn as they are
            )
            #wrapping everythings in a single pipeline
            final_pipeline = Pipeline(steps=[('Preprocessor', preprocessor)])
            logging.info('final pipeline ready!')
            logging.info('Exited get_data_transformer_object method od DataTransformation class')
            return final_pipeline
        
        except Exception as e:
            logging.exception("exception occured in get_data_transformer_object method of DataTransformation class")
            raise MyException(e,sys) from e
    
    def _map_gender_column(self,df):
        '''Map gender columns to set 0 for demale and 1 for male'''
        logging.info("mapping 'Gender' columns to binary values")
        df['Gender'] = df['Gender'].map({'Female':0, 'Male':1}).astype(int)
        return df
    
    def _create_dummy_columns(self,df):
        logging.info('Create dummy variable for categorical features')
        df = pd.get_dummies(df, drop_first=True)
        return df
    
    def _rename_columns(self,df):
        logging.info("Renaming specific columns and casting to 'int'")
        df = df.rename(columns={
            "Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
            "Vehicle_Age_< 2 Year": "Vehicle_Age_gt_1_Year"
        })
        for col in ['Vehicle_Age_lt_1_year', 'Vehicle_Age_gt_2_Years', 'Vehicle_Damage_Yes']:
            if col in df.columns:
                df[col] = df[col].astype('int')
        return df
    
    def _drop_id_column(self, df):
        logging.info("Dropping 'id' column")
        drop_col = self._schema_config['drop_columns']
        if drop_col in df.columns:
            df = df.drop(drop_col, axis= 1)
        return df
    
    def initiate_data_transformation(self)-> DataTransformationArtifact:
        '''
        Initiates the data transformation component for the pipeline
        '''
        try:
            logging.info('Data Transformation started')
            if not self.data_validation_artifact.validation_status:
                raise Exception(self.data_validation_artifact.message)
            
            #Load train and test data
            train_df = self.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(file_path=self.data_ingestion_artifact.test_file_path)
            logging.info('train-test data loaded')

            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            logging.info('Input and Target cols defined for both train and test df')

            #apply custom transformation in specified sequence
            input_feature_train_df=self._map_gender_column(input_feature_train_df)
            input_feature_train_df=self._drop_id_column(input_feature_train_df)
            input_feature_train_df=self._create_dummy_columns(input_feature_train_df)
            input_feature_train_df=self._rename_columns(input_feature_train_df)

            input_feature_test_df=self._map_gender_column(input_feature_test_df)
            input_feature_test_df=self._drop_id_column(input_feature_test_df)
            input_feature_test_df=self._create_dummy_columns(input_feature_test_df)
            input_feature_test_df=self._rename_columns(input_feature_test_df)
            logging.info('Custom Transformation applied to train and test data')

            logging.info('Starting data transformation')
            preprocessor = self.get_data_tranformer_obj()
            logging.info('Got the preprocessor object')

            logging.info('Initilizing transformation for training data')
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            logging.info('Initilizing transformation for testing data')
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)
            logging.info('Transformation done end to end to train-test df')

            logging.info('Applying SMOTEENN for handling imblanced datasets.')
            smt = SMOTEENN(sampling_strategy="minority")
            input_feature_train_final, target_feature_train_final = smt.fit_resample(input_feature_train_arr,target_feature_train_df)
            input_feature_test_final, target_feature_test_final = smt.fit_resample(input_feature_test_arr,target_feature_test_df)

            logging.info("Smoteenn applied to trin-test data")

            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]
            logging.info("featire-target concatenation done for train-test df")

            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor)
            save_numpy_arry_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_arry_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            logging.info("Saving transformation object and transformed files.")

            logging.info("Data transformation completed sucessfully")
            return DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
        except Exception as e:
            raise MyException(e,sys) from e 


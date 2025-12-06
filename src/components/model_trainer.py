import sys
from typing import Tuple

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,f1_score,precision_score,recall_score

from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import load_numpy_array_data, load_object, save_object
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact,ClassificationMetricArtifact
from src.entity.estimator import MyModel

class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact, 
                 model_trainer_config : ModelTrainerConfig):
        '''
        param data_transformation_artifact : Output reference of data transformation artifact stage
        param model_trainer_config: configuration for model training

        '''
        self.data_transformation_artfact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config
    
    def get_model_object_and_report(self, train : np.array, test:np.array)-> Tuple[object,object]:
        '''
        This function trains a RandomForestClassifier with specified parameters
        Returns metric artifact object and trained model object
        
        '''
        try:
            logging.info("Training RandomForestClassifier with specified parameters")

            #splitting train and test data into features and taget variables
            x_train, y_train, x_test, y_test = train[:, :-1], train[:,-1], test[:,:-1],test[:,-1]
            logging.info("Train-test split done")

            model = RandomForestClassifier(
                n_estimators = self.model_trainer_config.n_estimators,
                min_samples_split = self.model_trainer_config.min_samples_split,
                min_samples_leaf= self.model_trainer_config.min_samples_leaf,
                max_depth= self.model_trainer_config.max_depth,
                criterion= self.model_trainer_config.criterion,
                random_state= self.model_trainer_config.random_state

            )
            #fit the model
            logging.info("Model training stated")
            model.fit(x_train,y_train)
            logging.info("Model Training Done")

            #predicition and evulation metrics
            y_pred = model.predict(x_test)
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            precision = precision_score(y_test,y_pred)
            recall = recall_score(y_test,y_pred)

            #Creating metric artifact
            metric_artifact = ClassificationMetricArtifact(f1_score=f1, precision_score=precision,recall_score=recall)
            return model,metric_artifact
            
        except Exception as e:
            raise MyException(e,sys) from e
        
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")
        '''
        This function initiate the model training steps.
        Return model trainer artifact

        '''
        try:
            print(50*'-')
            print("starting Model Trainer Component")
            #load transformed train and test data
            train_arr = load_numpy_array_data(file_path=self.data_transformation_artfact.transformed_train_file_path)
            test_arr = load_numpy_array_data(file_path=self.data_transformation_artfact.transformed_test_file_path)
            logging.info("train-test data loaded")

            #Train model and get metrics
            trained_model, metric_artifact = self.get_model_object_and_report(train=train_arr, test=test_arr)
            logging.info("Model object and artifact loaded")

            #load preprocessing object
            preprocessing_obj = load_object(file_path=self.data_transformation_artfact.transformed_object_file_path)
            logging.info("Preprocessing object loaded")

            #check if the model's accuracy meets the expected threshold
            if accuracy_score(train_arr[:,-1],trained_model.predict(train_arr[:,:-1])) < self.model_trainer_config.expected_accuracy:
                logging.info("No model found with score above the base score")
                raise Exception("No model found with above the base score")
            
            #save the final model object that includes both preprocessing and trained model
            logging.info("Saving new model as performacne is better than previous one")
            my_model = MyModel(preprocessing_object=preprocessing_obj, trained_model_object=trained_model)
            save_object(self.model_trainer_config.trained_model_file_path, my_model)
            logging.info("Saved final model object that includes both preprocessing and the trained model")

            #Created and return the ModelTrainerArtifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact= metric_artifact,
                preprocessor_path=self.data_transformation_artfact.transformed_object_file_path
            )
            logging.info(f'Model trainer artifact: {model_trainer_artifact}')
            return model_trainer_artifact
        except Exception as e:
            raise MyException(e,sys) from e
        


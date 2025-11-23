import sys

import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline

from src.exception import MyException
from src.logger import logging

class TargetValueMapping:
    def __init__(self):
        self.yes:int = 0
        self.mo:int = 1
    def _asdict(self):
        return self.__dict__
    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))    


class MyModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        '''
        :param preprocessing_object : Input obj of preprocessor
        param trained_model_obj = Input obj of trained model
        '''
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: pd.DataFrame)->DataFrame:
        '''
        Function accepts preporcessed inputs(with all custom transformation already applied),
        applies scaling using preprocessing_object and perfome prediction on transformed features.
        '''
        try:
            logging.info("starting predicition process")
            transformed_feature = self.preprocessing_object.transform(dataframe)
            logging.info("using the trained model to get predictions")
            predicition = self.trained_model_object.predict(transformed_feature)
            return predicition
        except Exception as e:
            raise MyException(e, sys) from e
        
    
    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"
    
    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"
    
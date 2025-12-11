import sys 
from src.entity.config_entity import VehiclePredictorConfig
from src.entity.s3_estimator import Proj1Estimator
from src.exception import MyException
from src.logger import logging
from pandas import DataFrame

class VehicleData:
    def __init__(self,
                 Gender,
                 Age,
                 Driving_License,
                 Region_Code,
                 Previously_Insured,
                 Vehicle_Age,
                 Vehicle_Damage,
                 Annual_Premium,
                 Policy_Sales_Channel,
                 Vintage):
        '''
        Vehicle data Constructor
        Input: All features of trained model for prediction
        '''
        try:
            self.Gender = Gender
            self.Age = Age
            self.Driving_License = Driving_License
            self.Region_Code = Region_Code
            self.Previously_Insured = Previously_Insured
            self.Vehicle_Age = Vehicle_Age
            self.Vehicle_Damage = Vehicle_Damage
            self.Annual_Premium = Annual_Premium
            self.Policy_Sales_Channel = Policy_Sales_Channel
            self.Vintage = Vintage
        
        except Exception as e:
            raise MyException(e, sys) from e
        
    def get_vehicle_input_data_frame(self) -> DataFrame:
        '''
        This function returns a DataFrame from class input
        '''
        try:
            vehicle_input_dict = self.get_vehicle_data_as_dict()
            return DataFrame(vehicle_input_dict)
        except Exception as e:
            raise MyException(e, sys) from e 
    
    def get_vehicle_data_as_dict(self):
        '''
        Returns a dictionary from vehicleData class input
        '''
        try:
            input_data = {
                "Gender": [self.Gender],
                "Age": [self.Age],
                "Driving_License": [self.Driving_License],
                "Region_Code": [self.Region_Code],
                "Previously_Insured": [self.Previously_Insured],
                "Vehicle_Age": [self.Vehicle_Age],
                "Vehicle_Damage": [self.Vehicle_Damage],
                "Annual_Premium": [self.Annual_Premium],
                "Policy_Sales_Channel": [self.Policy_Sales_Channel],
                "Vintage": [self.Vintage]
            }
            #check the debug
            df = DataFrame(input_data)
            logging.info(f"🔍 DataFrame columns: {df.columns.tolist()}")
            logging.info(f"🔍 DataFrame shape: {df.shape}")
            logging.info(f"🔍 DataFrame values:\n{df.to_dict('records')}")
            logging.info(f"🔍 Vehicle_Age type: {type(self.Vehicle_Age)}, value: '{self.Vehicle_Age}'")
            logging.info(f"🔍 Vehicle_Damage type: {type(self.Vehicle_Damage)}, value: '{self.Vehicle_Damage}'")
        

            

            
            logging.info("Created vehicle data dict")
            logging.info("Exited get_vehicle_data_as_dict method as VehicleData Class")
            return input_data
        except Exception as e:
            raise MyException(e, sys) from e
    
class VehicleDataClassifier:
    def __init__(self, prediction_pipeline_config: VehiclePredictorConfig = VehiclePredictorConfig()):
        '''
        prediction_pipeline_config: Configuration for prediction the value
        '''
        try:
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise MyException(e, sys)
    
    def predict(self, dataframe) -> str:
        '''
        returns prediction in string format
        '''
        try:
            logging.info("Entered predict method of VehicleDataClassifier class")
            model = Proj1Estimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )
            result = model.predict(dataframe)
            return result
        except Exception as e:
            raise MyException(e, sys)
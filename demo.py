# #to check the logging config
# from src.logger import logging

# logging.debug('Thos is a debug message')
# logging.info('Thos is a info message')
# logging.warning('Thos is a warning message')
# logging.error('Thos is a error message')
# logging.critical('Thos is a critical message')

#below code to check expection config
# from src.logger import logging
# from src.exception import MyException
# import sys

# try:
#     a=1+'z'
# except Exception as e:
#     logging.info(e)
#     raise MyException(e, sys) from e

from src.pipeline.training_pipeline import TrainPipeline

pipeline = TrainPipeline()
pipeline.run_pipeline()
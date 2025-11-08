import sys
import logging

def error_message_detail(error: Exception, error_details: sys):
    '''
    Extracts detailed error information including file name, line number and the error meaasge.
    
    param error: This expection that occured.
    param error_detail: the sys module to access trackback details.
    return: A formatted error message string.

    '''

    #Extract traceback details(expection information)
    _, _, exc_tb = error_details.exc_info()

    #Get the file name where the expection occured
    file_name = exc_tb.tb_frame.f_code.co_filename

    #create a formatted error message string with file name, line number and actual error
    line_number = exc_tb.tb_lineno
    error_message = f'Error occured in python script: [{file_name}] at a line number [{line_number}]: {str(error)}'

    #Log the error for better tracking
    logging.error(error_message)

    return error_message

class MyException(Exception):
    '''
    Custom expection class for handeling error in the us visa application.
    '''
    def __init__(self, error_message, error_details):
        '''
        Initializes the USvisaEXpection with detailed error message.

        param error_message:A string describing the error.
        param error_detail: The sys module to access traceback details.
        '''
        #call the base class constructor with error message
        super().__init__(error_message)

        #format the detailed error message using the error_message_detail function
        self.error_message = error_message_detail(error_message,error_details)

    def __str__(self):
        '''
        Returns the string representation of the error message.
        '''
        return self.error_message
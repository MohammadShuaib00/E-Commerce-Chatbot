import os
import sys
import logging
import traceback


# Function to extract error message and details including traceback
def error_message_details(error_message, error_details: sys):
    # Get the exception type, value, and traceback
    _, _, exc_tb = error_details.exc_info()

    # Get the file name, line number, and function name where the error occurred
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    function_name = exc_tb.tb_frame.f_code.co_name

    # Format the detailed error message
    detailed_error_message = f"Error occurred in file: {file_name}, line: {line_number}, function: {function_name}\n"
    detailed_error_message += f"Error message: {error_message}\n"
    detailed_error_message += f"Traceback: {traceback.format_exc()}"

    return detailed_error_message


# Custom exception class
class aiChatbot(Exception):
    def __init__(self, error_message, error_details=sys.exc_info()):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_details)

    def __str__(self):
        return self.error_message
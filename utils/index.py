from datetime import datetime, date
import json

class ResponseExecption(Exception):
    def __init__(self, message, status):
        super().__init__(message)
        self.status = status
        self.message = message


# Define a function to convert non-serializable types
def convert_datetime_to_string(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Convert datetime to ISO 8601 format string
    elif isinstance(obj, date):
        return obj.isoformat()  # Convert date to ISO 8601 format string
    # Add other conversions as needed
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")



def convert_query_result_to_json(results, rows):
    if rows:
       column_names = results.keys()    
       data_list = [dict(zip(column_names, row)) for row in rows]
    else:
       data_list = []
    json_data = json.dumps(data_list, default=convert_datetime_to_string, indent=4)
    return json_data
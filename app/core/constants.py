class ResponseMessage:
    RECORD_NOT_FOUND = "Record was not found."
    RECORD_SAVED = "Successfully saved record."
    RECORD_NOT_SAVED = "Record was not saved."
    RECORD_UPDATED = "Successfully updated record."
    RECORD_NOT_UPDATED = "Record was not updated."
    RECORD_DELETED = "Successfully deleted record."
    RECORD_NOT_DELETED = "Record was not deleted."
    RECORD_ALREADY_DELETED = "The record was deleted and is no longer available."
    RECORD_EXISTS = "Record already exists."
    RECORD_STILL_REFERENCED = "Record is still referenced."
    SERVICE_ERROR = "There was an error with the service."
    FORBIDDEN = "You are not allowed to access resource."
    REQUEST_INCOMPLETE = "Request was not completed."
    UNAUTHORIZED = "Request was not authorized."
    PROVIDE_DELETE_PARAMETERS = "Provide delete parameters for composite table."
    CANNOT_INDEX = "Endpoint records cannot be indexed."
    SEARCH_FAILED = "Search query failed."


class Message:
    ERROR = 'Error occurred'
    VALIDATION_ERROR = 'Field validation error'
    SUCCESS = 'Successfully completed'

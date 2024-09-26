from utilities.custom_log import logger


statusCodeErrorMessages = {
    422: 'unprocessable_entity',
    404: 'not_found',
    500: 'internal_server_error',
    405: 'method_not_allowed',
    401: 'invalid_token'
}


def handle_error_status_codes(status_code):
    if status_code in statusCodeErrorMessages:
        return statusCodeErrorMessages[status_code]


def handle_exception_standard_messages(exception, apiName, token):
    logger.error(str(exception), extra={'apiName': apiName, 'token': token})

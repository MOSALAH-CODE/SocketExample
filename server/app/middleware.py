import json
from fastapi import Request, Response
from pydantic import ValidationError
from models import StandardResponse
from utilities.custom_log import logger
from utilities.error_handling import handle_error_status_codes, handle_exception_standard_messages
from utilities.config_variables import ALLOWED_ORIGINS


async def get_response_body(response):
    responseBody = b""
    async for chunk in response.body_iterator:
        responseBody += chunk

    responseBodyStr = responseBody.decode()

    return responseBodyStr


async def create_error_status_codes_response(status_code, responseBodyStr, apiName, token):
    errorMessage = handle_error_status_codes(status_code) if handle_error_status_codes(
        status_code) is not None else responseBodyStr
    standardResponse = StandardResponse(
        success=False, error=errorMessage, body=None)
    logger.error(str({responseBodyStr}), extra={
                 'apiName': apiName, 'token': token})
    return standardResponse.model_dump()


async def handle_success_response(responseBodyJson):
    standardResponse = StandardResponse(success=True, body=responseBodyJson)
    return standardResponse.model_dump()


async def form_Response_object(content):

    FinalResponse = Response(content=json.dumps(content), status_code=200)

    FinalResponse.headers["Content-Type"] = "application/json"
    return FinalResponse


async def standard_response(request: Request, call_next):
    try:
        apiName = request.url.path
        # Extract the token from the Authorization header
        token = request.headers.get('Authorization')
        if token and token.startswith("Token"):
            token = token[len("Token"):].strip()

        response = await call_next(request)
    except ValidationError as e:
        handle_exception_standard_messages(e, apiName, token)
        error_details = e.errors()[0]['loc'][0]
        return await form_Response_object(StandardResponse(success=False, error=str(error_details)+"_felid_error", body=None).model_dump())
    except Exception as e:
        handle_exception_standard_messages(e, apiName, token)
        return await form_Response_object(StandardResponse(success=False, error='internal_server_error', body=None).model_dump())

    responseBodyStr = await get_response_body(response)
    try:
        responseBodyJson = json.loads(responseBodyStr)

    except json.JSONDecodeError as e:
        responseBodyJson = {}

    if response.status_code >= 400:
        standardResponse = await create_error_status_codes_response(response.status_code, responseBodyStr, apiName, token)
    else:
        standardResponse = await handle_success_response(responseBodyJson)

    return await form_Response_object(standardResponse)

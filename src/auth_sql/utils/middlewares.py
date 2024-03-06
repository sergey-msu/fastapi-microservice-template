'''
    App-wide custom middlewares
'''
import logging

from fastapi import status
from fastapi import Request
from fastapi import Response
from fastapi.responses import JSONResponse
from fastapi.utils import is_body_allowed_for_status_code

from utils.utils import ex_details


async def app_exception_handler(request: Request, exc: Exception) -> Response:
    log_error(request)

    detail = getattr(exc, 'detail', 'Internal server error')
    status_code = getattr(exc, 'status_code', status.HTTP_500_INTERNAL_SERVER_ERROR)
    headers = getattr(exc, 'headers', {'Content-Type': 'application/json'})

    if not is_body_allowed_for_status_code(status_code):
        return Response(status_code=status_code, headers=headers)

    return JSONResponse(
        {'detail': detail}, status_code=400, headers=headers,
    )


def log_error(request: Request):
    # logging customization
    host = getattr(getattr(request, 'client', None), 'host', None)
    port = getattr(getattr(request, 'client', None), 'port', None)
    url = f'{request.url.path}?{request.query_params}' if request.query_params else request.url.path
    exception_details = ex_details()
    message = f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error: - {exception_details}'

    logging.getLogger().error(message)

import os
import sys
import ast
import traceback
from cryptography.fernet import Fernet

from utils.consts import MODE_ENV_VAR
from utils.consts import SECRET_ENV_VAR


def load_secrets():
    app_mode = os.environ[MODE_ENV_VAR].lower()
    secret_key = os.environ[SECRET_ENV_VAR]

    with open(f'secrets.{app_mode}', 'rb') as f:
        secrets_encoded = Fernet(secret_key).decrypt(f.read()).decode()
        secrets = ast.literal_eval(secrets_encoded)
        for key, value in secrets.items():
            os.environ[key] = value


def ex_details():
    exception_type, exception_value, exception_traceback = sys.exc_info()
    exception_name = getattr(exception_type, '__name__', None)
    exception_traceback = ''.join(traceback.format_tb(exception_traceback))
    exception_details = f'{exception_name}: {exception_value}\n{exception_traceback}'

    return exception_details

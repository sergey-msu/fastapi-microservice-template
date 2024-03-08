import sys
import traceback


def ex_details():
    exception_type, exception_value, exception_traceback = sys.exc_info()
    exception_name = getattr(exception_type, '__name__', None)
    exception_traceback = ''.join(traceback.format_tb(exception_traceback))
    exception_details = f'{exception_name}: {exception_value}\n{exception_traceback}'

    return exception_details

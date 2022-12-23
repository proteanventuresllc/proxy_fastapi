import logging
from functools import partial

from starlette.exceptions import HTTPException
from starlette.responses import Response
from tenacity import (retry, retry_if_exception_type, stop_after_delay,
                      wait_fixed)


def return_fail(_):
    # This is weird part.. will improve in future
    _.outcome.result()

def log_try(retry_state):
    logging.error(f"Retrying: {retry_state.attempt_number} {retry_state.kwargs}")

retry_on_dead_upstream = partial(
    retry,
    stop=stop_after_delay(10),
    wait=wait_fixed(0.3),
    retry_error_callback=return_fail,
    after=log_try,
    retry=retry_if_exception_type(HTTPException)
)()

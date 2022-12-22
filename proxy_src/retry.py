from functools import partial
from starlette.responses import Response 
from tenacity import retry, stop_after_delay, wait_fixed, retry_if_exception_type

class DeadUpstreamError(Exception):
    pass

def return_fail(_):
    return Response(
        'dead upstream',
        media_type='text/plain',
        status_code=503
    )

retry_on_dead_upstream = partial(
    retry,
    stop=stop_after_delay(10),
    wait=wait_fixed(0.3),
    retry_error_callback=return_fail,
    retry=retry_if_exception_type(DeadUpstreamError)
)()

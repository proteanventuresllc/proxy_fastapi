import httpx
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse

from .retry import DeadUpstreamError, retry_on_dead_upstream
from .settings import settings

RETRY_CODE = 503;

_client = httpx.AsyncClient(base_url=settings.target_host)



@retry_on_dead_upstream
async def client(
    path,
    query,
    method,
    headers,
    content
):
    url = httpx.URL(
        path=path,
        query=query
    )
    request = _client.build_request(
            method, url,
            headers=headers,
            content=content
    )
    response = await _client.send(request, stream=True)

    if response.status_code == RETRY_CODE:
        raise DeadUpstreamError

    return StreamingResponse(
        response.aiter_raw(),
        status_code=response.status_code,
        headers=response.headers,
        background=BackgroundTask(response.aclose),
    )

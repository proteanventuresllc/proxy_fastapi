import httpx
from starlette.background import BackgroundTask
from starlette.exceptions import HTTPException
from starlette.responses import StreamingResponse

from .retry import retry_on_dead_upstream
from .settings import settings

RETRY_CODES = settings.retry_codes;

_client = httpx.AsyncClient(base_url=settings.target_host, timeout=None)



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

    if response.status_code in RETRY_CODES:
        raise HTTPException(response.status_code, detail="Can't resolve request")

    return StreamingResponse(
        response.aiter_raw(),
        status_code=response.status_code,
        headers=response.headers,
        background=BackgroundTask(response.aclose),
    )

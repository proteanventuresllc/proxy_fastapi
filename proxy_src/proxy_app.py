
from fastapi import FastAPI
from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.responses import StreamingResponse

from .client import client

app = FastAPI()



@app.api_route("/health", methods=["GET"])
def health():
    return { 'message': 'success' }

@app.api_route("/{full_path:path}", methods=["GET", "POST"])
async def mask_request(request: Request):
    response = await client(
        path=request.url.path,
        query=request.url.query.encode("utf-8"),
        method=request.method,
        headers=request.headers.raw,
        content=await request.body()
    )
    return response

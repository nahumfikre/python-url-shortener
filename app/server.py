from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, AnyUrl
from .data_handler import UrlLogger
from .helpers import make_short_code, is_valid_code
from typing import Optional
import time

app = FastAPI(title='url shortener')

store = UrlLogger('data/links.log')
SITE_ROOT = 'http://localhost:8000'


class LinkRequest(BaseModel):
    url: AnyUrl
    custom: Optional[str] = None
    ttl: Optional[int] = None


@app.get('/ping')
def ping():
    # basic health check
    return {'ok': True, 'ts': int(time.time())}


@app.post('/new')
def create_link(data: LinkRequest, request: Request):
    # use a custom code if provided, otherwise generate one
    if data.custom:
        if not is_valid_code(data.custom):
            raise HTTPException(400, 'custom code must be 3–12 letters/numbers')
        if store.fetch(data.custom):
            raise HTTPException(409, 'custom code already exists')
        code = data.custom
    else:
        code = make_short_code()
        tries = 0
        while store.fetch(code) and tries < 5:
            code = make_short_code()
            tries += 1
        if store.fetch(code):
            raise HTTPException(500, 'could not find a free code')

    # optional link expiration
    if data.ttl and data.ttl <= 0:
        raise HTTPException(400, 'ttl must be positive')

    store.save(code, str(data.url), ttl_seconds=data.ttl)
    short_url = f'{SITE_ROOT}/{code}'
    print(f'[{int(time.time())}] {code} -> {data.url}')

    return {'code': code, 'short': short_url}


@app.get('/{code}')
def go(code: str):
    # redirect to the original link
    target = store.fetch(code)
    if not target:
        raise HTTPException(404, 'link not found')
    return RedirectResponse(url=target, status_code=301)


@app.get('/show/{code}')
def show(code: str):
    # view stored info for a short code
    item = store.peek(code)
    if not item:
        raise HTTPException(404, 'no such code')
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.server:app", host="127.0.0.1", port=8000, reload=True)
from __future__ import annotations

import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request

from app.core.config import settings

_buckets: dict[str, deque[float]] = defaultdict(deque)


async def enforce_rate_limit(request: Request) -> None:
    identity = request.headers.get("authorization") or request.client.host or "anonymous"
    key = f"{request.method}:{request.url.path}:{identity}"
    now = time.time()
    window = settings.RATE_LIMIT_WINDOW_SECONDS
    bucket = _buckets[key]
    while bucket and bucket[0] <= now - window:
        bucket.popleft()
    if len(bucket) >= settings.RATE_LIMIT_REQUESTS:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    bucket.append(now)

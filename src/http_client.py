from dataclasses import dataclass
from typing import Any, Dict, Optional
import requests

@dataclass
class HttpError(Exception):
    status_code: int
    url: str
    body: Any

def get_json(url: str, headers: Dict[str, str], timeout_s: int = 30) -> Any:
    r = requests.get(url, headers=headers, timeout=timeout_s)
    content_type = (r.headers.get("content-type") or "").lower()

    try:
        body = r.json() if "application/json" in content_type else r.text
    except Exception:
        body = r.text

    if not r.ok:
        raise HttpError(status_code=r.status_code, url=url, body=body)

    return body

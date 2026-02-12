from dataclasses import dataclass
from typing import Any, Dict, Optional
import time
import random
import logging

import requests

log = logging.getLogger(__name__)

@dataclass
class HttpError(Exception):
    status_code: int
    url: str
    body: Any

def _should_retry(status: int) -> bool:
    return status in (429, 500, 502, 503, 504)

def get_json(
    url: str,
    headers: Dict[str, str],
    timeout_s: int = 30,
    max_retries: int = 5,
    base_backoff_s: float = 0.8,
) -> Any:
    """
    GET JSON with retry/backoff for transient errors (429/5xx).
    """
    last_exc: Optional[Exception] = None

    for attempt in range(max_retries + 1):
        try:
            r = requests.get(url, headers=headers, timeout=timeout_s)
            content_type = (r.headers.get("content-type") or "").lower()

            try:
                body = r.json() if "application/json" in content_type else r.text
            except Exception:
                body = r.text

            if r.ok:
                return body

            # non-2xx
            if _should_retry(r.status_code) and attempt < max_retries:
                # exponential backoff with jitter
                sleep_s = (base_backoff_s * (2 ** attempt)) * (0.8 + 0.4 * random.random())
                log.warning(
                    "Retrying (%s/%s) HTTP %s for %s (sleep=%.2fs)",
                    attempt + 1, max_retries, r.status_code, url, sleep_s
                )
                time.sleep(sleep_s)
                continue

            raise HttpError(status_code=r.status_code, url=url, body=body)

        except requests.RequestException as e:
            last_exc = e
            if attempt < max_retries:
                sleep_s = (base_backoff_s * (2 ** attempt)) * (0.8 + 0.4 * random.random())
                log.warning(
                    "RequestException retry (%s/%s) for %s: %s (sleep=%.2fs)",
                    attempt + 1, max_retries, url, str(e), sleep_s
                )
                time.sleep(sleep_s)
                continue
            raise

    # fallback (teoricamente não chega aqui)
    if last_exc:
        raise last_exc
    raise RuntimeError("Unexpected HTTP client failure")

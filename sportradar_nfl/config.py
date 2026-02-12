from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

def must_get(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing env var: {name}")
    return v

@dataclass(frozen=True)
class SportradarConfig:
    api_key: str
    access_level: str
    lang: str
    fmt: str
    version: str
    base_url: str
    product_root: str = "/nfl/official"

config = SportradarConfig(
    api_key=must_get("SPORTRADAR_API_KEY"),
    access_level=must_get("SPORTRADAR_ACCESS_LEVEL"),
    lang=must_get("SPORTRADAR_LANG"),
    fmt=must_get("SPORTRADAR_FORMAT"),
    version=must_get("SPORTRADAR_VERSION"),
    base_url=must_get("SPORTRADAR_BASE_URL"),
)

DEFAULT_HEADERS = {
    "accept": "application/json",
    "x-api-key": config.api_key,
}
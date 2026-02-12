import json
import logging
import re
from pathlib import Path

from sportradar_nfl.nfl_service import (
    get_teams,
    get_team_seasonal_statistics,
)

logging.basicConfig(level=logging.INFO)

SEASON_YEAR = 2024
SEASON_TYPE = "REG"

OUT_DIR = Path("data/raw/season_stats/2024_REG")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def slugify_team(market: str, name: str) -> str:
    base = f"{market} {name}".strip().lower()
    base = re.sub(r"[^a-z0-9]+", "_", base)
    base = re.sub(r"_+", "_", base).strip("_")
    return base


def save_json(path: Path, payload: dict) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    teams_payload = get_teams()
    teams = teams_payload.get("teams", []) or []

    logging.info("Starting 2024 REG stats download for %s teams", len(teams))

    ok = 0
    fail = 0

    for idx, t in enumerate(teams, start=1):
        team_id = t["id"]
        market = t.get("market", "")
        name = t.get("name", "")
        slug = slugify_team(market, name)

        try:
            logging.info("[%02d/32] Fetching stats: %s %s", idx, market, name)
            payload = get_team_seasonal_statistics(SEASON_YEAR, SEASON_TYPE, team_id)

            out_file = OUT_DIR / f"{slug}.json"
            save_json(out_file, payload)
            ok += 1

        except Exception as e:
            logging.exception("Failed %s %s (%s): %s", market, name, team_id, str(e))
            fail += 1

    logging.info("Finished 2024 REG season stats | OK=%s | FAIL=%s", ok, fail)


if __name__ == "__main__":
    main()

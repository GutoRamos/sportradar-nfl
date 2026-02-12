import json
import logging
import re
from pathlib import Path

from sportradar_nfl.nfl_service import get_teams, get_team_seasonal_statistics

logging.basicConfig(level=logging.INFO)

OUT_DIR = Path("data/raw/season_stats")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def slugify_team(market: str, name: str) -> str:
    base = f"{market} {name}".strip().lower()
    base = re.sub(r"[^a-z0-9]+", "_", base)
    base = re.sub(r"_+", "_", base).strip("_")
    return base

def main():
    # ajuste conforme sua necessidade
    SEASON_YEAR = 2025
    SEASON_TYPE = "REG"  # REG / PST

    teams_payload = get_teams()
    teams = teams_payload.get("teams", []) or []

    ok = 0
    fail = 0

    for i, t in enumerate(teams, start=1):
        team_id = t["id"]
        market = t.get("market") or ""
        name = t.get("name") or ""
        slug = slugify_team(market, name)

        try:
            logging.info("[%02d/%02d] stats: %s %s", i, len(teams), market, name)
            payload = get_team_seasonal_statistics(SEASON_YEAR, SEASON_TYPE, team_id)

            out = OUT_DIR / f"{SEASON_YEAR}_{SEASON_TYPE}_{slug}.json"
            out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
            ok += 1
        except Exception as e:
            logging.exception("Failed %s %s (%s): %s", market, name, team_id, str(e))
            fail += 1

    logging.info("Done. OK=%s FAIL=%s", ok, fail)

if __name__ == "__main__":
    main()

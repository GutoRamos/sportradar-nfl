import json
import logging
import re
from pathlib import Path
from typing import Dict, Any, List

from sportradar_nfl.nfl_service import get_teams, get_team_roster

logging.basicConfig(level=logging.INFO)

RAW_DIR = Path("data/raw")
TEAMS_DIR = RAW_DIR / "teams"
RAW_DIR.mkdir(parents=True, exist_ok=True)
TEAMS_DIR.mkdir(parents=True, exist_ok=True)


def slugify_team(market: str, name: str) -> str:
    """
    Ex.: 'New England' + 'Patriots' -> 'new_england_patriots'
    """
    base = f"{market} {name}".strip().lower()
    base = re.sub(r"[^a-z0-9]+", "_", base)
    base = re.sub(r"_+", "_", base).strip("_")
    return base


def save_json(path: Path, payload: Any) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def main():
    logging.info("Fetching teams list...")
    teams_payload = get_teams()
    save_json(RAW_DIR / "teams.json", teams_payload)

    teams: List[Dict[str, Any]] = teams_payload.get("teams", []) or []
    logging.info("Found %s teams. Saving rosters to %s", len(teams), TEAMS_DIR.resolve())

    ok = 0
    fail = 0

    for i, t in enumerate(teams, start=1):
        team_id = t.get("id")
        market = t.get("market") or ""
        name = t.get("name") or ""

        if not team_id:
            logging.warning("Skipping team without id: %s", t)
            fail += 1
            continue

        slug = slugify_team(market, name)
        out_file = TEAMS_DIR / f"{slug}.json"

        try:
            logging.info("[%02d/%02d] Fetching roster: %s %s (%s)", i, len(teams), market, name, team_id)
            roster_payload = get_team_roster(team_id)
            save_json(out_file, roster_payload)
            ok += 1
        except Exception as e:
            logging.exception("Failed roster for %s %s (%s): %s", market, name, team_id, str(e))
            fail += 1

    logging.info("Done. OK=%s | FAIL=%s", ok, fail)


if __name__ == "__main__":
    main()

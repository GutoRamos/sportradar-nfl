import json
import logging
from pathlib import Path
import sys

from sportradar_nfl.nfl_service import (
    get_team_id_by_name,
    get_team_roster,
)

logging.basicConfig(level=logging.INFO)

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def slugify(text: str) -> str:
    return text.lower().replace(" ", "_")

def main():
    if len(sys.argv) < 2:
        print("Uso: python -m scripts.save_roster_payload \"New England Patriots\"")
        sys.exit(1)

    team_name = " ".join(sys.argv[1:])
    team_id = get_team_id_by_name(team_name)

    if not team_id:
        print(f"Time não encontrado: {team_name}")
        sys.exit(2)

    logging.info("Fetching roster for %s (team_id=%s)", team_name, team_id)
    payload = get_team_roster(team_id)

    filename = f"roster_{slugify(team_name)}.json"
    output_file = OUTPUT_DIR / filename

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    logging.info("Saved roster payload to %s", output_file.resolve())

if __name__ == "__main__":
    main()

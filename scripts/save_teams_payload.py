import json
import logging
from pathlib import Path

from sportradar_nfl.nfl_service import get_teams

logging.basicConfig(level=logging.INFO)

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    logging.info("Fetching teams from Sportradar API...")
    payload = get_teams()

    output_file = OUTPUT_DIR / "teams.json"
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    logging.info("Saved teams payload to %s", output_file.resolve())

if __name__ == "__main__":
    main()

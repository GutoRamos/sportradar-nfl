import json
import logging
import sys
from sportradar_nfl.nfl_service import get_team_id_by_name, get_team_roster

logging.basicConfig(level=logging.INFO)

def main():
    if len(sys.argv) < 2:
        print("Uso: python -m scripts.roster_by_team_name \"New England Patriots\"")
        sys.exit(1)

    team_name = " ".join(sys.argv[1:]).strip()
    team_id = get_team_id_by_name(team_name)

    if not team_id:
        print(f"Time não encontrado: {team_name}")
        sys.exit(2)

    profile = get_team_roster(team_id)
    players = profile.get("players", []) or []

    print(f"{profile.get('market')} {profile.get('name')} | team_id={team_id}")
    print(f"Roster size: {len(players)}")
    print(json.dumps(players[:15], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

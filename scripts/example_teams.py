import json
from sportradar_nfl.nfl_service import get_teams

if __name__ == "__main__":
    data = get_teams()
    teams = data.get("teams", [])
    print(f"Total teams: {len(teams)}")

    # imprime 5 times
    print(json.dumps(teams[:5], indent=2, ensure_ascii=False))

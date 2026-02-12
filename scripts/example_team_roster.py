import json
from sportradar_nfl.nfl_service import get_team_roster

TEAM_ID = "COLOQUE_AQUI_UM_TEAM_ID"  # pegue do retorno do example_teams.py

if __name__ == "__main__":
    profile = get_team_roster(TEAM_ID)

    players = profile.get("players", []) or []
    market = profile.get("market")
    name = profile.get("name")

    print(f"{market} {name}")
    print(f"Roster size: {len(players)}")

    # imprime 10 jogadores
    print(json.dumps(players[:10], indent=2, ensure_ascii=False))

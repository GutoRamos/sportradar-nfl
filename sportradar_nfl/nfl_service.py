from typing import Any, Dict, List, Optional
from .config import DEFAULT_HEADERS
from .http_client import get_json
from . import endpoints

def get_teams() -> Dict[str, Any]:
    """
    Retorna o payload do endpoint /league/teams
    """
    url = endpoints.league_teams()
    return get_json(url, headers=DEFAULT_HEADERS)

def get_team_roster(team_id: str) -> Dict[str, Any]:
    """
    Retorna o payload do endpoint /teams/{team_id}/profile
    O roster vem dentro de profile["players"].
    """
    url = endpoints.team_profile(team_id)
    return get_json(url, headers=DEFAULT_HEADERS)

def get_team_id_by_name(team_name: str) -> Optional[str]:
    """
    Resolve team_id pelo nome do time (case-insensitive), procurando por:
    - match exato em `name` (ex.: "Patriots")
    - match em "market name" (ex.: "New England Patriots")
    """
    data = get_teams()
    teams = data.get("teams", []) or []
    needle = team_name.strip().lower()

    # 1) exato em name
    for t in teams:
        name = (t.get("name") or "").strip().lower()
        if name == needle:
            return t.get("id")

    # 2) exato em "market name"
    for t in teams:
        market = (t.get("market") or "").strip()
        name = (t.get("name") or "").strip()
        full = f"{market} {name}".strip().lower()
        if full == needle:
            return t.get("id")

    # 3) contém
    for t in teams:
        market = (t.get("market") or "").strip()
        name = (t.get("name") or "").strip()
        full = f"{market} {name}".strip().lower()
        if needle in full:
            return t.get("id")

    return None

def get_team_seasonal_statistics(season_year: int, season_type: str, team_id: str) -> dict:
    url = endpoints.team_seasonal_statistics(season_year, season_type, team_id)
    return get_json(url, headers=DEFAULT_HEADERS)


def get_player_profile(player_id: str) -> dict:
    url = endpoints.player_profile(player_id)
    return get_json(url, headers=DEFAULT_HEADERS)


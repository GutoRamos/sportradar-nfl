from typing import Any, Dict, List, Optional
from src.config import DEFAULT_HEADERS
from src.http_client import get_json
from src import endpoints

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

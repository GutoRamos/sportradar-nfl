from src.config import config

def _root() -> str:
    # https://api.sportradar.com/nfl/official/{access_level}/v7/{lang}
    return f"{config.base_url}{config.product_root}/{config.access_level}/{config.version}/{config.lang}"

def _ext() -> str:
    return f".{config.fmt}"

def league_teams() -> str:
    # /league/teams.{format}
    return f"{_root()}/league/teams{_ext()}"

def team_profile(team_id: str) -> str:
    # /teams/{team_id}/profile.{format}
    # (Roster vem dentro do profile no campo players)
    return f"{_root()}/teams/{team_id}/profile{_ext()}"

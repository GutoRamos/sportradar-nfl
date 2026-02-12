# Sportradar NFL API Client

Cliente Python para consumir dados da API oficial da NFL via Sportradar.

## Funcionalidades

- Listar todos os times da NFL
- Obter roster (elenco) de qualquer time
- Buscar time por nome (case-insensitive)
- Obter estatisticas sazonais dos times
- Obter perfil de jogadores

## Estrutura do Projeto

```
sportradar-nfl/
├── sportradar_nfl/          # Pacote principal
│   ├── config.py            # Configuracoes e variaveis de ambiente
│   ├── endpoints.py         # URLs dos endpoints da API
│   ├── http_client.py       # Cliente HTTP com retry e rate limiting
│   └── nfl_service.py       # Servicos de alto nivel para a API
├── scripts/                 # Scripts utilitarios
│   ├── example_teams.py     # Exemplo: listar times
│   ├── example_team_roster.py   # Exemplo: obter roster
│   ├── roster_by_team_name.py   # Buscar roster por nome do time
│   ├── save_teams_payload.py    # Salvar dados de todos os times
│   ├── save_all_team_rosters.py # Salvar rosters de todos os times
│   └── save_all_teams_season_stats.py  # Salvar estatisticas da temporada
├── data/                    # Dados salvos em JSON
│   └── raw/
│       ├── teams/           # Rosters dos 32 times
│       ├── season_stats/    # Estatisticas por temporada
│       └── teams.json       # Lista de todos os times
└── .env                     # Variaveis de ambiente (nao commitado)
```

## Instalacao

1. Clone o repositorio:
```bash
git clone https://github.com/GutoRamos/sportradar-nfl.git
cd sportradar-nfl
```

2. Crie um ambiente virtual e instale as dependencias:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Configure as variaveis de ambiente criando um arquivo `.env`:
```env
SPORTRADAR_API_KEY=sua_api_key_aqui
SPORTRADAR_ACCESS_LEVEL=trial
SPORTRADAR_LANG=en
SPORTRADAR_FORMAT=json
SPORTRADAR_VERSION=v7
SPORTRADAR_BASE_URL=https://api.sportradar.com
```

## Uso

### Listar times
```python
from sportradar_nfl.nfl_service import get_teams

teams = get_teams()
for team in teams.get("teams", []):
    print(f"{team['market']} {team['name']}")
```

### Obter roster de um time
```python
from sportradar_nfl.nfl_service import get_team_roster, get_team_id_by_name

team_id = get_team_id_by_name("Kansas City Chiefs")
roster = get_team_roster(team_id)

for player in roster.get("players", []):
    print(f"{player['name']} - {player['position']}")
```

### Obter estatisticas da temporada
```python
from sportradar_nfl.nfl_service import get_team_seasonal_statistics

stats = get_team_seasonal_statistics(2024, "REG", team_id)
```

## Dados Incluidos

O repositorio inclui dados pre-coletados da temporada 2024:
- Rosters completos dos 32 times da NFL
- Estatisticas da temporada regular 2024

## API Reference

A API do Sportradar requer uma chave de acesso. Obtenha a sua em:
https://developer.sportradar.com/

## Fotos dos Jogadores

Para obter fotos dos jogadores, use a URL do ESPN:
```
https://a.espncdn.com/i/headshots/nfl/players/full/{playerId}.png
```

Exemplo (Nick Chubb): https://a.espncdn.com/i/headshots/nfl/players/full/3128720.png

## Licenca

MIT

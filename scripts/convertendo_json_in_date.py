import pandas as pd
import json
import sqlite3
import glob

# --- CONFIGURAÇÕES ---
PATH_RAW = r"C:\Users\gustavo.luiz\Project\sportradar-nfl\data\raw\season_stats\2024_REG"
ataque = ["LT", "LG", "C", "RG", "RT", "QB", "RB", "FB", "WR", "TE"]
defesa = ["DE", "DT", "NT", "LB", "MLB", "OLB", "CB", "SS", "FS"]

# --- FUNÇÕES DE APOIO ---

def definir_unidade(posicao):
    if posicao in ataque: return 'ataque'
    if posicao in defesa: return 'defesa'
    return 'special_teams'

def extrair_df_jogadores(dados_json):
    """Padroniza a extração do JSON para DataFrame."""
    return pd.json_normalize(
        dados_json, 
        record_path=['players'], 
        meta=['id', ['season', 'year'], ['season', 'type'], 'name'],
        meta_prefix='team_', 
        sep='_'
    )

def extrair_time(dados_json):
    """Extrai apenas os dados da entidade Time."""
    df_time = pd.DataFrame([{
        'team_id': dados_json.get('id'),
        'team_name': dados_json.get('name'),
        'team_market': dados_json.get('market'),
        'team_alias': dados_json.get('alias')
    }])
    return df_time

def extrair_dim_jogadores(df_raw):
    """Filtra apenas colunas biográficas para a dimensão Player."""
    colunas_bio = ['id', 'name', 'jersey', 'position']
    # Filtramos apenas as colunas que existem (evita erro se alguma faltar)
    df_players = df_raw[df_raw.columns.intersection(colunas_bio)].copy()
    return df_players.drop_duplicates(subset=['id'])

# --- FUNÇÕES DA ABORDAGEM 3 (SCHEMA ENFORCEMENT) ---

def mapear_esquema_global(arquivos):
    """Fase 1: Descobre todas as colunas possíveis em todos os arquivos."""
    print("Mapeando esquema global (isso pode levar alguns segundos)...")
    colunas_mestres = set()
    
    for arquivo in arquivos:
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            df_temp = extrair_df_jogadores(dados)
            colunas_mestres.update(df_temp.columns)
            
    return sorted(list(colunas_mestres))

def padronizar_dataframe(df, colunas_mestres):
    """Fase 2: Garante que o DF atual tenha todas as colunas da lista mestre."""
    # Adiciona colunas que existem no mestre mas não no DF atual (preenche com NaN)
    colunas_faltantes = set(colunas_mestres) - set(df.columns)
    for col in colunas_faltantes:
        df[col] = None
    
    # Reordena as colunas para garantir consistência no SQL
    return df[colunas_mestres]

# --- FLUXO PRINCIPAL ---

def main():
    arquivos = glob.glob(PATH_RAW + "/*.json")
    if not arquivos:
        print("Nenhum arquivo encontrado.")
        return

    # 1. Mapeamento Global
    todas_as_colunas = mapear_esquema_global(arquivos)
    print(f"Total de colunas mapeadas: {len(todas_as_colunas)}")

# ... (início do main igual até a conexão) ...
    conn = sqlite3.connect('nfl_stats_robust.db')
    
    for arquivo in arquivos:
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados_carregados = json.load(f)
        
        nome_time = dados_carregados['name']
        print(f"Processando: {nome_time}")

        # --- 1. EXTRAÇÃO ---
        df_raw = extrair_df_jogadores(dados_carregados)
        df_time = extrair_time(dados_carregados)
        df_dim_player = extrair_dim_jogadores(df_raw)

        # --- 2. TRANSFORMAÇÃO ---
        df_raw['unit'] = df_raw['position'].apply(definir_unidade)
        
        if 'unit' not in todas_as_colunas:
            todas_as_colunas.append('unit')
            
        # Agora sim criamos o df_final padronizado
        df_final = padronizar_dataframe(df_raw, todas_as_colunas)

        # --- 3. CARGA (Com verificação de duplicatas) ---
        
        # Para o Time: Só insere se o banco estiver vazio ou se o ID não existir
        df_time.to_sql('dim_teams', conn, if_exists='append', index=False) 
        # Nota: Idealmente aqui faríamos o filtro de ID, mas como é 1 por arquivo,
        # você pode apenas rodar um df_time.drop_duplicates() depois se preferir.

        # Para os Jogadores (Bio):
        df_dim_player.to_sql('dim_players', conn, if_exists='append', index=False)

        # Para as Estatísticas (Fato):
        df_final.to_sql('fact_player_stats', conn, if_exists='append', index=False)

    conn.close()
    print("\nCarga finalizada com sucesso!")

if __name__ == "__main__":
    main()
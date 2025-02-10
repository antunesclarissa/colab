import pandas as pd
import os
import re
from openpyxl import load_workbook  # Para leitura de Excel com openpyxl

# =============================================================================
# Função: extrair_nome_coluna
# =============================================================================
def extrair_nome_coluna(nome_coluna):
    """
    Extrai a parte do nome da coluna antes do delimitador " : ".
    
    Exemplo:
        "NOME : INFO EXTRA" -> "NOME"
    """
    return nome_coluna.split(" : ")[0]

# =============================================================================
# Função: renomear_colunas
# =============================================================================
def renomear_colunas(nome_coluna):
    """
    Renomeia o nome da coluna com base em padrões pré-definidos.
    
    Aplica expressões regulares para identificar:
      - Padrões de perguntas (ex.: P2, P2a, P2b, P3a, P3b, P4B), gerando:
            CAT{categoria}_{pergunta}_M{marca} ou CAT{categoria}_{pergunta}
      - Padrões de atributos (ex.: P2Ca, P2Cb), gerando:
            CAT{categoria}_{pergunta}_AT{atributo}_M{marca} (com ajuste para P2Cb)
    """
    nome_coluna_limpo = extrair_nome_coluna(nome_coluna)
    
    padrao_pergunta = re.compile(r'(P2|P2[ab]|P3[ab]|P4B)_(\d+)(?:_(\d+))?', re.IGNORECASE)
    padrao_atributo = re.compile(r'(P2Ca|P2Cb)_(\d+)_(\d+)_(\d+)', re.IGNORECASE)

    match_pergunta = padrao_pergunta.match(nome_coluna_limpo)
    if match_pergunta:
        pergunta, primeiro_numero, segundo_numero = match_pergunta.groups()
        if segundo_numero:
            categoria = segundo_numero
            marca = primeiro_numero
            novo_nome = f'CAT{categoria}_{pergunta}_M{marca}'
        else:
            categoria = primeiro_numero
            novo_nome = f'CAT{categoria}_{pergunta}'
        return novo_nome

    match_atributo = padrao_atributo.match(nome_coluna)
    if match_atributo:
        pergunta, atributo, marca, categoria = match_atributo.groups()
        atributo = int(atributo)
        if 'P2Cb' in pergunta:
            atributo += 12
        novo_nome = f'CAT{categoria}_{pergunta}_AT{atributo}_M{marca}'
        return novo_nome

    return nome_coluna

# =============================================================================
# Função: remover_linhas_colunas_vazias
# =============================================================================
def remover_linhas_colunas_vazias(df):
    """
    Substitui strings vazias por NA e remove linhas e colunas inteiramente vazias.
    """
    # Considera células com espaços ou strings vazias como NA
    df.replace(r'^\s*$', pd.NA, regex=True, inplace=True)
    df = df.dropna(how='all')         # Remove linhas completamente vazias
    df = df.dropna(axis=1, how='all')    # Remove colunas completamente vazias
    return df

# =============================================================================
# Função: converter_para_categorias
# =============================================================================
def converter_para_categorias(df):
    """
    Converte colunas para 'category' se a proporção de valores únicos for inferior a 50%.
    """
    for col in df.columns:
        if df[col].dtype == 'object':
            num_unique = df[col].nunique()
            num_total = len(df[col])
            if num_unique / num_total < 0.5:
                df[col] = df[col].astype('category')
    return df

# =============================================================================
# Função: processar_arquivo_excel
# =============================================================================
def processar_arquivo_excel(caminho_entrada, caminho_saida):
    """
    Processa um arquivo Excel:
      - Lê o arquivo utilizando openpyxl;
      - Remove as duas primeiras colunas;
      - Conta e remove linhas e colunas completamente vazias;
      - Renomeia as colunas conforme os padrões definidos;
      - Converte colunas para 'category' quando aplicável;
      - Salva o DataFrame processado em um novo arquivo Excel.
    """
    # Leitura do arquivo Excel
    df = pd.read_excel(caminho_entrada, engine='openpyxl')
    
    # Remove as duas primeiras colunas
    df = df.iloc[:, 2:]
    print(f"Dimensões do DataFrame após remover as duas primeiras colunas: {df.shape}")
    
    # Conta linhas vazias antes da remoção
    linhas_vazias = df.isna().all(axis=1).sum()
    print(f"Número de linhas completamente vazias (antes da remoção): {linhas_vazias}")
    
    # Remove linhas e colunas completamente vazias
    df = remover_linhas_colunas_vazias(df)
    print(f"Dimensões do DataFrame após remoção de linhas e colunas vazias: {df.shape}")
    
    # Renomeia as colunas utilizando os padrões definidos
    colunas_renomeadas = [renomear_colunas(coluna) for coluna in df.columns]
    mapeamento = dict(zip(df.columns, colunas_renomeadas))
    df = df.rename(columns=mapeamento)
    
    # Converte colunas para 'category' quando aplicável
    df = converter_para_categorias(df)
    
    # Salva o DataFrame processado em um novo arquivo Excel
    df.to_excel(caminho_saida, index=False)
    print(f"Arquivo processado e salvo como: {caminho_saida}")
    
    return df

# =============================================================================
# Execução do Processamento para o Arquivo Único: /mnt/data/NLS2023_Bancos_Tradicionais.xlsx
# =============================================================================

# Defina o diretório onde o arquivo está localizado
caminho_pasta = "/mnt/data/"

# Nome do arquivo de entrada
arquivo_entrada = "/mnt/data/NLS2023_Bancos_Tradicionais.xlsx"
caminho_entrada = os.path.join(caminho_pasta, arquivo_entrada)

# Nome do arquivo de saída
arquivo_saida = "NLS2023_Bancos_Tradicionais_tratado.xlsx"
caminho_saida = os.path.join(caminho_pasta, arquivo_saida)

# Processa o arquivo Excel
df_processado = processar_arquivo_excel(caminho_entrada, caminho_saida)
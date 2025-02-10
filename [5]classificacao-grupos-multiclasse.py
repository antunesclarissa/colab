import pandas as pd
import numpy as np
import re

# Função para classificar em grupos multiclasse
def classificar_grupo(nota):
    if pd.isna(nota):
        return np.nan
    elif nota >= 9:
        return 1  # Grupo G1
    elif nota >= 7:
        return 2  # Grupo G2
    elif nota >= 5:
        return 3  # Grupo G3
    else:
        return 4  # Grupo G4

# Caminho do arquivo
caminho_arquivo = '/content/NLS/Categorias_Amor_AT_NaN.xlsx'

# Ler o arquivo excel
df = pd.read_excel(caminho_arquivo)

# Identificar categorias
categorias = set(col.split('_')[0] for col in df.columns if 'P2a' in col)

# Processar cada categoria
for categoria in categorias:
    # Filtrar colunas da categoria
    colunas_categoria = df.filter(regex=f'{categoria}_P2a.*').columns

    # Classificar respostas e criar colunas de grupo
    df_categoria = df[colunas_categoria].map(classificar_grupo)
    for grupo in range(1, 5):
        df[f'{categoria}_G{grupo}'] = (df_categoria == grupo).any(axis=1).astype(int)

    # Remover colunas originais da categoria
    df.drop(colunas_categoria, axis=1, inplace=True)

# Salvar o DataFrame processado
df.to_excel('/content/NLS/Categorias_Amor_AT_grupos.xlsx', index=False)
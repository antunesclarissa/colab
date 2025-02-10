import pandas as pd
import numpy as np
import re

# Carregar o DataFrame
df = pd.read_excel('/content/NLS/Categorias_Amor_AT_sem_linhas.xlsx')

# Definir um tamanho de lote (número de colunas a processar por vez)
tamanho_lote = 500

# Expressões regulares para identificar as colunas de variáveis dependentes e independentes
regex_var_dep = re.compile('.*P2a.*')
regex_var_indep = re.compile('.*P2Ca.*|.*P2Cb.*')

# Tratar valores ausentes em lotes
for i in range(0, len(df.columns), tamanho_lote):
    colunas_lote = df.columns[i:i + tamanho_lote]
    for coluna in colunas_lote:
        if regex_var_dep.search(coluna):
            df[coluna] = df[coluna].fillna(np.nan)
        elif regex_var_indep.search(coluna):
            df[coluna] = df[coluna].fillna(0)

# Salvar o DataFrame tratado
df.to_excel('/content/NLS/Categorias_Amor_AT_NaN.xlsx', index=False)
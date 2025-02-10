import pandas as pd

# Caminho do arquivo
caminho_arquivo = '/content/NLS/Categorias_Amor_AT_grupos.xlsx'

# Ler o arquivo excel
df = pd.read_excel(caminho_arquivo)

# Verificar se existem colunas com 'P2a'
colunas_p2a = [col for col in df.columns if 'P2a' in col]

# Imprimir se colunas com 'P2a' existem
if not colunas_p2a:
    print("Todas as colunas contendo 'P2a' foram removidas.")
else:
    print("Ainda existem colunas contendo 'P2a':")
    print(colunas_p2a)
    
# Verificar se existem colunas com 'P4B'
colunas_p4b = [col for col in df.columns if 'P4B' in col]

# Imprimir se colunas com 'P4B' existem
if not colunas_p4b:
    print("Todas as colunas contendo 'P4B' foram removidas.")
else:
    print("Ainda existem colunas contendo 'P4B':")
    print(colunas_p4b)

# Verificar e imprimir o tamanho do DataFrame
print(f"Dimensões do DataFrame: {df.shape} (Linhas, Colunas)")
import pandas as pd

def processar_e_salvar_arquivo(caminho_arquivo_entrada, caminho_arquivo_saida):
    # Ler o arquivo excel
    df = pd.read_excel(caminho_arquivo_entrada)

    # Imprimir o tamanho do DataFrame antes da remoção
    print(f'Tamanho do DataFrame antes da remoção: {df.shape} (Linhas, Colunas)')

    # Contar o número de linhas vazias
    linhas_vazias = df.isna().all(axis=1).sum()

    # Imprimir o resultado da verificação
    if linhas_vazias == 0:
        print("Não existem linhas completamente vazias no arquivo.")
    else:
        print(f"Existem {linhas_vazias} linhas completamente vazias no arquivo.")

    # Remover linhas que são completamente vazias
    df_limpo = df.dropna(how='all')

    # Imprimir o tamanho do DataFrame após a remoção
    print(f'Tamanho do DataFrame após a remoção: {df_limpo.shape} (Linhas, Colunas)')

    # Salvar o DataFrame limpo em um novo arquivo excel
    df_limpo.to_excel(caminho_arquivo_saida, index=False)
    print(f'Arquivo salvo após remover linhas vazias: {caminho_arquivo_saida}')

# Caminho do arquivo original
caminho_arquivo_entrada = "/mnt/data/Categorias_Amor_AT.xlsx"

# Caminho para salvar o arquivo após a remoção das linhas vazias
caminho_arquivo_saida = "/mnt/data/Categorias_Amor_AT_sem_linhas.xlsx"

# Executar a função
processar_e_salvar_arquivo(caminho_arquivo_entrada, caminho_arquivo_saida)
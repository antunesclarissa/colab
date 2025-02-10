import pandas as pd
import os
import re

# =============================================================================
# FUNÇÃO: dividir_e_salvar_arquivo
# =============================================================================
def dividir_e_salvar_arquivo(nome_arquivo_original, caminho_saida, regex_arquivo_1, regex_arquivo_2):
    """
    Lê um arquivo Excel processado (já tratado), filtra as colunas que correspondem a dois
    conjuntos distintos (baseados em expressões regulares) e salva cada conjunto em um arquivo Excel separado.
    
    Exemplo: separar atributos de "amor" e "NPS":
      - regex_arquivo_1: Filtra colunas para atributos de "amor" (por exemplo, contendo "P2a", "P2Ca" ou "P2Cb").
      - regex_arquivo_2: Filtra colunas para atributos de "NPS" (por exemplo, contendo "P4B", além de "P2Ca" e "P2Cb" se necessário).
    
    Parâmetros:
      nome_arquivo_original (str): Caminho do arquivo Excel já tratado.
      caminho_saida (str): Diretório onde os novos arquivos serão salvos.
      regex_arquivo_1 (regex): Expressão regular para filtrar colunas do grupo "amor".
      regex_arquivo_2 (regex): Expressão regular para filtrar colunas do grupo "NPS".
    """
    # Ler o arquivo Excel tratado
    df = pd.read_excel(nome_arquivo_original)
    
    # Filtrar as colunas para cada grupo com base nas expressões regulares
    colunas_arquivo_1 = [col for col in df.columns if regex_arquivo_1.search(col)]
    colunas_arquivo_2 = [col for col in df.columns if regex_arquivo_2.search(col)]
    
    # Exibir contagens para validação
    print(f"Número de colunas selecionadas para 'Amor': {len(colunas_arquivo_1)}")
    print(f"Número de colunas selecionadas para 'NPS': {len(colunas_arquivo_2)}")
    
    # Criar DataFrames para cada grupo de colunas
    df_arquivo_1 = df[colunas_arquivo_1]
    df_arquivo_2 = df[colunas_arquivo_2]
    
    # Definir os caminhos de saída completos
    caminho_saida_1 = os.path.join(caminho_saida, "Categorias_Amor_AT.xlsx")
    caminho_saida_2 = os.path.join(caminho_saida, "Categorias_NPS_AT.xlsx")
    
    # Salvar os DataFrames em arquivos Excel separados
    df_arquivo_1.to_excel(caminho_saida_1, index=False)
    df_arquivo_2.to_excel(caminho_saida_2, index=False)
    
    print(f"Arquivo 'Amor' salvo em: {caminho_saida_1}")
    print(f"Arquivo 'NPS' salvo em: {caminho_saida_2}")

# =============================================================================
# EXECUÇÃO DO SCRIPT DE DIVISÃO
# =============================================================================

# Arquivo já tratado (gerado no Script 1)
nome_arquivo_original = "/mnt/data/NLS2023_Bancos_Tradicionais_tratado.xlsx"

# Diretório de saída (no Google Colab, normalmente "/mnt/data/")
caminho_saida = "/mnt/data/NLS"

# Compilar as expressões regulares para filtrar as colunas desejadas
regex_arquivo_1 = re.compile(r'.*P2a.*|.*P2Ca.*|.*P2Cb.*')  # Grupo de "amor"
regex_arquivo_2 = re.compile(r'.*P4B.*|.*P2Ca.*|.*P2Cb.*')   # Grupo de "NPS"

# Executa a função para dividir e salvar os grupos
dividir_e_salvar_arquivo(nome_arquivo_original, caminho_saida, regex_arquivo_1, regex_arquivo_2)
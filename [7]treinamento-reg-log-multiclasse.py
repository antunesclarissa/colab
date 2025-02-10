import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import classification_report
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

# =============================================================================
# ETAPA 1: LEITURA DOS DADOS PROCESSADOS
# =============================================================================
# Carrega o DataFrame processado contendo os grupos de "amor"
# O arquivo deve conter as colunas, por exemplo, "CAT7_G1", "CAT7_G2", "CAT7_G3" e "CAT7_G4"
df = pd.read_excel('/content/NLS/Categorias_Amor_AT_grupos.xlsx')
print("Arquivo carregado.")

# =============================================================================
# ETAPA 2: DEFINIÇÃO DAS VARIÁVEIS INDEPENDENTES (X)
# =============================================================================
# Seleciona as colunas que representam os atributos independentes (variáveis preditoras)
# Neste caso, as colunas que contêm "P2Ca" ou "P2Cb"
X = df.filter(regex='P2Ca|P2Cb')
print(f"Variáveis independentes selecionadas: {X.shape}")

# =============================================================================
# ETAPA 3: TREINAMENTO DOS MODELOS DE REGRESSÃO LOGÍSTICA PARA A CATEGORIA 7
# =============================================================================
# Como estamos lidando com uma única categoria (7), definimos:
categoria = 7
resultados = {categoria: {}}

for grupo in ['G1', 'G2', 'G3', 'G4']:
    nome_coluna_grupo = f'CAT{categoria}_{grupo}'
    if nome_coluna_grupo in df.columns:
        y = df[nome_coluna_grupo]
        print(f"\nTreinando modelo para {nome_coluna_grupo}...")
        
        # Dividir os dados em conjuntos de treino e teste com amostragem estratificada
        X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                            test_size=0.3, 
                                                            random_state=42, 
                                                            stratify=y)
        # Treinar modelo de regressão logística com validação cruzada (5 folds)
        modelo = LogisticRegressionCV(cv=5, penalty='l2', max_iter=1000, random_state=42).fit(X_train, y_train)
        
        # Avaliar modelo
        y_pred = modelo.predict(X_test)
        report = classification_report(y_test, y_pred, zero_division=1, output_dict=True)
        
        # Armazenar os resultados
        resultados[categoria][grupo] = {
            'modelo': modelo,
            'report': report
        }
    else:
        print(f"A coluna {nome_coluna_grupo} não foi encontrada no DataFrame.")

# =============================================================================
# ETAPA 4: CONSOLIDAÇÃO DOS RELATÓRIOS DE CLASSIFICAÇÃO E SALVAMENTO
# =============================================================================
relatorios_df = []  # Inicializa uma lista
for cat, dados_categoria in resultados.items():
    for grupo, dados_grupo in dados_categoria.items():
        # Extrai o relatório completo
        report_completo = dados_grupo['report']
        # Extrai o valor global de acurácia
        overall_accuracy = report_completo.get('accuracy', None)
        # Extrai o dicionário 'weighted avg'
        weighted_avg = report_completo.get('weighted avg', {})
        # Adiciona o valor de acurácia ao dicionário de weighted avg
        weighted_avg['accuracy'] = overall_accuracy
        # Cria um DataFrame temporário e adiciona informações de categoria e grupo
        report_df = pd.DataFrame([weighted_avg])
        report_df['categoria'] = cat
        report_df['grupo'] = grupo
        relatorios_df.append(report_df)

# Concatenar a lista de DataFrames em um único DataFrame
relatorios_df = pd.concat(relatorios_df, ignore_index=True)

# Salvar os relatórios em um arquivo Excel
relatorios_df.to_excel('/content/NLS/Amor_regressao_relatorios_class.xlsx', index=False)
print("Relatórios de classificação salvos em: /content/NLS/Amor_regressao_relatorios_class.xlsx")

# =============================================================================
# ETAPA 5: PLOTAGEM DAS MÉTRICAS
# =============================================================================
sns.set(style="whitegrid")
fig, axes = plt.subplots(nrows=len(resultados), ncols=1, figsize=(10, 5 * len(resultados)))
if not isinstance(axes, np.ndarray):
    axes = np.array([axes])
for i, (cat, grupos) in enumerate(resultados.items()):
    # Coleta a acurácia para cada grupo da categoria
    precisoes = [grupo_info['report']['accuracy'] for grupo_info in grupos.values()]
    sns.barplot(ax=axes[i], x=list(grupos.keys()), y=precisoes)
    axes[i].set_title(f'Precisão dos Grupos para a Categoria {cat}')
    axes[i].set_ylabel('Precisão')
    axes[i].set_xlabel('Grupo')
plt.tight_layout()
plt.show()

# =============================================================================
# ETAPA 6: GERAÇÃO DE EXPLICAÇÕES TEXTUAIS DOS RESULTADOS
# =============================================================================
def gerar_explicacao(report):
    """
    Gera uma explicação textual para um relatório de classificação.
    """
    # Utiliza .get() para evitar KeyError caso alguma métrica não esteja presente
    return (
        f"Acurácia: {report.get('accuracy', 0):.2f}\n"
        f"Precisão: {report.get('precision', 0):.2f}\n"
        f"Recall: {report.get('recall', 0):.2f}\n"
        f"F1-score: {report.get('f1-score', 0):.2f}\n"
    )

print("\nResumo dos Resultados para Categoria 7:")
for grupo in ['G1', 'G2', 'G3', 'G4']:
    if grupo in resultados[categoria]:
        report = resultados[categoria][grupo]['report']['weighted avg']
        explicacao = gerar_explicacao(report)
        print(f"\nResultados para Categoria {categoria} - Grupo {grupo}:\n{explicacao}")
    else:
        print(f"\nRelatório para Categoria {categoria} - Grupo {grupo} não encontrado.")
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys

sns.set()

def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).unstack().plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    return None

def gerar_graficos_para_mes(df, mes):
    max_data = df.DTNASC.max()[:7]
    
    os.makedirs(f'./output/figs/{max_data}', exist_ok=True)

    plota_pivot_table(df_mes, 'IDADEMAE', 'DTNASC', 'mean', 'Média Idade Mãe por Data', 'Data de Nascimento')
    plt.savefig(f'./output/figs/{max_data}/media_idade_mae_por_data_{mes}.png')
    plt.title(f'Media de idade das mae por data_{mes}')
    plt.show()

    plota_pivot_table(df_mes, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'Média Idade Mãe', 'Data de Nascimento', 'unstack')
    plt.savefig(f'./output/figs/{max_data}/media_idade_mae_por_sexo_{mes}.png')
    plt.title(f'Media de idade das mae por sexo_{mes}')
    plt.show()

    plota_pivot_table(df_mes, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'Média Peso Bebê', 'Data de Nascimento', 'unstack')
    plt.savefig(f'./output/figs/{max_data}/media_peso_bebe_por_sexo_{mes}.png')
    plt.title(f'Media do peso do bebe por data_{mes}')
    plt.show()

    plota_pivot_table(df_mes, 'PESO', 'ESCMAE', 'median', 'Peso Mediano', 'Escolaridade Mãe', 'sort')
    plt.savefig(f'./output/figs/{max_data}/peso_mediano_por_escolaridade_mae_{mes}.png')
    plt.title(f'Peso mediano por escolaridade mae_{mes}')
    plt.show()

    plota_pivot_table(df_mes, 'APGAR1', 'GESTACAO', 'mean', 'Apgar1 Médio', 'Gestação', 'sort')
    plt.savefig(f'./output/figs/{max_data}/media_apgar1_por_gestacao_{mes}.png')
    plt.title(f'Media de apgar1 por gestacao_{mes}')
    plt.show()


mes_entrada = sys.argv
print(mes_entrada)

# Dicionário para armazenar os DataFrames
dicionario_df = {}

# Iteração sobre a lista de meses
for i in range(1,len(mes_entrada)):
    # Substituir 'mes' no nome do arquivo pelo mês atual
    nome_arquivo = f'D:\\EBAC\\Unid14\\Aula6\\SINASC_RO_2019_{mes_entrada[i]}.csv'
    
    # Leitura do arquivo específico do mês
    df_mes = pd.read_csv(nome_arquivo)
    for mes in mes_entrada[1:]:
        # Armazenar o DataFrame no dicionário
        dicionario_df[mes] = df_mes

# Acessar os DataFrames a partir do dicionário
for mes, df in dicionario_df.items():
    gerar_graficos_para_mes(df, mes)
    
    
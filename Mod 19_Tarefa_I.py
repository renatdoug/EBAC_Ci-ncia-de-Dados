import pandas as pd
import streamlit as st
import seaborn as sns
import timeit
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import tracemalloc

# Custom functions
tracemalloc.start()

# Configuração de estilo do Seaborn
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)

# Função para ler o dataframe


@st.cache_data
def load_data(file_data):
    try:
        if file_data.name.endswith('.csv'):
            # Se o arquivo tiver extensão CSV, use pd.read_csv
            return pd.read_csv(file_data, sep=';')
        elif file_data.name.endswith(('.xlsx', '.xls')):
            # Se o arquivo tiver extensão XLSX ou XLS, use pd.read_excel
            return pd.read_excel(file_data)
        else:
            # Se o tipo de arquivo não for suportado, mostre um erro
            st.error("Formato de arquivo não suportado. Use arquivos CSV ou Excel.")
            return None
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return None


# Função para filtrar as colunas


@st.cache_data
def multiselect_filter(data, col, selected):
    if 'all' in selected:
        return data
    else:
        return data[data[col].isin(selected)].reset_index(drop=True)


@st.cache_data
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

# Função principal


def main():
    # Configuração inicial da página da aplicação
    st.set_page_config(page_title="Telemarketing analysis",
                       page_icon="negocio.jpg", layout='wide', initial_sidebar_state='expanded')

    # Título principal da aplicação
    st.write('# Telemarketing analysis')
    st.markdown("-----")

    #start = timeit.default_timer()

    # Apresenta a imagem na barra lateral da aplicação
    image = Image.open('bank.jpeg')
    st.sidebar.image(image)

    # Botão para carregar arquivo na aplicação
    st.sidebar.write("## Suba o arquivo")
    data_file_1 = st.sidebar.file_uploader(
        "Bank marketing data", type=["xlsx", "csv"])

    # Verifica se o arquivo foi carregado
    if data_file_1 is not None:
        # Início da medição do tempo
        #start = timeit.default_timer()

        # Carrega os dados brutos
        bank_raw = load_data(data_file_1)

        # Verifica se os dados foram carregados com sucesso
        if bank_raw is not None:
            # Exibe o tempo de carregamento
            #st.write('Time: ', timeit.default_timer() - start)

            # Cria uma cópia do dataframe original
            bank = bank_raw.copy()

            # Exibe os dados brutos antes dos filtros
            st.write('## Antes dos filtros')
            st.write(bank_raw.head())

            # Inicia o formulário para aplicar filtros
            with st.sidebar.form(key='my_form'):
                # SELECIONA O TIPO DE GRÁFICO
                graph_type = st.radio('Tipo de gráfico: ',  ['Pizza', 'Bar'])

                # IDADES
                min_age = int(bank.age.min())
                max_age = int(bank.age.max())
                idades = st.slider(label='Idade',
                                   min_value=min_age,
                                   max_value=max_age,
                                   value=(min_age, max_age),
                                   step=1)

                # PROFISSÕES
                jobs_list = bank.job.unique().tolist()
                jobs_list.append('all')
                jobs_selected = st.multiselect(
                    'Profissão', sorted(jobs_list), ['all'])

                # ESTADO CIVIL
                marital_list = bank.marital.unique().tolist()
                marital_list.append('all')
                marital_selected = st.multiselect(
                    'Estado civil', marital_list, ['all'])

                # DEFAULT
                default_list = bank.default.unique().tolist()
                default_list.append('all')
                default_selected = st.multiselect(
                    'Default', default_list, ['all'])

                # TEM EMPRESTIMO?
                housing_list = bank.housing.unique().tolist()
                housing_list.append('all')
                housing_selected = st.multiselect(
                    'Tem financiamento imob?', housing_list, ['all'])

                # TEM FINANCIAMENTO IMOBILIÁRIO?
                loan_list = bank.loan.unique().tolist()
                loan_list.append('all')
                loan_selected = st.multiselect(
                    'Tem empréstimo?', loan_list, ['all'])

                # MEIO DE CONTATO?
                contact_list = bank.contact.unique().tolist()
                contact_list.append('all')
                contact_selected = st.multiselect(
                    'Meio de contato', contact_list, ['all'])

                # MÊS DE CONTATO?
                month_list = bank.month.unique().tolist()
                month_list.append('all')
                month_selected = st.multiselect(
                    'Mês de contato', month_list, ['all'])

                # DIA DA SEMANA
                day_of_week_list = bank.day_of_week.unique().tolist()
                day_of_week_list.append('all')
                day_of_week_selected = st.multiselect(
                    'Dia da semana', day_of_week_list, ['all'])

                # Botão de submit para aplicar os filtros
                submit_button = st.form_submit_button(label='Aplicar')

                # Aplica os filtros ao dataframe no momento do clique no botão
                if submit_button:
                    bank = (bank.query("age >= @idades[0] and age <= @idades[1]")
                            .pipe(multiselect_filter, 'job', jobs_selected)
                            .pipe(multiselect_filter, 'marital', marital_selected)
                            .pipe(multiselect_filter, 'default', default_selected)
                            .pipe(multiselect_filter, 'housing', housing_selected)
                            .pipe(multiselect_filter, 'loan', loan_selected)
                            .pipe(multiselect_filter, 'contact', contact_selected)
                            .pipe(multiselect_filter, 'month', month_selected)
                            .pipe(multiselect_filter, 'day_of_week', day_of_week_selected)
                            )

        else:
            # Mensagem de aviso em caso de erro no carregamento dos dados
            st.write("Erro ao carregar os dados. Verifique o formato do arquivo.")
    else:
        # Mensagem de aviso para carregar um arquivo antes de continuar
        st.write("Carregue um arquivo antes de continuar.")

    # Verifica se o dataframe 'bank' está definido antes de acessá-lo
    if 'bank' in locals():
        # Exibe os dados após os filtros
        st.write('## Após os filtros')
        st.write(bank.head())
        st.markdown("-----")

        # PLOTS
        fig, ax = plt.subplots(1, 2, figsize=(12, 5))

        bank_raw_target_perc = bank_raw['y'].value_counts(
            normalize=True).to_frame()*100
        bank_raw_target_perc = bank_raw_target_perc.sort_index()

        try:
            bank_target_perc = bank['y'].value_counts(
                normalize=True).to_frame()*100
            bank_target_perc = bank_target_perc.sort_index()
        except:
            st.error("Erro no filtro")

        # Botões de download dos dados dos gráficos
        col1, col2 = st.columns(2)

        df_xlsx = to_excel(bank_raw_target_perc)
        col1.write('### Proporção original')
        col1.write(bank_raw_target_perc)
        col1.download_button(label='📥 Download',
                             data=df_xlsx,
                             file_name='bank_raw_y.xlsx')

        df_xlsx = to_excel(bank_target_perc)
        col2.write('### Proporção da tabela com filtros')
        col2.write(bank_target_perc)
        col2.download_button(label='📥 Download',
                             data=df_xlsx,
                             file_name='bank_y.xlsx')
        st.markdown('---')

        st.write('## Proporção de aceite')

        # PLOTS
        if graph_type == 'Bar':
            sns.barplot(x=bank_raw_target_perc.index,
                        y='y',
                        data=bank_raw_target_perc,
                        ax=ax[0])

            ax[0].bar_label(ax[0].containers[0])
            ax[0].set_title('Dados brutos',
                            fontweight='bold')

            sns.barplot(x=bank_target_perc.index,
                        y='y',
                        data=bank_target_perc,
                        ax=ax[1])

            ax[1].bar_label(ax[1].containers[0])
            ax[1].set_title('Dados filtrados',
                            fontweight='bold')
        else:
            bank_raw_target_perc.plot(
                kind='pie', autopct='%.2f', y='y', ax=ax[0])
            ax[0].set_title('Dados brutos',
                            fontweight='bold')
            bank_target_perc.plot(
                kind='pie', autopct='%.2f', y='y', ax=ax[1])
            ax[1].set_title('Dados filtrados',
                            fontweight='bold')

        st.pyplot(plt)

        st.write('-----')


# Executa a função principal
if __name__ == "__main__":
    main()

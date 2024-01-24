import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import altair as alt


st.title("1 - Códigos referente ao link:  https://docs.streamlit.io/en/stable/getting_started.html")

st.write("Hello world")

"Usando  Magic - Sempre que o Streamlit vê um valor variável ou literal em sua prórpia linha, ele grava automaticamente isso no seu aplicativo usando st.write"

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

df
st.write("---")

st.write("Meu Codespaces: https://cuddly-fiesta-59jj49v4wwvh49g7.github.dev/")

df2 = pd.DataFrame({'col1': [1, 2, 3]})
df2

st.write("---")

arr = np.random.normal(1, 1, size=100)

fig, ax = plt.subplots()


ax.hist(arr, bins=50)

fig

st.write("---")

"Usando numpy para gerar uma amostra aleatória e despois plotar o DataFrame"

dataframe = np.random.randn(10, 20)
st.dataframe(dataframe)

st.write("---")

"Usando os Pandas Styler para destacar alguns elemntos na tabela interativa"

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))

st.write("---")

st.write("# Usando a biblioteca Altair")

df = pd.DataFrame(
    np.random.randn(200, 3),
    columns=['a', 'b', 'c'])

c = alt.Chart(df).mark_circle().encode(
    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

st.write(c)

st.write("---")

st.write("# Desenhando um gráfico de linha")

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)

st.line_chart(chart_data)

st.markdown('<hr style="border:2px solid #fff">', unsafe_allow_html=True)

st.write("# Entrando com um mapa")

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

st.markdown('<hr style="border:2px solid #fff">', unsafe_allow_html=True)

st.write("# Agora mostrando um mapa de Onde Moro")

# Coordenadas obtidas diretamente do Google Maps
localizacao = [-2.5135503651930615, -44.28797491029731]
zoom_level = 11

# Criação de dados aleatórios ao redor da localização desejada
map_data = pd.DataFrame(
    np.random.randn(50, 2) / [50, 50] + localizacao,
    columns=['lat', 'lon'])

# Exibe o mapa centrado na localização desejada com o zoom configurado
st.map(map_data, zoom=zoom_level)

st.write("--")
st.subheader("Widgets")

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

st.markdown('<hr style="border:2px solid #fff">', unsafe_allow_html=True)

st.subheader("Caixa de seleção mas mostrar ou ocultar um determinado dado")

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

    chart_data

if st.checkbox("Renato Douglas"):
    st.markdown("""Aos poucos está aprendendo""")

st.markdown('<hr style="border:2px solid #fff">', unsafe_allow_html=True)

st.subheader("Caixa de seleção para opções")

df = pd.DataFrame({
    'first column': [i for i in range(1, 101)],

})

option = st.selectbox(
    'Escolha um numero para cácular o seu fatorial',
    df['first column'])
fat = np.arange(1, option+1).cumprod()[-1]
'O fatorial do número selecionado é : ', fat

st.markdown('<hr style="border:2px solid #fff">', unsafe_allow_html=True)

st.markdown('Do lado esquerdo foi adicionado uma barra leteral')
# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (10.0, 75.0)
)

st.markdown('<hr style="border:2px solid #fff">', unsafe_allow_html=True)

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")


st.markdown('<hr style="border:2px solid #fff">', unsafe_allow_html=True)

st.title("2 - Códigos referente ao link: https://docs.streamlit.io/get-started/tutorials/create-an-app")


DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    def lowercase(x): return str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)


st.markdown('<hr style="border:2px solid #fff">', unsafe_allow_html=True)

st.title("3 - Códigos referente ao link: https://docs.streamlit.io/knowledge-base/using-streamlit")


df = pd.DataFrame(
    {
        "Animal": ["Lion", "Elephant", "Giraffe", "Monkey", "Zebra"],
        "Habitat": ["Savanna", "Forest", "Savanna", "Forest", "Savanna"],
        "Lifespan (years)": [15, 60, 25, 20, 25],
        "Average weight (kg)": [190, 5000, 800, 10, 350],
    }
)


def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={
            "Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)


selection = dataframe_with_selections(df)
st.write("Your selection:")
st.write(selection)

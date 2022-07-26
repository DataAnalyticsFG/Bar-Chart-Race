import streamlit as st
import pandas as pd
from raceplotly.plots import barplot
import io
import pandas as pd

#df = pd.read_excel("C://Users/marco.gomez/Downloads/Histórico Cierres por Agencia 06-2022.xlsx")
#df = df.groupby(by = ["Nombre de Agencia", "Mes-Año"]).agg({'Saldo': 'sum', 'PAR1' : 'sum', 'PAR30' : 'sum', '# Créditos' : 'sum'})
#print(df.head(5))
#df.to_excel("C://Users/marco.gomez/Downloads/Histórico Cierres por Agencia v1.xlsx")

st.set_page_config(
     page_title="Gráfico Bar Chart Race Finca GT",
     layout="wide",
     initial_sidebar_state="collapsed"
     #menu_items={
     #    'Get Help': 'https://www.extremelycoolapp.com/help',
     #    'Report a bug':    "https://www.extremelycoolapp.com/bug",
     #    'About': "# This is a header. This is an *extremely* cool app!"
     #}
 )

st.title("Gráfico de barras dinámico Finca GT")

#spreadsheetId = "117829087850796113144"
#gauth = GoogleAuth()
#gauth.LocalWebserverAuth()
#url = "https://www.googleapis.com/drive/v3/files/" + spreadsheetId + "/export?mimeType=application%2Fvnd.openxmlformats-officedocument.spreadsheetml.sheet"
#res = requests.get(url, headers={"Authorization": "Bearer " + gauth.attr['credentials'].access_token})
#values = pd.read_excel(BytesIO(res.content), usecols=None)
#print(values)

df = pd.read_excel("C://Users/marco.gomez/Downloads/Histórico Cierres por Agencia v1.xlsx")
df = df[df['Año'] >= 2017]
column_list = df.columns
#print(df.head(5))
#print(df.columns)
#saldo = df[['Nombre de Agencia', 'Fecha', 'Saldo']]
#par1 = df[['Nombre de Agencia', 'Fecha', 'PAR1']]
#par30 = df[['Nombre de Agencia', 'Fecha', 'PAR30']]



with st.form("form_datos"):

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        item_column = st.selectbox('Nombre de las barras:', column_list, help='Escoja una columna categorica en los datos para comparar en el transcurso del tiempo')
    with col2:
        value_column = st.selectbox('Valores de las barras:', column_list, help='Escoja una columna numérica en los datos para ver evolución')
    with col3:
        time_column = st.selectbox('Evolución Temporal:', column_list, help='Escoja una columna en los datos que represente una evolución temporal (Fecha)')

    col4, col5, col6 = st.columns([1, 1, 1])
    with col4:
        direction = st.selectbox('Seleccione orientación del gráfico:', ['-', 'Horizontal', 'Vertical'], index=0, help='Escoja la orientación de las barras, puede ser Horizonal o Vertical, por defecto es Horizontal')
        if direction == 'Horizontal' or direction == '-':
            orientation = 'horizontal'
        elif direction == 'Vertical':
            orientation = 'vertical'
    with col5:
        item_label = st.text_input('Escriba un label para el eje de las barras:', help='Ejemplo: Top de agencias y su evolución en Saldo de Cartera')
    with col6:
        value_label = st.text_input('Escriba un label para el eje de la métrica', help='Ejemplo: Saldo de Cartera a lo largo del tiempo')

    col7, col8, col9 = st.columns([1, 1, 1])
    with col7:
        num_items = st.number_input('# de Barras:', min_value=5, max_value=50, value=10, step=1, help='Escoja el número de barras a mostrar en el gráfico')
    with col8:
        format = st.selectbox('Mostrar por Año o Mes:', ['-', 'Por Año', 'Por Mes'], index=0, help='Escoja para escoger la animación de manera mensual o anual, por defecto es por Año')
        if format == 'Por Año' or format == '-':
            date_format = '%Y'
        elif format == 'Por Mes':
            date_format = '%x'
    with col9:
        chart_title = st.text_input('Agregar Título al gráfico', help='Ejemplo: Gráfico de evolución de Cartera 2020 - 2022')

    col10, col11, col12 = st.columns([1, 1, 1])
    with col10:
        speed = st.slider('Velocidad de Animación', 10, 1000, 100, step=10, help='Ajustar la velocidad de animación')
        frame_duration = 500 - speed
    with col11:
        chart_width = st.slider('Ancho de Animación', 500, 1000, 500, step=20, help='Ajustar el ancho de la animación')
    with col12:
        chart_height = st.slider('Alto de Animación', 500, 1000, 600, step=20, help='Ajustar el alto de la animación')

    submitted = st.form_submit_button('Ver Gráfico')

if submitted:

    df['time_column'] = pd.to_datetime(df[time_column])
    df['value_column'] = df[value_column].astype(float)

    raceplot = barplot(df, item_column = '%s' % item_column, value_column = '%s' % value_column, time_column = '%s' % time_column, top_entries = num_items)
    fig = raceplot.plot(item_label = item_label, value_label = value_label, frame_duration = frame_duration, date_format = date_format, orientation = orientation)
    fig.update_layout(
        title = chart_title,
        autosize = False,
        width = chart_width,
        height = chart_height,
        paper_bgcolor="lightgray",
    )
    st.plotly_chart(fig, use_container_width=True)

    buffer = io.StringIO()
    fig.write_html(buffer, include_plotlyjs='cdn')
    html_bytes = buffer.getvalue().encode()
    st.download_button(
        label="Descargar gráfico %s" %chart_title,
        data=html_bytes,
        file_name="Gráfico %s.html" %chart_title,
        mime='text/html'
    )

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
st.set_page_config(layout="wide")


women = pd.read_csv('wc_wom_2023.csv')
men = pd.read_csv('cop_lib_2023.csv')

st.title('Assestment Scouting Club América')

### box to box
box_2_box = men[men['Pos'].str.contains("MF")]
box_2_box = box_2_box[(men['Age'] >= 18) & (men['Age'] < 29)]

st.header('Categoría Varonil')

col1, col2 = st.columns(2)
with col1:
    st.markdown('''### Variables clave para evaluar a un "Box to Box":

    - Fls (Faltas Cometidas):
        Refleja la intensidad defensiva del jugador y su capacidad para cortar jugadas del oponente, aunque es importante que mantenga un equilibrio para evitar sanciones.

    - Fld (Faltas Recibidas):
        Un "Box to Box" tiende a ser un jugador muy involucrado en el juego, tanto en defensa como en ataque, lo que podría llevar a recibir muchas faltas debido a su protagonismo en el mediocampo.

    - Int (Intercepciones):
        Las intercepciones son clave para medir la capacidad del jugador de recuperar el balón en posiciones defensivas y medias, iniciando transiciones rápidas al ataque.

    - TklW (Entradas Ganadas):
        Un jugador "Box to Box" debe ser efectivo en los duelos uno a uno para recuperar balones y cortar el avance del oponente.

    - Recov (Recuperaciones de balón):
        Refleja la capacidad del jugador para recuperar balones en posiciones más adelantadas y en el medio campo, crucial para un centrocampista que cubre mucho terreno.

    - Won% (% de Duelos Ganados):
        Refleja la capacidad del jugador para imponerse en los duelos tanto defensivos como ofensivos, un atributo esencial para un "Box to Box".
    
    - Crs (Centros): Si el jugador tiene funciones ofensivas amplias, podría ser útil evaluar la capacidad de enviar centros al área.

    - Off (Fuera de Juego): Esto puede ser relevante si el jugador tiende a involucrarse mucho en las jugadas ofensivas y llega a posiciones de ataque.''')

cols_box_2_box = ['Fls', 'Fld', 'Off', 'Crs', 'Int', 'TklW', 'Recov', 'Won%']
scores_b_2_b = box_2_box[['Player', 'Pos', 'Squad', 'Age'] + cols_box_2_box]
# Calcular el máximo de cada columna en cols_box_2_box
max_values = scores_b_2_b[cols_box_2_box].max()

# Dividir cada registro por el máximo de su columna correspondiente
scores_b_2_b[cols_box_2_box] = men[cols_box_2_box].div(max_values)

# Sumar las columnas en cols_box_2_box y crear la columna 'suma total'
scores_b_2_b['suma_total'] = scores_b_2_b[cols_box_2_box].sum(axis=1)

# Normalizar la columna 'suma_total' tomando el valor más alto y dividiendo cada registro por ese valor
max_suma_total = scores_b_2_b['suma_total'].max()
scores_b_2_b['score'] = scores_b_2_b['suma_total'] / max_suma_total
with col2:
    selected = scores_b_2_b[scores_b_2_b['Player'].isin(["Fernando David Cardozo", "Thiago Maia", "Wanderson"])][['Player', 'Squad', 'Pos', 'Age', 'score']]
    selected['price'] = ['3M', '6M', '8M']
    st.dataframe(selected)
    st.success("El valor asignado a los jugadores está asignado en relación a la página transfer Market")

    men_players = st.multiselect(
    "Puedes seleccionar mas jugadores",
    list(scores_b_2_b['Player']),
    ["Fernando David Cardozo", "Thiago Maia", "Wanderson"],
    )
    # Filtrar los jugadores seleccionados del DataFrame 'men'
    selected_players = scores_b_2_b[scores_b_2_b['Player'].isin(men_players)]

    # Columnas que representan las estadísticas para el radar (box to box)
    cols_box_2_box = ['Fls', 'Fld', 'Off', 'Crs', 'Int', 'TklW', 'Recov', 'Won%']

    # Preparar los datos para el gráfico de radar
    fig = go.Figure()

    # Agregar los datos de cada jugador al gráfico
    for player in selected_players['Player']:
        player_data = selected_players[selected_players['Player'] == player][cols_box_2_box].values.flatten()
        fig.add_trace(go.Scatterpolar(
            r=player_data,
            theta=cols_box_2_box,
            fill='toself',
            name=player
        ))

    # Actualizar el diseño del gráfico
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                #range=[0, 1]  # Ajustar si las variables tienen un rango mayor
            )),
        showlegend=True,
        title="Desempeño de jugadores seleccionados en Box to Box"
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)




#################################### contencion
st.header('Categoría Femenil-Contención')
col1, col2 = st.columns(2)
with col1:
    st.markdown('''### Variables clave para evaluar a una Contención:
                
- Intercepciones (Int): Un buen número de intercepciones refleja que el jugador está cortando pases y controlando el medio campo defensivamente.
- Entradas ganadas (TklW): Los jugadores de contención generalmente tienen un alto número de entradas exitosas.
- Faltas cometidas (Fls): Los centrocampistas defensivos suelen cometer más faltas debido a la naturaleza de su trabajo, que implica frenar el avance de los rivales.
- Recuperaciones (Recov): Número de balones sueltos que el jugador recupera.
- Duelos aéreos ganados (Won%): Muchos centrocampistas defensivos se involucran en duelos aéreos para recuperar balones en el mediocampo.''')

mids = women[women['Pos'].str.contains("MF")]
mids = mids[(women['Age'] >= 18) & (women['Age'] < 29)]
cols_conte = ['Int', 'TklW', 'Fls', 'Recov', 'Won%']
scores_conte = mids[['Player', 'Pos', 'Squad', 'Age'] + cols_conte]
# Calcular el máximo de cada columna en cols_conte
max_values_conte = scores_conte[cols_conte].max()
# Dividir cada registro por el máximo de su columna correspondiente
scores_conte[cols_conte] = women[cols_conte].div(max_values_conte)
# Sumar las columnas en cols_conte y crear la columna 'suma total'
scores_conte['suma_total'] = scores_conte[cols_conte].sum(axis=1)
# Normalizar la columna 'suma_total' tomando el valor más alto y dividiendo cada registro por ese valor
max_suma_total = scores_conte['suma_total'].max()
scores_conte['score'] = scores_conte['suma_total'] / max_suma_total
with col2:
    selected_con = scores_conte[scores_conte['Player'].isin(["Teresa Abelleira", "Christy Ucheibe"])][['Player', 'Squad', 'Pos', 'Age', 'score']]
    st.dataframe(selected_con)

    women_players_c = st.multiselect(
    "Puedes seleccionar mas jugadores",
    list(scores_conte['Player']),
    ["Teresa Abelleira", "Christy Ucheibe"],
    )
    # Filtrar los jugadores seleccionados del DataFrame 'women'
    selected_con_players = scores_conte[scores_conte['Player'].isin(women_players_c)]

    # Preparar los datos para el gráfico de radar
    fig = go.Figure()

    # Agregar los datos de cada jugador al gráfico
    for player in selected_con_players['Player']:
        player_data = selected_con_players[selected_con_players['Player'] == player][cols_conte].values.flatten()
        fig.add_trace(go.Scatterpolar(
            r=player_data,
            theta=cols_conte,
            fill='toself',
            name=player
        ))

    # Actualizar el diseño del gráfico
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                #range=[0, 1]  # Ajustar si las variables tienen un rango mayor
            )),
        showlegend=True,
        title="Desempeño de jugadores seleccionadas para la contención"
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)


############################################################## defensa central
st.header('Categoría Femenil-Defensa Central')
col1, col2 = st.columns(2)
with col1:
    st.markdown('''### Variables clave para evaluar a una Defensa Central:
                
- Intercepciones (Int): Un buen número de intercepciones refleja que el jugador está cortando pases y controlando el medio campo defensivamente.
- Entradas ganadas (TklW): Los jugadores de contención generalmente tienen un alto número de entradas exitosas.
- Recuperaciones (Recov): Número de balones sueltos que el jugador recupera.
- Duelos aéreos ganados (Won%): Muchos centrocampistas defensivos se involucran en duelos aéreos para recuperar balones en el mediocampo.''')

defs = women[women['Pos'].str.contains("DF")]
defs = defs[(women['Age'] >= 18) & (women['Age'] < 29)]
cols_def = ['Int', 'TklW', 'Recov', 'Won%']
scores_def = defs[['Player', 'Pos', 'Squad', 'Age'] + cols_def]
# Calcular el máximo de cada columna en cols_def
max_values_def = scores_def[cols_def].max()
# Dividir cada registro por el máximo de su columna correspondiente
scores_def[cols_def] = women[cols_def].div(max_values_def)
# Sumar las columnas en cols_def y crear la columna 'suma total'
scores_def['suma_total'] = scores_def[cols_def].sum(axis=1)
# Normalizar la columna 'suma_total' tomando el valor más alto y dividiendo cada registro por ese valor
max_suma_total = scores_def['suma_total'].max()
scores_def['score'] = scores_def['suma_total'] / max_suma_total

with col2:
    selected_def = scores_def[scores_def['Player'].isin(["Manuela Vanegas", "Dominique Janssen"])][['Player', 'Squad', 'Pos', 'Age', 'score']]
    st.dataframe(selected_def)

    women_players_c = st.multiselect(
    "Puedes seleccionar mas jugadores",
    list(scores_def['Player']),
    ["Manuela Vanegas", "Dominique Janssen"],
    )
    # Filtrar los jugadores seleccionados del DataFrame 'women'
    selected_def_players = scores_def[scores_def['Player'].isin(women_players_c)]

    # Preparar los datos para el gráfico de radar
    fig = go.Figure()

    # Agregar los datos de cada jugador al gráfico
    for player in selected_def_players['Player']:
        player_data = selected_def_players[selected_def_players['Player'] == player][cols_def].values.flatten()
        fig.add_trace(go.Scatterpolar(
            r=player_data,
            theta=cols_def,
            fill='toself',
            name=player
        ))

    # Actualizar el diseño del gráfico
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                #range=[0, 1]  # Ajustar si las variables tienen un rango mayor
            )),
        showlegend=True,
        title="Desempeño de jugadores seleccionadas para la Defensa central"
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)
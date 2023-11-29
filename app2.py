import pandas as pd
from dash import Dash
from dash import dcc
from dash import html 
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objs as go


# Cargar el DataFrame
historico_csv = 'C:\\Users\\Jaz 2\\Desktop\HATAPY FINAL\\historico_pais_paraguai.csv'
historico_df = pd.read_csv(historico_csv, encoding='latin-1')


# Transformar el DataFrame a formato 'long-form' para el uso en Plotly
historico_df_long = historico_df.melt(id_vars='Año', var_name='Mes', value_name='FocosDeCalor')
historico_df_long = historico_df_long[historico_df_long['Mes'] != 'Total']  # Excluir la columna 'Total'

# Crear un DataFrame con la suma total de 'Focos de Calor' por año
resumen_anual = historico_df_long.groupby('Año').sum().reset_index()

# Crear la aplicación Dash
app = Dash(__name__)

# Crear subgráficos
fig = sp.make_subplots(rows=1, cols=1)

# Añadir barras al subgráfico
fig.add_trace(go.Bar(x=resumen_anual['Año'], y=resumen_anual['FocosDeCalor'], marker_color='orange'))

# Actualizar diseño del subgráfico
fig.update_layout(title='Histórico de Focos de Calor', showlegend=False, xaxis=dict(tickmode='linear'), yaxis=dict(title='Número de Focos de Calor'))

# Definir el diseño de la aplicación
app.layout = html.Div([
    html.H2("Histórico de Focos de Calor en Paraguay"),
    html.P("Seleccione el año:"),
    
    # Dropdown para seleccionar el año
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in historico_df['Año'].unique()],
        value=historico_df['Año'].max(),
        multi=False,
        style={'width': '30%'}
    ),
    
    # Gráfico interactivo por año
    dcc.Graph(id='temperature-graph'),
    
    # Gráfico con el resumen de todos los años
    dcc.Graph(id='annual-summary-graph', figure=fig)
])

# Callback para actualizar el gráfico según el año seleccionado
@app.callback(
    Output('temperature-graph', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_graph(selected_year):
    filtered_df = historico_df_long[historico_df_long['Año'] == selected_year]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=filtered_df['Mes'], y=filtered_df['FocosDeCalor'], marker_color=px.colors.sequential.Reds))
    fig.update_layout(title=f'Focos de Calor en Paraguay en {selected_year}',
                      xaxis_title='Mes', yaxis_title='Número de Focos de Calor')

    return fig


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)



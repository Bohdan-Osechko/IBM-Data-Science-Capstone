import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Завантаження даних
spacex_df = pd.read_csv("dataset_part_2.csv")
max_payload = spacex_df['PayloadMass'].max()
min_payload = spacex_df['PayloadMass'].min()

# Ініціалізація додатка Dash
app = dash.Dash(__name__)

# Макет інтерфейсу
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # ПУНКТ 1.14: Випадаючий список для вибору стартового майданчика
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True
                 ),
    html.Br(),

    # Кругова діаграма успішності
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    
    # ПУНКТ 1.14: Слайдер для вибору маси вантажу
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                    value=[min_payload, max_payload]),

    # Діаграма розсіювання (Payload vs Success)
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callback для кругової діаграми
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='Class', 
                     names='LaunchSite', 
                     title='Total Success Launches By Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['LaunchSite'] == entered_site]
        success_counts = filtered_df['Class'].value_counts().reset_index()
        fig = px.pie(success_counts, values='count', 
                     names='Class', 
                     title=f'Total Success Launches for site {entered_site}')
        return fig

# Callback для діаграми розсіювання
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter(site, payload):
    low, high = payload
    mask = (spacex_df['PayloadMass'] > low) & (spacex_df['PayloadMass'] < high)
    filtered_df = spacex_df[mask]
    
    if site == 'ALL':
        fig = px.scatter(filtered_df, x="PayloadMass", y="Class", 
                         color="Block",
                         title="Correlation between Payload and Success for all Sites")
        return fig
    else:
        filtered_df = filtered_df[filtered_df['LaunchSite'] == site]
        fig = px.scatter(filtered_df, x="PayloadMass", y="Class", 
                         color="Block",
                         title=f"Correlation between Payload and Success for site {site}")
        return fig

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)
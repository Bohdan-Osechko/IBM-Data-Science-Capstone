import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import requests
import io

# ==========================================
# 1. ЗАВАНТАЖЕННЯ ТА ПІДГОТОВКА ДАНИХ
# ==========================================
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv"
response = requests.get(URL)
response.raise_for_status()
csv_content = io.StringIO(response.text)
df = pd.read_csv(csv_content)

# Підготовка даних (як ми робили раніше)
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year

# ==========================================
# 2. ІНІЦІАЛІЗАЦІЯ ДОДАТКУ DASH
# ==========================================
app = dash.Dash(__name__)

# ==========================================
# 3. МАКЕТ ДОДАТКУ (LAYOUT)
# ==========================================
app.layout = html.Div([
    html.H1("Панель аналітики продажів автомобілів", 
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    
    # Випадаючий список для вибору типу звіту
    html.Div([
        html.Label("Виберіть звіт:"),
        dcc.Dropdown(
            id='report-dropdown',
            options=[
                {'label': 'Звіт про рецесію', 'value': 'Recession'},
                {'label': 'Річний звіт', 'value': 'Yearly'}
            ],
            value='Recession', # Значення за замовчуванням
            placeholder='Виберіть тип звіту'
        )
    ], style={'width': '50%', 'padding': '10px', 'fontSize': '20px'}),
    
    # Контейнер для графіків
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flexWrap': 'wrap'})
])

# ==========================================
# 4. CALLBACKS ДЛЯ ІНТЕРАКТИВНОСТІ
# ==========================================
@app.callback(
    Output(component_id='output-container', component_property='children'),
    Input(component_id='report-dropdown', component_property='value')
)
def update_output_container(selected_report):
    if selected_report == 'Recession':
        # Фільтруємо дані для періодів рецесії
        recession_data = df[df['Recession'] == 1]
        
        # --- Графік 1: Середні продажі за роками під час рецесії ---
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig1 = px.line(yearly_rec, x='Year', y='Automobile_Sales', 
                       title="Середні продажі під час рецесії")
        
        # --- Графік 2: Продажі за типом авто під час рецесії ---
        avg_sales_type = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        fig2 = px.bar(avg_sales_type, x='Vehicle_Type', y='Automobile_Sales', 
                      title="Середні продажі за типом авто під час рецесії")
        
        # --- Графік 3: Рекламні витрати за типом авто під час рецесії ---
        adv_type = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig3 = px.pie(adv_type, values='Advertising_Expenditure', names='Vehicle_Type', 
                      title="Витрати на рекламу за типом авто під час рецесії")
        
        # Графік 4: Кореляція ВВП і продажі (Scatter)
        fig4 = px.scatter(recession_data, x='GDP', y='Automobile_Sales', 
                          title="ВВП vs Продажі під час рецесії")

        return [
            html.Div(dcc.Graph(figure=fig1), style={'width': '50%'}),
            html.Div(dcc.Graph(figure=fig2), style={'width': '50%'}),
            html.Div(dcc.Graph(figure=fig3), style={'width': '50%'}),
            html.Div(dcc.Graph(figure=fig4), style={'width': '50%'})
        ]
        
    elif selected_report == 'Yearly':
        # 1. Plot for Yearly Automobile sales (Line Chart)
        yearly_data = df.groupby('Year')['Automobile_Sales'].sum().reset_index()
        fig_yearly_sales = px.line(yearly_data, x='Year', y='Automobile_Sales', 
                                   title="Загальні річні продажі автомобілів")
        
        # 2. Plot for Total Monthly Automobile sales (Line Chart)
        monthly_data = df.groupby(['Year', 'Month'])['Automobile_Sales'].sum().reset_index()
        fig_monthly_sales = px.line(monthly_data, x='Month', y='Automobile_Sales', 
                                    color='Year', title="Місячні продажі автомобілів")

        # 3. Bar chart for Average Advertising Expenditure by Vehicle Type (Bar Chart)
        avg_adv_type = df.groupby('Vehicle_Type')['Advertising_Expenditure'].mean().reset_index()
        fig_avg_adv = px.bar(avg_adv_type, x='Vehicle_Type', y='Advertising_Expenditure',
                             title="Середні витрати на рекламу за типом авто")

        # 4. Pie chart for Total Advertising Expenditure by Vehicle Type (Pie Chart)
        total_adv_type = df.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig_total_adv = px.pie(total_adv_type, values='Advertising_Expenditure', names='Vehicle_Type',
                               title="Загальні витрати на рекламу за типом авто")
    
    # Example for adding multiple graphs to the output container:
    return [
        html.Div(dcc.Graph(figure=fig_yearly_sales), style={'width': '50%'}),
        html.Div(dcc.Graph(figure=fig_monthly_sales), style={'width': '50%'}),
        html.Div(dcc.Graph(figure=fig_avg_adv), style={'width': '50%'}),
        html.Div(dcc.Graph(figure=fig_total_adv), style={'width': '50%'})
    ]
# ==========================================
# 5. ЗАПУСК СЕРВЕРА
# ==========================================
if __name__ == '__main__':
    app.run(debug=True)
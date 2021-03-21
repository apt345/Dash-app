import dash
from dash.dependencies import Input, Output, State
import math
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_table

app = dash.Dash(__name__, title="Arturo and Guille Dash app")

import numpy as np
import pandas as pd
import json

df_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
df = pd.read_csv(df_url).dropna(subset = ['location'])
df=df.drop(['iso_code','total_vaccinations_per_hundred','people_vaccinated_per_hundred'], axis=1)

df_location = df['location'].sort_values().unique()
opt_location = [{'label':x, 'value':x} for x in df_location]
# Discrete Colors in Python
# https://plotly.com/python/discrete-color/
#col_location = {x: px.colors.qualitative.G10[i] for i,x in enumerate(df_location)}

#resolver que selected dates vayan en orden y que al final cuando hace el filtro se haga efectivamente. linea 111

df_dates=df['date'].sort_values().unique()
nrows=len(df_dates)
min_date = df_dates[0]
max_date = df_dates[nrows-1]
selected_dates = [min_date, df_dates[math.floor(nrows/10)], df_dates[math.floor(nrows*2/10)], df_dates[math.floor(nrows*3/10)], df_dates[math.floor(nrows*4/10)], df_dates[math.floor(nrows*5/10)], df_dates[math.floor(nrows*6/10)], df_dates[math.floor(nrows*7/10)], df_dates[math.floor(nrows*8/10)], df_dates[math.floor(nrows*9/10)], max_date]
#print(df_dates)
#print(selected_dates)

#make dates dataframe accessible by index


markdown_text = '''
### Some references
- [Dash HTML Components](https://dash.plotly.com/dash-html-components)
- [Dash Core Components](https://dash.plotly.com/dash-core-components)  
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/) 
- [Dash DataTable](https://dash.plotly.com/datatable)  
'''

table_tab = dash_table.DataTable(
                id='my-table',
                columns=[{"name": i, "id": i} for i in df.columns]
            )

graph_tab = dcc.Graph(id="my-graph")

app.layout= html.Div([
    html.Div([html.H1(app.title, className="app-header--title")],
        className= "app-header",
    ),
    html.Div([  
        dcc.Markdown(markdown_text),
        html.Label(["Select countries:",
            dcc.Dropdown('my-dropdown', options= opt_location, value= [opt_location[0]['value']], multi=True)
        ]),
        html.Label(["Range of dates:",
                 dcc.RangeSlider(id="range",
                     max= 10,
                     min= 0,
                     step= 1/10,
                     marks= selected_dates,
                     value= [0,1],
                 )
        ]),
        html.Div(id='data', style={'display': 'none'}),
        html.Div(id='dataRange', style={'display': 'none'}),
        dcc.Tabs(id="tabs", value='tab-t', children=[
            dcc.Tab(label='Table', value='tab-t'),
            dcc.Tab(label='Graph', value='tab-g'),
        ]),
        html.Div(id='tabs-content')
    ],
    className= "app-body")
])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-t':
        return table_tab
    elif tab == 'tab-g':
        return graph_tab


@app.callback(
     Output('my-table', 'data'),
     Input('data', 'children'), 
     State('tabs', 'value'))
def update_table(data, tab):
    if tab != 'tab-t':
        return None
    dff = pd.read_json(data, orient='split')
    return dff.to_dict("records")

@app.callback(
     Output('my-graph', 'figure'),
     Input('data', 'children'), 
     State('tabs', 'value'))
def update_graph(data, tab):
    if tab != 'tab-g':
        return None
    dff = pd.read_json(data, orient='split')
    dff["location"] = df["location"].astype(str)
    return px.scatter(dff, x="date", y="total_vaccinations", color="location")

@app.callback(Output('data', 'children'), 
    Input('range', 'value'), 
    State('my-dropdown', 'value'))
def filter(range, values):
     #filter by location given in values selector and in dates from range0 and range[1]
     #keep in mind range is between 0 (start of df_dates) and 10 (end of df_dates)

     filter = df['location'].isin(values) & df['date'].between(df_dates[math.floor(range[0]*(nrows-1)/10)], df_dates[math.floor(range[1]*(nrows-1)/10)])

     # more generally, this line would be
     # json.dumps(cleaned_df)
     return df[filter].to_json(date_format='iso', orient='split')


@app.callback(Output('dataRange', 'children'), 
    Input('my-dropdown', 'value'))
def dataRange(values):
    filter = df['location'].isin(values) 
    dff = df[filter]
    min_date = min(dff['date'].dropna())
    max_date = max(dff['date'].dropna())
    return json.dumps({'min_date': min_date, 'max_date': max_date})

if __name__ == '__main__':
    app.server.run(debug=True)
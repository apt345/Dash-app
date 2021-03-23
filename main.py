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


#loading the covid dataset
df_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
df = pd.read_csv(df_url).dropna(subset = ['location'])
#drop some unnecessary columns
df=df.drop(['iso_code','total_vaccinations_per_hundred','people_vaccinated_per_hundred'], axis=1)
#clean of empty dates
df=df.dropna(axis=0)

#find the sorted list of location/countries in alphabetical order
df_location = df['location'].sort_values().unique()
opt_location = [{'label':x, 'value':x} for x in df_location]

#find the sorted list of dates in chronological order
df_dates=df['date'].sort_values().unique()
#create a range of dates uniformly distributed
nrows=len(df_dates)
min_date = df_dates[0]
max_date = df_dates[nrows-1]
selected_dates = [min_date, df_dates[math.floor(nrows/10)], df_dates[math.floor(nrows*2/10)], df_dates[math.floor(nrows*3/10)], df_dates[math.floor(nrows*4/10)], df_dates[math.floor(nrows*5/10)], df_dates[math.floor(nrows*6/10)], df_dates[math.floor(nrows*7/10)], df_dates[math.floor(nrows*8/10)], df_dates[math.floor(nrows*9/10)], max_date]



# Selection for Guille

df_guille = [0,1]
opt_guille = [{'label':x, 'value':x} for x in df_guille]


#References and descriptive text
markdown_text = '''
### Description
This app describes two datasets with interactive options for both of them.
- Covid vaccinations: Information about country and date of your choice
- Guille pon aqui tus cosas

### References
- [COVID-19 information](https://www.who.int/es/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19)
- [Original data from OurWorldInData](https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv)  
'''

#Covid table
table_tab = dash_table.DataTable(
                id='my-table',
                columns=[{"name": i, "id": i} for i in df.columns]
            )

#Covid graph
graph_tab = dcc.Graph(id="my-graph")

#Set tabs corresponding to covid analysis in red
tab_style_Arturo = {
    'borderBottom': '1px solid #d6d6d6',
    'fontWeight': 'bold',
    'backgroundColor': 'red'
}
#Set tabs corresponding to guille's analysis in blue
tab_style_Guille = {
    'borderBottom': '1px solid #d6d6d6',
    'fontWeight': 'bold',
    'backgroundColor': 'blue'
}
#Set that when a tab is selected, it maintains its color but the letter changes to white for Covid and guille's tabs

tab_selected_style_Arturo = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'red',
    'color': 'white'
}

tab_selected_style_Guille = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'blue',
    'color': 'white'
}

#define the app layout
app.layout= html.Div([
    html.Div([html.H1(app.title, className="app-header--title")],
        className= "app-header",
    ),
    html.Div([  
        dcc.Markdown(markdown_text),
        html.Label(["Select countries/continents for Covid analysis:",
            dcc.Dropdown('my-dropdown', options= opt_location, value= [opt_location[0]['value']], multi=True)
        ]),
        html.Label(["Range of dates for Covid analysis:",
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
        html.Label(["Select between 0 and 1 for Guille:",
            dcc.Dropdown('guille-dropdown', options= opt_guille, value= [opt_guille[0]['value']], multi=False)
        ]),
        dcc.Tabs(id="tabs", value='tab-t', children=[
            dcc.Tab(label='Table Covid', value='tab-t', style=tab_style_Arturo, selected_style=tab_selected_style_Arturo),
            dcc.Tab(label='Graph Covid', value='tab-g', style=tab_style_Arturo, selected_style=tab_selected_style_Arturo),
            dcc.Tab(label='Table Guille', value='tab-t-2', style=tab_style_Guille, selected_style=tab_selected_style_Guille),
            dcc.Tab(label='Graph Guille', value='tab-g-2', style=tab_style_Guille, selected_style=tab_selected_style_Guille),
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
    return px.scatter(dff, x="date", y="total_vaccinations", color="location")

@app.callback(Output('data', 'children'), 
    Input('range', 'value'), 
    State('my-dropdown', 'value'))
def filter(range, values):
     #filter by location given in values selector and in dates from range0 and range[1]
     #keep in mind range is between 0 (start of df_dates) and 10 (end of df_dates)

     filter = df['location'].isin(values) & df['date'].between(df_dates[math.floor(range[0]*(nrows-1)/10)], df_dates[math.floor(range[1]*(nrows-1)/10)])
     return df[filter].to_json(date_format='iso', orient='split')


@app.callback(Output('dataRange', 'children'), 
    Input('my-dropdown', 'value'))
def dataRange(values):
    filter = df['location'].isin(values) 
    dff = df[filter]
    dff_dates = dff['date'].sort_values().unique()
    min_dates = dff_dates[0]
    max_dates = dff_dates[len(dff_dates) - 1]
    return json.dumps({'min_date': min_dates, 'max_date': max_dates})

if __name__ == '__main__':
    app.server.run(debug=True)
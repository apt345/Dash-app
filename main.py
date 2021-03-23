import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_table

app = dash.Dash(__name__, title="Arturo and Guille Dash app")

import numpy as np
import pandas as pd
import json
import math

#######ARTURO########
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
############################

###GUILLERMO################
# Load the data and select the columns
data = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data')
data.columns = ['age','workclass','fnlwgt','education','education_num','marital_status','occupation','relationship','race','sex','cap_gain','cap_loss','hours_week','native_country','label']
data = data[['age','workclass','education','race','sex','hours_week','label']]

# Drops missing values (marked as ' ?' in the dataframe)
data = data[~data.eq(' ?').any(1)]
#data.isna().sum()

# Modify the categories
data['workclass'] = data['workclass'].replace('.*^\\ Self.*', 'Self Employed', regex=True)
data['workclass'] = data['workclass'].replace([' Local-gov', ' State-gov', ' Federal-gov'], 'Public', regex=True)
data['workclass'] = data['workclass'].replace(' Without-pay', 'Without Pay', regex=True)
data['workclass'] = data['workclass'].replace(' Never-worked', 'Never Worked', regex=True)
data['workclass'] = data['workclass'].replace(' Private', 'Private', regex=True)

data['education'] = data['education'].replace(' 1st-4th', 'Elementary School', regex=True)
data['education'] = data['education'].replace([' 5th-6th',' 7th-8th'], 'Middle School', regex=True)
data['education'] = data['education'].replace([' 9th',' 10th',' 11th',' 12th'], 'High School', regex=True)
data['education'] = data['education'].replace(' Some-college', 'Unfinnished College', regex=True)
data['education'] = data['education'].replace(' Assoc-voc', 'Assoc', regex=True)
data['education'] = data['education'].replace(' Assoc-acdm', 'Assoc', regex=True)

data['race'] = data['race'].replace(' Amer-Indian-Eskimo', 'Ind-Eskimo', regex=True)
data['race'] = data['race'].replace(' Asian-Pac-Islander', 'Asian-Pac', regex=True)

# Convert categorical variables into 'category'
data[['workclass','education','race','sex','label']] = data[['workclass','education','race','sex','label']].astype("category")

# Convert label into (0,1)
data['label'] = np.where(data['label'] == ' >50K', 1, 0)

#########################################3

# Selection for Guille
opt_label = [{'label':'Less than 50K', 'value':0},
             {'label':'More than 50K', 'value':1}]

opt_var = [{'label':col, 'value':col} for col in data.columns]


#References and descriptive text
markdown_text = '''
### Description
This app describes two datasets with interactive options for both of them.
- Covid vaccinations: Information about country and date of your choice.
- Adult Income: Data from and US Income Census, which classifies individuals in smaller or larger than US$ 50K anual income.
### References
- [COVID-19 information] (https://www.who.int/es/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19)
- [Original data from OurWorldInData] (https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv)  
- [Original Adult Income dataset] (https://archive.ics.uci.edu/ml/datasets/Adult)
'''

#Covid table
table_tab = dash_table.DataTable(
    id='my-table',
    columns=[{"name": i, "id": i} for i in df.columns]
)

#Adult table
table_tab2 = dash_table.DataTable(
    id='my-table2',
    columns=[{"name": i, "id": i} for i in data.columns]
)

#Covid graph
graph_tab = dcc.Graph(id="my-graph")

#Covid graph
graph_tab2 = dcc.Graph(id="my-graph2")

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

#app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])

#define the app layout
app.layout= html.Div([

    html.Div([html.H1(app.title, className="app-header--title")],
             className= "app-header"
    ),

    html.Div([
        html.Div(id='data', style={'display': 'none'}),
        html.Div(id='data2', style={'display': 'none'})
    ]),

    dcc.Markdown(markdown_text),
    html.Br(),

    html.H2('COVID Dataset Parameters'),
    html.Div([

        html.Label(["Select countries/continents for Covid analysis:",
                    dcc.Dropdown('my-dropdown', options= opt_location, value= [opt_location[0]['value']], multi=True)
                    ]),

        html.Br(),

        html.Label(["Range of dates for Covid analysis:",
                    dcc.RangeSlider(id="range",
                                    max= 10,
                                    min= 0,
                                    step= 1/10,
                                    marks= selected_dates,
                                    value= [0,1],
                                    )
                    ]),

        html.Div(id='dataRange')
    ]),

    html.Br(),

    html.H2('Adult Income Dataset Parameters'),
    html.Div([

        html.Label(["Select the income range(s):",
                    dcc.Checklist(
                        id='checkbox',
                        options=opt_label,
                        value=0
                    )]),

        html.Br(),

        html.Label(["Select the variable:",
                    dcc.Dropdown(
                        'my-dropdown2',
                        options=opt_var,
                        value='age'
                    )]),
    ]),

    html.Br(),
    html.Br(),

    html.Div([
        dcc.Tabs(id="tabs", value='tab-t', children=[
            dcc.Tab(label='Table Covid', value='tab-t', style=tab_style_Arturo, selected_style=tab_selected_style_Arturo),
            dcc.Tab(label='Graph Covid', value='tab-g', style=tab_style_Arturo, selected_style=tab_selected_style_Arturo),
            dcc.Tab(label='Table Income', value='tab-t2', style=tab_style_Guille, selected_style=tab_selected_style_Guille),
            dcc.Tab(label='Graph Income', value='tab-g2', style=tab_style_Guille, selected_style=tab_selected_style_Guille)
        ]),#children, Tabs
        html.Div(id='tabs-content')
    ],
        className= "app-body") #div
    ])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-t':
        return table_tab
    elif tab == 'tab-g':
        return graph_tab
    elif tab == 'tab-t2':
        return table_tab2
    elif tab == 'tab-g2':
        return graph_tab2

###ARTURO###
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
              Input('range', 'value'))
def dataRange(range):
    return json.dumps({'Minimum_selected_date': df_dates[math.floor(range[0]*(nrows-1)/10)], 'Maximum_selected_date': df_dates[math.floor(range[1]*(nrows-1)/10)]})

######

###GUILLE###
@app.callback(
    Output('my-table2', 'data'),
    Input('data2', 'children'),
    State('tabs', 'value'))
def update_table(data, tab):
    if tab != 'tab-t2':
        return None
    dff = pd.read_json(data, orient='split')
    return dff.to_dict("records")

@app.callback(
    Output('my-graph2', 'figure'),
    Input('data', 'children'),
    State('tabs', 'value'))
def update_graph(data, tab):
    if tab != 'tab-g2':
        return None
    dff = pd.read_json(data, orient='split')
    return px.scatter(dff, x="date", y="total_vaccinations", color="location")

@app.callback(Output('data2graph', 'children'),
              Input('checkbox', 'value'),
              Input('my-dropdown2', 'value'))
def filter2graph(label, variable):
    filter = data['label'].isin(label)
    #select = variable
    return data[filter, variable].to_json(date_format='iso', orient='split')


@app.callback(Output('data2', 'children'),
              Input('checkbox', 'value'))
def filter2(label):
    filter = data['label'].isin(label)
    return data[filter].to_json(date_format='iso', orient='split')
######



if __name__ == '__main__':
    app.server.run(debug=True)
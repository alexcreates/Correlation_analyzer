import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import Dashboard_correlation as Correlation_tool
DEBUG = True

app = dash.Dash()
app.config['suppress_callback_exceptions']=True
df = pd.read_csv('/Users/mac/Desktop/PyFi/Historical_Stock_Data/Yahoo/ASYS_1983_daily.csv', index_col='Date', parse_dates=True)


features = df.columns
colors = {'background': '#1c1c1c', 'text': '#efefef'}

app.layout = html.Div([html.P('Correlations', style={'fontSize': 40,'marginLeft': 50, 'fontWeight': 'light', 'fontFamily': 'verdana', 'letterSpacing': 10, 'color': 'white', 'marginBottom': -10}),
                            # Child div 1
                            # Independent X Axis Input
                            html.Div([html.P("Independent 'X'", style={'fontSize': 14, 'color': colors['text'], 'fontFamily': 'verdana', 'fontWeight': 100, 'letterSpacing': 3}),
                                     dcc.Dropdown(id='xaxis',
                                                  options=[{'label': i.title(), 'value': i} for i in features],
                                                  value='High')],
                                                  style={'width': '15%', 'display': 'inline-block', 'marginLeft': 70}),
                            # Child div 2
                            # Dependent Y Axis Input
                            html.Div([html.P("Dependent 'Y'", style={'fontSize': 14, 'color': colors['text'], 'fontFamily': 'verdana', 'fontWeight': 100, 'letterSpacing': 3}),
                                      dcc.Dropdown(id='yaxis',
                                                   options=[{'label': i.title(), 'value': i} for i in features],
                                                   value='Low')],
                                                   style={'width': '15%', 'paddingLeft': 20,'display': 'inline-block', 'marginLeft': 80}),
                            # Correlation Graph
                            # Correlation Graph
                            html.Div([dcc.Graph(id='correlation_graphic',
                                                figure = {'layout': {'plot_bgcolor': colors['background'],
                                                          'paper_bgcolor': colors['background'],
                                                          'font': {'color': colors['text']},
                                                          'title': 'Dash Data Visualization',
                                                          'opacity': 0.5}})],
                                                          style = {'width': 700}),
                            html.Div([html.P(id='pearsonR',
                                              style={'fontSize': 12, 'color': '#c9c5c5', 'paddingTop': 25, 'fontWeight': 200, 'fontFamily': 'verdana', 'letterSpacing': 4, 'marginLeft': 500, 'lineWeight': 100, 'marginTop': -150, 'position': 'absolute'})],
                                              style={'width':'30%', 'display':'inline-block', 'verticalAlign':'top'}),
                            # Density Result
                            html.Div([html.H4(id='density',
                                              style={'fontSize': 12, 'color': '#c9c5c5', 'paddingTop': 25, 'fontWeight': 200, 'fontFamily': 'verdana', 'letterSpacing': 4, 'marginLeft': 500, 'lineWeight': 100, 'marginTop': -150, 'position': 'absolute'})],
                                              style={'width':'30%', 'display':'block', 'verticalAlign':'top'})
                            # PearsonR Result

], style={'padding':20, 'backgroundColor': colors['background']})









#####################################################
    #                 Methods                   #
#####################################################

@app.callback(Output('pearsonR', 'children'),
             [Input('xaxis', 'value'),
              Input('yaxis', 'value')])
def find_pr(xaxis_name, yaxis_name):
    pr = np.corrcoef(df[xaxis_name], df[yaxis_name])[0,1]
    return 'pearsonR: {:.9f}'.format(pr)

#_____________________________________________________
@app.callback(Output('correlation_graphic', 'figure'),
             [Input('xaxis', 'value'),
              Input('yaxis', 'value')])
def update_graph(xaxis_name, yaxis_name):
    return {'data': [go.Scatter(
                        x=df[xaxis_name],
                        y=df[yaxis_name],
                        text='A',
                        mode='markers',
                        marker={'size': 15, 'opacity': 0.5, 'line': {'width': 0.5, 'color': 'white'}}
                        )],
            'layout': {'xaxis': {'title': xaxis_name.title(),
                                 'tick0': 0,
                                 'dtick': 2,
                                 'ticklen': 0,
                                 'tickwidth': 1,
                                 'gridcolor': '#444444',
                                 'tickcolor': 'white'},
                       'yaxis': {'title': yaxis_name.title()},
                                 'margin': {'l': 40, 'b': 40, 't': 10, 'r': 0},
                                 'hovermode': 'closest',
                                 'plot_bgcolor': colors['background'],
                                 'paper_bgcolor': colors['background'],
                                 'font': {'color': colors['text']}
                        }}





#               Density Evaluation
#_____________________________________________________
@app.callback(
    Output('density', 'children'),
    [Input('correlation_graphic', 'selectedData')])
def find_density(selectedData):
    pts = len(selectedData['points'])
    rng_or_lp = list(selectedData.keys())
    rng_or_lp.remove('points')
    max_x = max(selectedData[rng_or_lp[0]]['x'])
    min_x = min(selectedData[rng_or_lp[0]]['x'])
    max_y = max(selectedData[rng_or_lp[0]]['y'])
    min_y = min(selectedData[rng_or_lp[0]]['y'])
    area = (max_x-min_x)*(max_y-min_y)
    d = pts/area
    return 'density: {:.6f}'.format(d)







if __name__ == '__main__':
    app.run_server()

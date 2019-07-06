import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.io as pio
from collections import deque
from dash.dependencies import Input, Output
import sqlite3
import pandas as pd
import os
import time

app = dash.Dash(__name__)


app.layout = html.Div(
        [html.Div([
                html.H2(dcc.Markdown('_Rapid Machining Solutions - Makino Spindle Utilization_'), 
                style={'textAlign': 'center'}),
        ]),
        html.Div([
                dcc.Graph(id='Cumulative_Target'),
                dcc.Interval(
                        id='interval-component',
                        interval=10*1000, # in milliseconds
                        n_intervals=0
                )
                ], style={'display': 'inline-block', 'width':'49%'}),
         html.Div([
                 dcc.Graph(id='Live_Target'),
                ], style={'display': 'inline-block', 'width':'49%'}),
         html.Div([
                 dcc.Graph(id='Live_UTIL'),
                ]) 
          
         ], style={'width': '100%', 'display': 'inline-block'})

@app.callback(Output('Cumulative_Target', 'figure'),
              [Input('interval-component', 'n_intervals')])
def Cumul_TRGT(n):
              
        date = pd.to_datetime('today') - pd.Timedelta('30 days')
        date = str(date)[0:10]
        path = os.getcwd() + '\\DATA\\' + 'util.db'
        conn = sqlite3.connect(path)
        c = conn.cursor()
        
        df = pd.read_sql("SELECT * FROM MACH_UTIL WHERE DATE > '%s'" % date, conn)
        
        
        
        dates = list((pd.to_datetime(i) - pd.to_datetime('today')).days + 1 for i in df.DATE)
        
        
        X = dates
        Y = df.CUMUL_HOURS
        
        trace1 = go.Bar(
            x=X,
            y=Y,
            name='Cumulative'
        )        
        data = [trace1]
        layout = go.Layout(
            title=go.layout.Title(
                text='Live Monthly Cumulative',
                x=0
            ),
            xaxis=go.layout.XAxis(
                title=go.layout.xaxis.Title(
                    text='Date',
                    font=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )
                )
            ),
            yaxis=go.layout.YAxis(
                title=go.layout.yaxis.Title(
                    text='Hours',
                    font=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )
                )
            )
        )     
        
        return({
        "data": data,

        "layout": layout})



@app.callback(Output('Live_Target', 'figure'),
              [Input('interval-component', 'n_intervals')])
def Live_TRGT(n):
              
        time = pd.to_datetime(str(pd.to_datetime('today'))[0:10] + ' 00:00:01.00')
        time = str(time)[10:]
        
        path = os.getcwd() + '\\DATA\\'
        db_path = path + 'util.db'
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        df = pd.read_sql("SELECT * FROM LIVE_UTIL WHERE DATE > '%s'" % time, conn)
        
        
        X = df.DATE
        Y2 = df.TARGET_HOURS
        Y = df.HOURS
        
        trace1 = go.Scatter(
            x=X,
            y=Y,
            name='Current Utilization'
        )
        trace2 = go.Scatter(
            x=X,
            y=Y2,
            name='Current Target'
        )      
        data = [trace1, trace2]
        layout = go.Layout(
            title=go.layout.Title(
                text='Live Utilization to Target',
            ),
            xaxis=go.layout.XAxis(
                title=go.layout.xaxis.Title(
                    text='Time',
                    font=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )
                )
            ),
            yaxis=go.layout.YAxis(
                title=go.layout.yaxis.Title(
                    text='Hours',
                    font=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )
                )
            )
        )     
        
        now = pd.to_datetime('today')
        print(str(now)[11:19])
        if "23:59:50" <= str(now)[11:19] <= "23:59:59":
                pio.write_image(go.Figure({'data':data, 'layout':layout}), (path + '\\ARCHIVE_IMGs\\' + str(now)[0:10] + '.jpeg'))
                
        return({
        "data": data,

        "layout": layout})

@app.callback(Output('Live_UTIL', 'figure'),
              [Input('interval-component', 'n_intervals')])
def Live_TRGT(n):
              
        time = pd.to_datetime(str(pd.to_datetime('today'))[0:10] + ' 00:00:01.00')
        time = str(time)[10:]
        print(time)
        path = os.getcwd() + '\\DATA\\' + 'util.db'
        conn = sqlite3.connect(path)
        c = conn.cursor()
        
        df = pd.read_sql("SELECT * FROM LIVE_UTIL WHERE DATE > '%s'" % time, conn)
        
        
        X = df.DATE
        Y = df.HOURS
        
        trace1 = go.Scatter(
            x=X,
            y=Y,
            name='Current Utilization'
        )
         
        data = [trace1]
        layout = go.Layout(
            title=go.layout.Title(
                text='Live Utilization',
            ),
            xaxis=go.layout.XAxis(
                title=go.layout.xaxis.Title(
                    text='Time',
                    font=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )
                )
            ),
            yaxis=go.layout.YAxis(
                title=go.layout.yaxis.Title(
                    text='Hours',
                    font=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )
                )
            )
        )     
        
        return({
        "data": data,

        "layout": layout})
app.run_server()        



import dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
#import mh_z19

# Load data
df = pd.read_csv('stockdata2.csv', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df['Date'])

def getCO2():
    return mh_z19.read_all()['co2']

# Initialise the app
app = dash.Dash(__name__,
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ])


# Define the app
app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                   html.Div(className='four columns div-user-controls',
                                            children=[
                                                html.H1('CO2: '+ getCO2()),                                                                
                                            ]),  # Define the left element
                                   # Define the right element
                                   html.Div(
                                       className='eight columns div-for-charts bg-grey')
                               ])
                      ])
# Run the app
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050")




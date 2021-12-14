import dash
from dash import html
import pandas as pd
import mh_z19
import dash_daq as daq
# Load data
df = pd.read_csv('stockdata2.csv', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df['Date'])


def getCO2():
    return str(mh_z19.read_all()['co2'])



def gauge():
    val = getCO2()
    return daq.Gauge(
        color={"gradient": True, "ranges": {
            "green": [0, 400], "darkgreen": [400, 1000],"yellow": [1000, 2000], "red": [2000, 3000]}},
        value=val,
        label={'label':'CO2: {} ppm'.format(val), 'style':{'font-size':'30px'}},
        max=3000,
        min=0,
    )


# Initialise the app
app = dash.Dash(__name__,
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ])


# Define the app
app.layout = html.Div(className='row',  # Define the row element
                      children=[
                          html.Div(className='four columns div-user-controls',
                                   children=[
                                       #  html.H1('CO2: ' + getCO2()),
                                       gauge()
                                   ]),  # Define the left element
                      ],
                   #   style={"height": "100%", "width": "100%"}
                      )


# Run the app
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050")

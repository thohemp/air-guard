import dash
from dash import html
import mh_z19
import dash_daq as daq
import datetime

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106, ssd1306
from PIL import ImageFont, ImageDraw, Image

import threading
import time
from time import sleep

#serial = i2c(port=1, address=0x3C)
#device = sh1106(serial)

oled_font = ImageFont.truetype('FreeSans.ttf', 14)
oled_font2 = ImageFont.truetype('FreeSans.ttf', 20)

CO2 = 0

def getCO2():
    print("here")
    try:
        val = mh_z19.read_all()['co2']
    except:
        return 0
    return val

def display_data():
    CO2 = getCO2()
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline = "white", fill = "black")
        draw.text((5, 5), "CO2", font = oled_font, fill = "white")
        draw.text((30, 30), str(CO2)+" ppm", font = oled_font2, fill = "white")
 #   sleep(1000)

def time():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')


sensor = threading.Thread(target=display_data)
sensor.daemon = True
#sensor.start()

def gauge():
    val = getCO2()
    return daq.Gauge(
	value = val,
        color={"gradient": True,'style':{'font-size':'30px'}, "ranges": {
            "green": [0, 400], "darkgreen": [400, 1000],"yellow": [1000, 2000], "red": [2000, 3000]}},
        label={'label':'CO2: {} ppm'.format(val), 'style':{'font-size':'30px'}},
        max=3000,
        min=0,
        size=300,
	scale={'custom':{'0':{'label':'0','style':{'font-size':'20px'}},
			'600':{'label':'600','style':{'font-size':'20px'}},
			'1200':{'label':'1200','style':{'font-size':'20px'}},
			'1800':{'label':'1800','style':{'font-size':'20px'}},
			'2400':{'label':'2400','style':{'font-size':'20px'}},
			'3000':{'label':'3000','style':{'font-size':'20px'}}
			}
		}
    )


def app_layout():
    return html.Div(className='row',  # Define the row element
                      children=[
                          html.H6(time()),
                          html.Div(className='four columns div-user-controls',
                                   children=[
                                       gauge()
                                   ]),  # Define the left element
                      ],
                   #   style={"height": "100%", "width": "100%"}
                      )

# Initialise the app
app = dash.Dash(__name__,
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ])


# Define the app
app.layout = app_layout


# Run the app
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="80")


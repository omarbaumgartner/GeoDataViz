import webbrowser
from folium import Map
from folium.plugins import MousePosition,FloatImage,TimestampedGeoJson
from geodataviz.birds import birds_to_GEOJSON, generate_birds_legend
from geodataviz.wildfires import wildfires_to_GEOJSON, generate_wildfires_legend
from tkinter import *

def generate_map(birds_feature, wildfires_feature, from_date, to_date):
    print("Generating map..")
    m = Map(zoom_start=2, min_zoom=2,
                   max_zoom=10, control_scale=True, max_bounds=True)
    features = []
    if(birds_feature == 1):
        print("Birds : selected")
        birds_data = birds_to_GEOJSON(from_date, to_date)
        features += birds_data[0]
        birds_legend_path = generate_birds_legend(birds_data[1], birds_data[2])
        FloatImage(birds_legend_path, bottom=8, left=3).add_to(m)
   
    if(wildfires_feature == 1):
        print("WildFire : selected")
        wildfires_data = wildfires_to_GEOJSON(from_date, to_date)
        features += wildfires_data
        wildfires_legend_path = generate_wildfires_legend()
        FloatImage(wildfires_legend_path, bottom=80, left=85).add_to(m)

    MousePosition().add_to(m)
    result_map = TimestampedGeoJson({
        'type': 'FeatureCollection',
        'features': features,
    }, period='P1D', add_last_point=True,min_speed=1, max_speed=20, duration='P1M')

    result_map.add_to(m)
    m.save('index.html')
    url = 'index.html'
    print("Opening WebBrowser ...")
    webbrowser.open(url, new=0)  # open in new tab

birds = 0
wildfire = 0

def compile():
    if from_slider.get() <= to_slider.get():
        displayed_message.set("Loading..")
        generate_map(birds, wildfire, from_slider.get(), to_slider.get())
    else:
        displayed_message.set("Wrong date range")


def birdval():
    global birds
    if birds == 0:
        birds = 1
    else:
        birds = 0

def wildfireval():
    global wildfire
    if wildfire == 0:
        wildfire = 1
    else:
        wildfire = 0

def reset():
    global birds
    global wildfire
    var_birds.set(0)
    var_wildfires.set(0)
    from_slider.set(2010)
    to_slider.set(2010)
    birds = 0
    wildfire = 0

top = Tk()
displayed_message = StringVar()
var_birds = IntVar()
var_wildfires = IntVar()
top.title("GeoDataViz")

Label(top, text="Select what features you'd like to see").grid(row=0, sticky=W)

ErrorLabel = Label(top, textvariable=displayed_message)
ErrorLabel.grid(row=1, sticky=E)

BirdBox = Checkbutton(top, text="Birds Migration", variable=var_birds,
                      command=birdval)
BirdBox.grid(row=1, sticky=W)

WildFireBox = Checkbutton(top, text="Wildfires", variable=var_wildfires,
                          command=wildfireval)

WildFireBox.grid(row=3, sticky=W)

resetButton = Button(
    top, text="Reset", command=reset)
resetButton.grid(row=6, column=1)

startButton = Button(
    top, text="Visualize", command=compile)
startButton.grid(row=6, column=2)

from_slider = Scale(top, label="From", from_=2010, to=2013,
                   orient=HORIZONTAL)

from_slider.grid(row=5, sticky=W)

to_slider = Scale(top, label="To", from_=2010, to=2013,
                 orient=HORIZONTAL)
to_slider.grid(row=5, sticky=E)

top.mainloop()

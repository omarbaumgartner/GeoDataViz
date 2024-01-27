import pandas as pd 
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import yaml

# Load config file
with open("config.yaml", "r") as stream:
    config = yaml.safe_load(stream)
    font_path = config["font_path"]
    data_path = config["wildfires"]["data_path"]
    legend_path = config["wildfires"]["legend_path"]

# Format time
def format_time(time: int):
    time_str = str(time)
    if len(time_str) == 1:
        time_formatted = "00:"+"0"+time_str[0]
    elif len(time_str) == 2:
        time_formatted = "00:"+time_str[0]+time_str[1]
    elif len(time_str) == 3:
        time_formatted = "0"+time_str[0]+":"+time_str[1]+time_str[2]
        pass
    else:
        time_formatted = time_str[0]+time_str[1]+":"+time_str[2]+time_str[3]
        pass
    return time_formatted

# Process data into a readable format
def wildfires_to_GEOJSON(from_date, to_date):
    file = pd.read_csv(data_path)
    features = []
    
    for row in file.iterrows():
        # print(round(each[1]["Frp"]/diff))
        data = row[1]['Date']
        year = data[0:4]
        if int(year) >= from_date and int(year) <= to_date:
            time = format_time(row[1]['Time'])
            time1 = row[1]['Date']+" "+time+":00"
            timestampobject = datetime.strptime(
                time1, '%Y-%m-%d %H:%M:%S')
            point = {
                "type": "Feature",
                "geometry":
                    {
                        "type": "Point",
                        "coordinates": [row[1]['Longitude'], row[1]['Latitude']]

                    },
                "properties":
                    {'style': {
                        'color': 'red',
                        'opacity': 0.7
                    },
                        'icon': 'circle',
                        'iconstyle': {
                            'iconColor': 'red',
                            'fillOpacity': 0.2,
                            'stroke': 'true',
                            'radius': 2
                    },
                        "time": str(timestampobject),
                        'popup': "Date : "+str(timestampobject)
                    },
            }
            features.append(point)
    return features

# Generate legend
def generate_wildfires_legend():
    img = Image.new('RGBA', (115, 40), color=(255, 255, 255, 0))
    font = ImageFont.truetype(font_path, 15)
    ImageDraw.Draw(img).text((10, 5), "Wildfires :", fill=(0, 0, 0), font=font)
    ImageDraw.Draw(img).ellipse((90, 12, 100, 22), fill=(255, 0, 0))
    img.save(legend_path)
    return legend_path

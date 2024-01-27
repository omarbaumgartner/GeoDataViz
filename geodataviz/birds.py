import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import random
import yaml

# Load config file
with open("config.yaml", "r") as stream:
    config = yaml.safe_load(stream)
    data_path = config["birds"]["data_path"]
    font_path = config["font_path"]
    legend_path = config["birds"]["legend_path"]

# Process data into a readable format
def birds_to_GEOJSON(from_date, to_date):
    birds_dicts = []
    birdstag = []
    allcords = []
    alldates = []
    features = []
    colors = []
    data = pd.read_csv(data_path)

    for row in data.iterrows():
        tag = row[1]["Tag"]
        coords = [row[1]["Longitude"], row[1]["Latitude"]]
        date = row[1]["Date"]
        if int(date[0:4]) >= from_date and int(date[0:4]) <= to_date:
            if tag in birdstag:
                index = birdstag.index(tag)
                allcords[index].append(coords)
                alldates[index].append(date)
            else:
                birdstag.append(tag)
                index = birdstag.index(tag)
                allcords.append([coords])
                alldates.append([date])
    for i in range(0, len(birdstag)):

        def r():
            return random.randint(0, 255)

        color = "#{:02x}{:02x}{:02x}".format(r(), r(), r())
        colors.append(color)
        sub_dict = {
            "coordinates": allcords[i],
            "dates": alldates[i],
            "color": color,
            "birdtag": str(birdstag[i]),
        }
        birds_dicts.append(sub_dict)
        features += [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": bird_dict["coordinates"],
                },
                "properties": {
                    "times": bird_dict["dates"],
                    "icon": "circle",
                    "iconstyle": {
                        "iconColor": bird_dict["color"],
                        "fillOpacity": 1,
                        "stroke": "true",
                        "radius": 6,
                    },
                    "style": {"color": bird_dict["color"], "opacity": 1},
                    "popup": "Bird " + bird_dict["birdtag"],
                },
            }
            for bird_dict in birds_dicts
        ]
    return features, colors, birdstag

# Generate legend
def generate_birds_legend(colors, tags):
    img = Image.new("RGBA", (115, 50 + len(colors) * 20), color=(255, 255, 255, 0))
    i = 1
    j = 0
    x1 = 10
    x2 = 20
    font = ImageFont.truetype(font_path, 15)
    ImageDraw.Draw(img).text((10, 5), "Birds :", fill=(0, 0, 0), font=font)
    for i in range(0, len(colors)):
        x1 = x1 + j
        x2 = x2 + j
        ImageDraw.Draw(img).ellipse((10, 32 + j, 20, 42 + j), fill=colors[i])
        ImageDraw.Draw(img).text(
            (25, 25 + j), "Bird " + str(tags[i]), fill=(0, 0, 0), font=font
        )
        i += 1
        j += 20
    img.save(legend_path)
    return legend_path

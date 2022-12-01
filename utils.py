from jinja2 import Environment, FileSystemLoader
import folium
import pandas as pd
import plotly.express as px


def export_html(filename: str, content: str):
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... wrote {filename}")


def sample_dataframe():
    return pd.read_csv("student.csv", index_col=0)


def sample_plot():
    students = pd.read_csv("student.csv", index_col=0)
    mean_mark = students.groupby("gender")["mark"].mean()
    fig = px.bar(mean_mark)
    return fig


def sample_map():
    location = "https://data.smartdublin.ie/dataset/33ec9fe2-4957-4e9a-ab55-c5e917c7a9ab/resource/2dec86ed-76ed-47a3-ae28-646db5c5b965/download/dublin.csv"
    bike_station_locations = pd.read_csv(location)
    bike_station_locations = bike_station_locations[["Latitude", "Longitude", "Name"]]
    map = folium.Map(
        location=[
            bike_station_locations.Latitude.mean(),
            bike_station_locations.Longitude.mean(),
        ],
        zoom_start=14,
        control_scale=True,
    )
    for index, location_info in bike_station_locations.iterrows():
        folium.Marker(
            [location_info["Latitude"], location_info["Longitude"]],
            popup=location_info["Name"],
        ).add_to(map)
    return map


def render_template():
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("styled_template.html")

    table = sample_dataframe().head()
    plot = sample_plot()
    map = sample_map()

    context = {
        "title": "Testing jinja templates",
        "table": table.to_html(),
        "plot": plot.to_html(),
        "map": map._repr_html_(),
    }

    content = template.render(context)
    export_html("sample.html", content)

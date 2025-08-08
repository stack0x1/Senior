from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd
import os
from flask import send_from_directory

df = pd.read_csv("speeders.csv")

# Keep lat/lon in df for mapping
fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    hover_name=df.columns[1] if len(df.columns) > 1 else None,
    hover_data={"lat": True, "lon": True},
    zoom=16,
    height=350
)

fig.update_traces(marker=dict(size=25, color="red"))

fig.update_layout(
    mapbox_style="open-street-map",
    margin=dict(l=0, r=0, t=0, b=0),
    uirevision="map-static"
)

app = Dash(__name__)

def generate_table(dataframe, max_rows=15):
    # Exclude lat/lon columns from table display
    cols = [c for c in dataframe.columns if c not in ("lat", "lon")]
    rows = []
    for i in range(min(len(dataframe), max_rows)):
        cells = []
        for j, col in enumerate(cols):
            if j == 0:  # adjust index if needed, here 3rd visible col is image
                img_src = str(dataframe.iloc[i][col])
                cells.append(html.Td(html.Img(src=img_src, style={
                    "height": "200px",
                    "width": "auto",
                    "display": "block",
                    "objectFit": "cover"
                })))
            else:
                cells.append(html.Td(str(dataframe.iloc[i][col])))
        rows.append(html.Tr(cells))

    return html.Table(
        [
            html.Thead(html.Tr([html.Th(c) for c in cols])),
            html.Tbody(rows)
        ],
        className="sticky-header-table",
        style={"width": "100%"}
    )

app.layout = html.Div([
    html.Div([
        html.Div(generate_table(df), style={
            "flex": "1",
            "paddingRight": "16px",
            "overflowY": "auto",
            "height": "100%",
            "minHeight": 0
        }),
        html.Div([
            dcc.Graph(
                id="map",
                figure=fig,
                style={"flex": "1", "minHeight": 0},
                config={"scrollZoom": False}
            ),
            html.Div([
                html.Img(id="preview", style={
                    "maxWidth": "100%",
                    "maxHeight": "400px",
                    "borderRadius": "6px",
                    "display": "block"
                })
            ])
        ], style={"flex": "1", "display": "flex", "flexDirection": "column", "minHeight": 0})
    ], style={
        "display": "flex",
        "gap": "16px",
        "height": "80vh",
        "minHeight": 0
    })
])

@app.callback(
    Output("preview", "src"),
    Input("map", "clickData")
)
def show_image(clickData):
    if not clickData:
        return None
    point = clickData["points"][0]
    idx = point["pointIndex"]
    img_path = df.iloc[idx]["image_path"]
    return str(img_path)

IMAGE_DIR = os.path.abspath("img")
@app.server.route("/img/<path:filename>")
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
from dash import Dash, html
import pandas as pd
import os

df = pd.read_csv('B:/SeniorDesign/Cuda2Fly/CarData/speeders.csv')


def generate_table(dataframe, max_rows=15):
    cols = list(dataframe.columns)
    rows = []
    for i in range(min(len(dataframe), max_rows)):
        cells = []
        for j, col in enumerate(cols):
            if j == 3:  # 3rd column -> image
                fname = os.path.basename(str(dataframe.iloc[i, j]))
                # OPTION A: if you set up a Flask route at /img/<filename>
                cells.append(html.Td(html.Img(src=f"B:/SeniorDesign/Cuda2Fly/CarData/Pictures/{fname}", style={"height": "100px"})))
                # OPTION B: if you copied images to ./assets/images/
                # cells.append(html.Td(html.Img(src=f"/assets/images/{fname}", style={"height": "100px"})))
                break
            else:
                cells.append(html.Td(str(dataframe.iloc[i, j])))
        rows.append(html.Tr(cells))

    return html.Table([
        html.Thead(html.Tr([html.Th(c) for c in cols])),
        html.Tbody(rows)
    ])


app = Dash()

app.layout = html.Div([
    html.H4(children='Waterview Pkwy & Synergy Park Blvd'),
    generate_table(df)
])

if __name__ == '__main__':
    app.run(debug=True)
from dash import Dash, html
import pandas as pd
import os

df = pd.read_csv('speeders.csv')


def generate_table(dataframe, max_rows=15):
    cols = list(dataframe.columns)
    rows = []
    for i in range(min(len(dataframe), max_rows)):
        cells = []
        for j, col in enumerate(cols):
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
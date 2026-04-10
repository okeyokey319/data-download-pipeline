import pandas as pd
from dash import Dash, Input, Output, dash_table, html
from sqlalchemy import create_engine

# загружаем данные из базы
def load_data():
    engine = create_engine("postgresql://postgres:postgres@localhost:5433/countries")
    df = pd.read_sql("SELECT * FROM countries", con=engine)
    return df

df = load_data()

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Countries Dashboard"),
    html.Div([
        dash_table.DataTable(
            id="table",
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict("records"),
            sort_action="native",
            row_selectable="single",
            selected_rows=[0],
            page_size=20,
        )
    ]),
    html.Div([
        html.H3(id="country-name"),
        html.Img(id="flag-img", style={"width": "200px"}),
    ])
])

# обновляем флаг когда выбрана строка
@app.callback(
    Output("flag-img", "src"),
    Output("country-name", "children"),
    Input("table", "selected_rows"),
)
def update_flag(selected_rows):
    if not selected_rows:
        return "", ""

    row = df.iloc[selected_rows[0]]
    return row["flag_png"], row["name"]


if __name__ == "__main__":
    app.run(debug=True)

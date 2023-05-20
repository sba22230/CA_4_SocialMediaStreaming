import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

import pandas
from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.output_table("table"),
)


def server(input, output, session):
    @output
    @render.table
    def table():
        infile = Path(__file__).parent.parent / "Data/TweetInfo.csv"
        df = pandas.read_csv(infile)
        df = df.sample(10)
        # Use the DataFrame's to_html() function to convert it to an HTML table, and
        # then wrap with ui.HTML() so Shiny knows to treat it as raw HTML.
        return df


app = App(app_ui, server, debug=True)

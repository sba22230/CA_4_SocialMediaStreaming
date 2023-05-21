from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shiny.plotutils import brushed_points, near_points

twtsent = pd.read_csv(Path(__file__).parent.parent / "Data/TweetInfo.csv")


app_ui = ui.page_fluid(
    ui.h2("Tweet Sentiment Analysis"),
    ui.row(
        ui.column(
            3,
            ui.input_select(
                "time_range",
                "Select Time Range to forecast",
                choices=["no forecast", "1 week", "1 month", "3 months"],
            ),
        ),
        ui.column(
            2,
            ui.output_text_verbatim("tweetcount"),
        ),
        ui.column(
            2,
            ui.output_text_verbatim("tweetcountLkrt"),
        ),
    ),
    ui.row(
        ui.column(
            6,
            ui.output_plot("plot1", click=True, dblclick=True, hover=True, brush=True),
        ),
    ),
)


def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.text()
    def tweetcount():
        count = len(twtsent["id"])
        return str("Number of tweets: " + str(count))

    @output
    @render.text()
    def tweetcountLkrt():
        langCounts = twtsent["LikertScale"].value_counts()
        langCounts = str("Number of tweets by Likert Scale: \n" + str(langCounts))
        return langCounts

    @output
    @render.plot(alt="A scatterplot")
    def plot1():
        if input.plot_type() == "matplotlib":
            fig, ax = plt.subplots()
            plt.title("Good old twtsent")
            ax.scatter(twtsent["wkofYr"], twtsent["txbSentiment"])
            return fig

    # @output
    # @render.text()
    # def click_info():
    #     return "click:\n" + json.dumps(input.plot1_click(), indent=2)

    # @output
    # @render.text()
    # def dblclick_info():
    #     return "dblclick:\n" + json.dumps(input.plot1_dblclick(), indent=2)

    # @output
    # @render.text()
    # def hover_info():
    #     return "hover:\n" + json.dumps(input.plot1_hover(), indent=2)

    # @output
    # @render.text()
    # def brush_info():
    #     return "brush:\n" + json.dumps(input.plot1_brush(), indent=2)


app = App(app_ui, server, debug=True)

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shiny.plotutils import brushed_points, near_points

twtsent = pd.read_csv(Path(__file__).parent.parent / "Data/TweetInfo.csv")
dfSent = pd.read_csv(Path(__file__).parent.parent / "Data/dfSentiment.csv")
start_date = "2021-01-31"
end_date = "2022-11-27"
mask = (dfSent["date"] >= start_date) & (dfSent["date"] <= end_date)
df_original = dfSent.loc[mask]

end_date = "2022-12-11"
mask = (dfSent["date"] >= start_date) & (dfSent["date"] <= end_date)
df_1week = dfSent.loc[mask]

end_date = "2022-12-28"
mask = (dfSent["date"] >= start_date) & (dfSent["date"] <= end_date)
df_1month = dfSent.loc[mask]


app_ui = ui.page_fluid(
    ui.panel_title("Tweet Sentiment Analysis"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select(
                "time_range",
                "Select Time Range to forecast",
                choices=["no forecast", "1 week", "1 month", "3 months"],
            ),
        ),
        ui.panel_main(
            ui.row(
                ui.column(
                    6,
                    ui.output_text_verbatim("tweetcount"),
                ),
                ui.column(
                    6,
                    ui.output_text_verbatim("tweetcountLkrt"),
                ),
            ),
            ui.row(
                ui.column(
                    6,
                    ui.output_plot(
                        "plot1", click=True, dblclick=True, hover=True, brush=True
                    ),
                ),
                ui.column(
                    6,
                    ui.output_ui("data_table"),
                ),
            ),
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
    @render.plot(alt="A lin chart")
    def plot1():
        fig, ax = plt.subplots()
        plt.title("Sentiment of Tweets over Time")
        plt.plot(
            dfSent["date"], dfSent["txbSentiment"], color="black", label="Sentiment"
        )
        # ax.scatter (twtsent["wkofYr"], twtsent["txbSentiment"])
        return fig

    @output
    @render.table()
    def data_table():
        return dfSent[["date", "txbSentiment"]]
        # x = input.time_range
        # if x == "no forecast":
        #     return df_original[["date", "txbSentiment"]]
        # elif x == "1 week":
        #     return df_1week[["date", "txbSentiment"]]
        # elif x == "1 month":
        #     return df_1month[["date", "txbSentiment"]]
        # elif x == "3 months":
        #     return dfSent[["date", "txbSentiment"]]
        # else:
        #     return df_original[["date", "txbSentiment"]]


app = App(app_ui, server, debug=True)

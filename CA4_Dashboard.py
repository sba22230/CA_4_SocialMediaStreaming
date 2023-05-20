import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_elements import elements, mui, html

st.title("Twitter Sentiment Analysis for the word rugby")
st.markdown(
    "The dashboard will help a researcher to get to know \
more about the given datasets and it's output"
)
data = pd.read_csv("Data/TweetInfo.csv")
with elements("dashboard"):

    # You can create a draggable and resizable dashboard using
    # any element available in Streamlit Elements.

    from streamlit_elements import dashboard

    # First, build a default layout for every element you want to include in your dashboard

    layout = [
        # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
        dashboard.Item("first_item", 0, 0, 1, 1),
        dashboard.Item("second_item", 1, 0, 1, 1, isDraggable=True, moved=True),
        dashboard.Item("third_item", 2, 0, 1, 1, isResizable=True),
    ]

    # Next, create a dashboard layout using the 'with' syntax. It takes the layout
    # as first parameter, plus additional properties you can find in the GitHub links below.

    with dashboard.Grid(layout):
        mui.Paper("Tweet Count", key="first_item", )
        mui.Paper("Count Per Lang", key="second_item")
        mui.Paper("Count Per Loc", key="third_item")

    # If you want to retrieve updated layout values as the user move or resize dashboard items,
    # you can pass a callback to the onLayoutChange event parameter.

    def handle_layout_change(updated_layout):
        # You can save the layout in a file, or do anything you want with it.
        # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
        print(updated_layout)

    """ with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
        mui.Paper("First item", key="first_item")
        mui.Paper("Second item (cannot drag)", key="second_item")
        mui.Paper("Third item (cannot resize)", key="third_item") """

st.sidebar.title("Select Visual Charts")
st.sidebar.markdown("Select the Charts/Plots accordingly:")



chart_visual = st.sidebar.selectbox(
    "Select Charts/Plot type", ("Line Chart", "Bar Chart", "Bubble Chart")
)

st.sidebar.checkbox("Show Analysis by Sentiment", True, key=1)
selected_status = st.sidebar.selectbox(
    "Select Sentiment",
    options=["TextBlob Sentiment", "Vader Sentiment", "Combined Sentiment"],
)

fig = go.Figure()

if chart_visual == "Line Chart":
    if selected_status == "TextBlob Sentiment":
        fig.add_trace(
            go.Scatter(
                x=data.date,
                y=data.txbSentiment,
                mode="lines",
                name="txbSentiment",
            )
        )
    if selected_status == "Vader Sentiment":
        fig.add_trace(
            go.Scatter(x=data.date, y=data.vaderSentiment, mode="lines", name="vaderSentiment")
        )
    if selected_status == "Combined Sentiment":
        fig.add_trace(
            go.Scatter(
                x=data.date,
                y=data.CombinedSentiment,
                mode="lines",
                name="CombinedSentiment",
            )
        )
    

elif chart_visual == "Bar Chart":
    if selected_status == "TextBlob Sentiment":
        fig.add_trace(go.Bar(x=data.date, y=data.txbSentiment, name="txbSentiment"))
    if selected_status == "Vader Sentiment":
        fig.add_trace(go.Bar(x=data.date, y=data.vaderSentiment, name="vaderSentiment"))
    if selected_status == "Combined Sentiment":
        fig.add_trace(
            go.Bar(x=data.date, y=data.CombinedSentiment, name="CombinedSentiment")
        )

elif chart_visual == "Bubble Chart":
    if selected_status == "TextBlob Sentiment":
        fig.add_trace(
            go.Scatter(
                x=data.date,
                y=data.txbSentiment,
                mode="markers",
                marker_size=[40, 60, 80, 60, 40, 50],
                name="txbSentiment",
            )
        )

    if selected_status == "Vader Sentiment":
        fig.add_trace(
            go.Scatter(
                x=data.date,
                y=data.vaderSentiment,
                mode="markers",
                marker_size=[40, 60, 80, 60, 40, 50],
                name="vaderSentiment",
            )
        )

    if selected_status == "Combined Sentiment":
        fig.add_trace(
            go.Scatter(
                x=data.date,
                y=data.CombinedSentiment,
                mode="markers",
                marker_size=[40, 60, 80, 60, 40, 50],
                name="CombinedSentiment",
            )
        )
    

st.plotly_chart(fig, use_container_width=True)

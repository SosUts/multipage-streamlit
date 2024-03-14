import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# ファイルをアップロードするボタンを作る
uploaded_file = st.file_uploader("Upload a file")
if uploaded_file is not None:
    # ファイルがアップロードされた場合の処理を記述する
    # 例えば、アップロードされたファイルをデータフレームとして読み込むなど
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded file:")
    st.write(df)
    # colの中でstringのものを抽出する
    string_columns = df.select_dtypes(include=["object"]).columns

    col1, col2 = st.columns([1, 1])
    # x軸、y軸として使いたい列を選択するボタンを作る。widthをdefaultの50%にする
    x = col1.selectbox(
        "X axis",
        df.columns,
    )
    y = col2.selectbox(
        "Y axis",
        df.columns,
    )
    hue = col1.selectbox(
        "Hue",
        string_columns,
    )
    ploty_type = col2.selectbox(
        "Plot type",
        ["scatter", "line", "bar"],
    )

    # create a input box to input the title of the plot
    title = col1.text_input(
        "Title",
        "Title",
    )
    # create a input box to input the x-axis label of the plot
    x_label = col1.text_input(
        "X-axis label",
        "X-axis",
    )
    # create a input box to input the y-axis label of the plot
    y_label = col2.text_input(
        "Y-axis label",
        "Y-axis",
    )

    if ploty_type == "scatter":
        fig = px.scatter(
            df, x=x, y=y, color=hue, title=title, labels={x: x_label, y: y_label}
        )
    elif ploty_type == "line":
        fig = px.line(
            df, x=x, y=y, color=hue, title=title, labels={x: x_label, y: y_label}
        )
    elif ploty_type == "bar":
        # calculate the mean of y for each x value
        mean_y = df.groupby("class")[y].mean().reset_index()
        # calculate the coefficients of variation
        cv = (
            100 * df.groupby("class")[y].std() / df.groupby("class")[y].mean()
        ).reset_index()
        # mean_y = pd.concat([mean_y, cv], axis=1)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        ylim1 = col1.text_input("ylim of left axis", mean_y[y].max() * 1.1)
        trace1 = go.Bar(
            x=mean_y["class"],
            y=mean_y[y],
            # error_y=cv,
            name=y,
            # text=cv[y],
            # marker=dict(color=hue),
        )
        fig.add_trace(trace1)
        # create a slider to specify the ylim
        ylim2 = col1.text_input("ylim of right axis", cv[y].max() * 1.1)
        # plot cv as a scatter plot in the same fig.
        trace2 = go.Scatter(
            x=cv["class"],
            y=cv[y],
            name="%CV",
            mode="markers",
        )
        fig.add_trace(trace=trace2, secondary_y=True)
        # show y-axis of cv on the right. y-axis of mean_y on the left
        fig.update_layout(
            yaxis1=dict(side="left", range=[0, ylim1]),
            yaxis2=dict(overlaying="y", side="right", range=[0, ylim2]),
        )

    # # # create a plot with the selected columns
    st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import ast
import os

st.set_page_config(layout="wide")

DATA_OUT = os.path.join("data", "output")
DATA_FILE = os.path.join(DATA_OUT, "race_analysis_full.csv")

st.title("香港賽馬會｜官方分段步速分析系統")

if not os.path.exists(DATA_FILE):
    st.error("未有分析資料，請先執行資料抓取與分析程序。")
    st.stop()

df = pd.read_csv(DATA_FILE)

race_no = st.sidebar.selectbox(
    "選擇場次",
    sorted(df["race_no"].unique())
)

race_df = df[df["race_no"] == race_no]

st.subheader(f"第 {race_no} 場｜全馬匹官方分段表")

st.dataframe(race_df, use_container_width=True)

st.subheader("官方每 200 / 400 米分段步速差異圖")

for _, row in race_df.iterrows():
    horse = row["horse_name"]
    diffs = ast.literal_eval(row["sectional_diff"])

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.bar(range(1, len(diffs) + 1), diffs)
    ax.axhline(0, linewidth=1)
    ax.set_title(f"{horse}｜每段步速差異（秒）")
    ax.set_xlabel("官方分段")
    ax.set_ylabel("與標準差異（秒）")

    st.pyplot(fig)

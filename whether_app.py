# weather_app.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.title("天気・気温・湿度予測アプリ")

# ユーザー入力
target_date = st.date_input("予測したい日付", value=datetime.today() + timedelta(days=1))

# ダミー予測（本来はモデルで予測）
np.random.seed(target_date.day)
temp = np.random.normal(25, 5)
humidity = np.random.uniform(40, 90)
weather = np.random.choice(["晴れ", "曇り", "雨"])

# 結果表示
st.subheader(f"{target_date.strftime('%Y/%m/%d')} の予測結果")
st.metric("気温 (℃)", f"{temp:.1f}")
st.metric("湿度 (%)", f"{humidity:.0f}")
st.metric("天気", weather)

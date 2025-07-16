import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# データ読み込み
df = pd.read_csv("weather.csv")
df.dropna(inplace=True)

# 日付変換（オプション）
df["年月日"] = pd.to_datetime(df["年月日"])

# ラベルエンコード（天気を数値化）
le = LabelEncoder()
df["天気ラベル"] = le.fit_transform(df["天気概況(昼：06時〜18時)"])

# 学習データ
X = df[["平均気温(℃)", "平均湿度(％)"]]
y = df["天気ラベル"]

# 訓練・テスト分割
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# モデル作成
model = RandomForestClassifier()
model.fit(X_train, y_train)

# StreamlitアプリUI
st.title("🌤 天気予測アプリ")
st.write("平均気温と湿度から、予測される天気を表示します。")

temp = st.slider("平均気温 (℃)", -10.0, 40.0, 20.0, 0.1)
humid = st.slider("平均湿度 (%)", 0, 100, 60, 1)

if st.button("予測する"):
    input_data = pd.DataFrame([[temp, humid]], columns=["平均気温(℃)", "平均湿度(％)"])
    prediction = model.predict(input_data)
    pred_label = le.inverse_transform(prediction)
    st.success(f"予測された天気: 🌤 {pred_label[0]}")

import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import os

# --- ログイン用データ（簡易） ---
USERS = {
    "admin": "password123",
    "guest": "weather2025"
}

# --- セッションステートでログイン管理 ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🌤️ 天気予測アプリ - ログイン")
    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")
    if st.button("ログイン"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("ユーザー名またはパスワードが間違っています。")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""

def main_app():
    st.title("🌦️ 天気予測アプリ")
    st.sidebar.success(f"ログイン中：{st.session_state.username}")
    if st.sidebar.button("ログアウト"):
        logout()
        st.experimental_rerun()

    # --- データ読み込み ---
    try:
        df = pd.read_csv("data.csv")
    except Exception as e:
        st.error(f"データの読み込みに失敗しました: {e}")
        return

    st.subheader("📄 データプレビュー")
    st.dataframe(df.head())

    # --- 必要な列だけ抽出 ---
    try:
        df = df[["平均気温(℃)", "平均湿度(％)", "天気概況(昼：06時〜18時)"]].dropna()
    except KeyError:
        st.error("必要な列（平均気温, 平均湿度, 天気概況(昼)）が見つかりません")
        return

    # --- 特徴量・ラベル ---
    X = df[["平均気温(℃)", "平均湿度(％)"]]
    y = df["天気概況(昼：06時〜18時)"]

    # --- ラベルエンコード ---
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # --- 学習 ---
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    st.subheader("🔍 天気を予測する")

    temp = st.slider("平均気温 (℃)", float(X["平均気温(℃)"].min()), float(X["平均気温(℃)"].max()), 20.0)
    humid = st.slider("平均湿度 (%)", float(X["平均湿度(％)"].min()), float(X["平均湿度(％)"].max()), 60.0)

    if st.button("予測実行"):
        input_data = pd.DataFrame([[temp, humid]], columns=["平均気温(℃)", "平均湿度(％)"])
        pred = model.predict(input_data)
        result = le.inverse_transform(pred)[0]
        st.success(f"☁️ 予測された天気（昼間）：**{result}**")

# --- 実行部 ---
if st.session_state.logged_in:
    main_app()
else:
    login()

import streamlit as st
import pandas as pd
import bcrypt
import yaml
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

USERS_FILE = "users.yaml"

# --- 初期化 ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- ユーザー読み込み ---
def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            yaml.dump({"users": {}}, f)
    with open(USERS_FILE, "r") as f:
        return yaml.safe_load(f)

def save_users(users_data):
    with open(USERS_FILE, "w") as f:
        yaml.safe_dump(users_data, f)

# --- ユーザー追加 ---
def add_user(username, password):
    users = load_users()
    if username in users["users"]:
        return False
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users["users"][username] = {"password": hashed}
    save_users(users)
    return True

# --- ユーザー認証 ---
def check_login(username, password):
    users = load_users()
    if username in users["users"]:
        hashed_pw = users["users"][username]["password"].encode()
        return bcrypt.checkpw(password.encode(), hashed_pw)
    return False

# --- ユーザー削除 ---
def delete_user(username):
    users = load_users()
    if username in users["users"]:
        del users["users"][username]
        save_users(users)
        return True
    return False

# --- ログイン画面 ---
def login_screen():
    st.title("🌤️ 天気予測アプリ")
    menu = st.sidebar.selectbox("メニューを選択", ["ログイン", "新規登録"])

    if menu == "ログイン":
        st.subheader("🔐 ログイン")
        username = st.text_input("ユーザー名")
        password = st.text_input("パスワード", type="password")
        if st.button("ログイン"):
            if check_login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"ようこそ、{username} さん！")
                st.experimental_rerun()
            else:
                st.error("ユーザー名またはパスワードが違います。")

    elif menu == "新規登録":
        st.subheader("📝 新規登録")
        new_user = st.text_input("新しいユーザー名")
        new_pass = st.text_input("新しいパスワード", type="password")
        if st.button("登録する"):
            if add_user(new_user, new_pass):
                st.success("登録が完了しました！ログインしてください。")
            else:
                st.error("すでに存在するユーザー名です。")

# --- メインアプリ ---
def main_app():
    st.title("🌦️ 天気予測")
    st.sidebar.success(f"ログイン中：{st.session_state.username}")
    if st.sidebar.button("ログアウト"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()

    if st.sidebar.button("このアカウントを削除"):
        if delete_user(st.session_state.username):
            st.success("アカウントを削除しました。")
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.experimental_rerun()
        else:
            st.error("削除に失敗しました。")

    # --- CSV読み込み ---
    try:
        df = pd.read_csv("data.csv")
    except Exception as e:
        st.error(f"CSVの読み込みに失敗しました: {e}")
        return

    try:
        df = df[["平均気温(℃)", "平均湿度(％)", "天気概況(昼：06時〜18時)"]].dropna()
    except KeyError:
        st.error("必要な列が存在しません。")
        return

    st.subheader("📊 データプレビュー")
    st.dataframe(df.head())

    X = df[["平均気温(℃)", "平均湿度(％)"]]
    y = df["天気概況(昼：06時〜18時)"]
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    model = RandomForestClassifier()
    model.fit(X, y_encoded)

    st.subheader("🌡️ 天気を予測")
    temp = st.slider("平均気温(℃)", float(X.min()[0]), float(X.max()[0]), 20.0)
    humid = st.slider("平均湿度(％)", float(X.min()[1]), float(X.max()[1]), 60.0)

    if st.button("予測する"):
        pred = model.predict([[temp, humid]])
        result = le.inverse_transform(pred)[0]
        st.success(f"予測された天気（昼）：**{result}**")

# --- 実行 ---
if st.session_state.logged_in:
    main_app()
else:
    login_screen()

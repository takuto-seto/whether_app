import streamlit as st
import pandas as pd

st.title("天気予測アプリ（CSVアップロード版）")

uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

if uploaded_file is not None:
    # CSV読み込み（ヘッダー調整は適宜）
    df = pd.read_csv(uploaded_file, header=0)
    st.write("アップロードされたデータ:")
    st.write(df.head())

    # ここでは例として「平均気温(℃)」列があると仮定
    if "平均気温(℃)" in df.columns:
        # 簡単な予測ルール：平均気温が25度以上なら「晴れ」、そうでなければ「曇り」
        def simple_weather_predict(temp):
            if temp >= 25:
                return "晴れ"
            else:
                return "曇り"

        df["予測天気"] = df["平均気温(℃)"].apply(simple_weather_predict)

        st.write("予測結果:")
        st.write(df[["平均気温(℃)", "予測天気"]])
    else:
        st.warning("データに「平均気温(℃)」列がありません。予測できません。")

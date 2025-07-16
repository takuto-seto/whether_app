import streamlit as st
import pandas as pd
import chardet

st.title("天気予測アプリ（CSVアップロード版）")

uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

if uploaded_file is not None:
    # 文字コード推定
    rawdata = uploaded_file.read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']
    st.write(f"推定エンコーディング: {encoding}")

    uploaded_file.seek(0)
    try:
        df = pd.read_csv(uploaded_file, encoding=encoding)
    except Exception as e:
        st.error(f"CSV読み込みエラー: {e}")
        st.stop()

    st.write("アップロードされたデータ:")
    st.write(df.head())

    if "平均気温(℃)" in df.columns:
        def simple_weather_predict(temp):
            if temp >= 25:
                return "晴れ"
            else:
                return "曇り"

        df["予測天気"] = df["平均気温(℃)"].apply(simple_weather_predict)
        st.write("予測結果:")
        st.write(df[["平均気温(℃)", "予測天気"]])
    else:
        st.warning("「平均気温(℃)」列がありません。予測できません。")

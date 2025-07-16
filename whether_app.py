import streamlit as st
import pandas as pd
import io

st.title("🌤️ 天気予測アプリ（CSVアップロード版）")
st.write("""
アップロードしたCSVファイルの「平均気温(℃)」を使って簡単に天気を予測します。  
予測は単純なルールベースですので、モデルを変えたい場合はご相談ください。
""")

uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

def simple_weather_predict(temp):
    if temp >= 25:
        return "☀️ 晴れ"
    elif temp >= 15:
        return "⛅ 曇り"
    else:
        return "🌧️ 雨"

if uploaded_file is not None:
    bytes_data = uploaded_file.read()
    data = io.BytesIO(bytes_data)
    encoding_list = ['utf-8', 'shift_jis', 'cp932', 'latin1']

    for encoding in encoding_list:
        try:
            data.seek(0)
            df = pd.read_csv(data, encoding=encoding)
            st.success(f"ファイルを {encoding} エンコードで読み込みました。")
            break
        except UnicodeDecodeError:
            pass
    else:
        st.error("全てのエンコーディングでの読み込みに失敗しました。")
        st.stop()

    st.subheader("アップロードされたデータプレビュー")
    st.dataframe(df.head(), use_container_width=True)

    if "平均気温(℃)" in df.columns:
        df["予測天気"] = df["平均気温(℃)"].apply(simple_weather_predict)

        st.subheader("天気予測結果")
        # カラフルに表示するためのスタイル関数
        def highlight_weather(val):
            color = {
                "☀️ 晴れ": "background-color: #FFF59D;",  # 黄色
                "⛅ 曇り": "background-color: #90CAF9;",  # 水色
                "🌧️ 雨": "background-color: #A5D6A7;",  # 緑
            }
            return color.get(val, "")

        st.dataframe(
            df[["平均気温(℃)", "予測天気"]].style.applymap(highlight_weather),
            use_container_width=True
        )
    else:
        st.warning("データに「平均気温(℃)」列がありません。予測できません。")

import streamlit as st
import pandas as pd
import io

st.title("天気予測アプリ（天気概況列から予測）")

uploaded_file = st.file_uploader("CSVファイルをアップロード", type=["csv"])

def weather_predict_from_text(text):
    if pd.isna(text):
        return "不明"
    text = text.lower()
    if any(word in text for word in ["晴", "sunny", "clear"]):
        return "☀️ 晴れ"
    elif any(word in text for word in ["曇", "cloud", "cloudy"]):
        return "⛅ 曇り"
    elif any(word in text for word in ["雨", "rain", "shower", "storm"]):
        return "🌧️ 雨"
    elif any(word in text for word in ["雪", "snow"]):
        return "❄️ 雪"
    else:
        return "不明"

if uploaded_file is not None:
    bytes_data = uploaded_file.read()
    data = io.BytesIO(bytes_data)
    encoding_list = ['utf-8', 'shift_jis', 'cp932', 'latin1']

    for encoding in encoding_list:
        try:
            data.seek(0)
            df = pd.read_csv(data, encoding=encoding)
            st.success(f"ファイルを {encoding} で読み込みました。")
            break
        except Exception:
            pass
    else:
        st.error("読み込みに失敗しました。")
        st.stop()

    st.subheader("データプレビュー")
    st.dataframe(df.head(), use_container_width=True)

    target_col = None
    # 天気の列を自動検出（名前に「天気」や「概況」が含まれている列を探す）
    for col in df.columns:
        if "天気" in col or "概況" in col:
            target_col = col
            break

    if target_col is None:
        st.warning("天気概況を示す列が見つかりません。")
        st.stop()

    st.write(f"予測に使用する列：{target_col}")

    df["予測天気"] = df[target_col].apply(weather_predict_from_text)

    st.subheader("予測結果")
    st.dataframe(df[[target_col, "予測天気"]], use_container_width=True)

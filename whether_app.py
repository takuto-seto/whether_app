import streamlit as st
import pandas as pd
import io

st.title("三行目の値を列名として天気予測アプリ")

uploaded_file = st.file_uploader("CSVファイルをアップロード", type=["csv"])

def weather_predict_from_text(text):
    if pd.isna(text):
        return "不明"
    text = str(text).lower()
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
            # ヘッダーは0のまま読み込み、3行目はインデックス2なのでデータとして読む
            df = pd.read_csv(data, encoding=encoding, header=0)
            st.success(f"ファイルを {encoding} で読み込みました。")
            break
        except Exception:
            pass
    else:
        st.error("読み込みに失敗しました。")
        st.stop()

    st.subheader("元データプレビュー")
    st.dataframe(df.head(), use_container_width=True)

    # 3行目の値を新しい列名として取得
    # CSV読み込み時、index=2が三行目
    if len(df) < 3:
        st.error("データの行数が3行未満です。")
        st.stop()

    new_columns = df.iloc[2].tolist()  # 3行目の値をリストで取得
    st.write(f"3行目の値（新しい列名候補）: {new_columns}")

    # 新しい列名を設定（元データに上書きしないためコピー）
    df2 = df.copy()

    # 元の列名数と3行目の要素数が違う場合に備えて調整
    if len(new_columns) != len(df.columns):
        st.error("3行目の値の数と列数が一致しません。")
        st.stop()

    df2.columns = new_columns

    st.subheader("新しい列名を設定したデータプレビュー")
    st.dataframe(df2.head(), use_container_width=True)

    # 天気予測の対象となる列（3行目の値に天気を示す文字が含まれている列）を探す
    target_col = None
    for col in df2.columns:
        if col is not None and ("天気" in str(col) or "概況" in str(col)):
            target_col = col
            break

    if target_col is None:
        st.warning("3行目の値から天気を示す列が見つかりません。")
        st.stop()

    st.info(f"▶️ 予測に使用する列：**{target_col}**")

    # 天気予測実行（元のdf2のデータは3行目が列名なので4行目以降が本当のデータ）
    df2["予測天気"] = df2[target_col].apply(weather_predict_from_text)

    st.subheader("予測結果")
st.dataframe(df2[[target_col, "予測天気"]], use_container_width=True)


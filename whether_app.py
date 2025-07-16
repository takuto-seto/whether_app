import streamlit as st
import pandas as pd
import io

st.title("天気予測アプリ（CSVアップロード版）")

uploaded_file = st.file_uploader("CSVファイルをアップロード", type=["csv"])

if uploaded_file is not None:
    # ファイルのバイトデータを読み込む
    bytes_data = uploaded_file.read()

    # バイトデータをBytesIOでラップしてpandasに渡す
    data = io.BytesIO(bytes_data)

    # 文字コードをいくつか試して読み込み
    encoding_list = ['utf-8', 'shift_jis', 'cp932', 'latin1']

    for encoding in encoding_list:
        try:
            data.seek(0)  # 読み込みポインタを先頭に戻す
            df = pd.read_csv(data, encoding=encoding)
            st.success(f"成功: {encoding} で読み込みました")
            st.write(df.head())
            break
        except UnicodeDecodeError:
            st.warning(f"{encoding} での読み込みに失敗しました")
        except Exception as e:
            st.error(f"その他のエラー: {e}")
            break
    else:
        st.error("全てのエンコーディングでの読み込みに失敗しました。ファイルの文字コードをご確認ください。")

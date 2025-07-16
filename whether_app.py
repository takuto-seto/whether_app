import streamlit as st
import pandas as pd
import io

uploaded_file = st.file_uploader("CSVファイルをアップロード", type="csv")

if uploaded_file is not None:
    # バイト列を読み込む（ストリームのポインタ問題を回避）
    bytes_data = uploaded_file.read()

    # BytesIOオブジェクトに変換
    data = io.BytesIO(bytes_data)

    # 文字コードを推測（任意）
    # import chardet
    # result = chardet.detect(bytes_data)
    # encoding = result['encoding']

    # pandasで読み込み（encodingは必要に応じて指定）
    try:
        df = pd.read_csv(data, encoding='utf-8')  # utf-8以外なら適宜変更
        st.write("読み込み成功！")
        st.write(df.head())
    except UnicodeDecodeError:
        # 失敗したら別エンコーディングで試す
        data.seek(0)
        df = pd.read_csv(data, encoding='shift_jis')
        st.write("Shift_JISで読み込み成功！")
        st.write(df.head())
    except Exception as e:
        st.error(f"読み込みエラー: {e}")

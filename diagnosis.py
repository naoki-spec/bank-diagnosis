import streamlit as st
import pandas as pd
import requests
import re
import io

# Google Drive上のCSVダウンロードURL（共有設定「全員が閲覧可能」済み）
CSV_URL = "https://drive.google.com/uc?export=download&id=1bHt7FZ2YfTDsxMyC2EZI36fzTbcWdW1f"

st.set_page_config(page_title="銀行診断フォーム", layout="centered")
st.markdown("<h2 style='text-align:center; color:#005792;'>🏦 銀行診断フォーム</h2>", unsafe_allow_html=True)

# 入力項目
income = st.number_input("給与年収（万円）", min_value=0, step=100, format="%d") * 10000
assets = st.number_input("金融資産（万円）", min_value=0, step=100, format="%d") * 10000
loan = st.number_input("既存借入金額（万円）", min_value=0, step=100, format="%d") * 10000

net_assets = assets - loan
st.markdown(
    f"<p style='font-weight:bold;'>純資産（自動計算）：<span style='color:#005792;'>{int(net_assets):,}</span> 円</p>",
    unsafe_allow_html=True
)

# 診断ボタン
if st.button("診断スタート"):
    try:
        # CSV取得＆DataFrame化
        res = requests.get(CSV_URL)
        content = res.content.decode('utf-8')
        df = pd.read_csv(io.StringIO(content))

        matched = []
        excluded = []

        for _, row in df.iterrows():
            name = str(row.get("name", "")).strip()
            url = str(row.get("url", "")).strip()

            # 金額の文字列を正規化（¥, カンマ, 空白削除）
            min_income = int(re.sub(r"\D", "", str(row.get("min_income", "0"))))
            min_net_assets = int(re.sub(r"\D", "", str(row.get("min_net_assets", "0"))))

            # 判定ロジック
            if income >= min_income and net_assets >= min_net_assets:
                matched.append((name, url))
            else:
                reasons = []
                if income < min_income:
                    reasons.append("給与年収が不足")
                if net_assets < min_net_assets:
                    reasons.append("純資産が不足")
                excluded.append(f"{name}（理由：{' / '.join(reasons)}）")

        # 表示処理
        if matched:
            st.markdown("### ✅ 該当する銀行")
            for name, url in matched:
                st.markdown(f"✅ <a href='{url}' target='_blank'><strong>{name}</strong></a>", unsafe_allow_html=True)
        else:
            st.info("条件に合致する銀行はありません。")

        if excluded:
            st.markdown("### ❌ 条件に合わなかった銀行")
            for msg in excluded:
                st.markdown(f"❌ {msg}")

    except Exception as e:
        st.error("CSVの読み込みに失敗しました。URLや形式をご確認ください。")
        st.exception(e)
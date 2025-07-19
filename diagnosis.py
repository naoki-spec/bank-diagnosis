import streamlit as st
import csv

st.set_page_config(page_title="銀行診断フォーム", page_icon="🏦", layout="centered")

# 💅 デザイン
st.markdown("""
    <style>
        body { background-color: #ffffff; }
        h1 { color: #003366; font-size: 30px; }
        .stButton>button {
            background-color: #005792;
            color: white;
            border-radius: 6px;
            padding: 10px 20px;
        }
        .matched-card {
            background-color: #e3f2fd;
            border-left: 6px solid #1976d2;
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 6px;
        }
        .excluded-card {
            background-color: #fce4ec;
            border-left: 6px solid #d81b60;
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 6px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🏦 銀行診断フォーム</h1>", unsafe_allow_html=True)

# 📋 入力欄
income_input = st.number_input("給与年収（万円）", min_value=0, step=100)
financial_input = st.number_input("金融資産（万円）", min_value=0, step=100)
loan_input = st.number_input("既存借入金額（万円）", min_value=0, step=100)

# 💰 自動計算（円単位）
income = income_input * 10000
financial_assets = financial_input * 10000
loan_amount = loan_input * 10000
net_assets = financial_assets - loan_amount

# 👇 純資産表示（入力欄の下）
st.markdown(f"**純資産（金融資産 − 既存借入金額）:** {net_assets:,.0f} 円")

# 🚀 診断実行
if st.button("診断スタート"):
    matched_banks = []
    excluded_banks = []

    def parse_amount(amount_str):
        try:
            return int(amount_str.replace("¥", "").replace(",", "").strip())
        except:
            return 0

    try:
        with open("Book1.csv", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row["name"]
                income_required = parse_amount(row["min_income"])
                assets_required = parse_amount(row["min_net_assets"])
                bank_url = row.get("url", "").strip()

                if income >= income_required and net_assets >= assets_required:
                    matched_banks.append((name, bank_url))
                else:
                    reasons = []
                    if income < income_required:
                        reasons.append("給与年収が足りない")
                    if net_assets < assets_required:
                        reasons.append("純資産が足りない")
                    excluded_banks.append(f"{name}（理由：{', '.join(reasons)}）")
    except FileNotFoundError:
        st.error("⚠️ Book1.csv が見つかりません。同じフォルダーに配置してください。")

    # 🏁 結果表示
    st.markdown("### ✅ 該当する銀行")
    if matched_banks:
        for bank, link in matched_banks:
            if link:
                st.markdown(f"<div class='matched-card'>✅ <a href='{link}' target='_blank'><strong>{bank}</strong></a></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='matched-card'>✅ <strong>{bank}</strong></div>", unsafe_allow_html=True)
    else:
        st.warning("条件に合致する銀行はありません")

    st.markdown("### ❌ 条件に合わなかった銀行")
    if excluded_banks:
        for bank in excluded_banks:
            st.markdown(f"<div class='excluded-card'>❌ {bank}</div>", unsafe_allow_html=True)
    else:
        st.write("除外された銀行はありません")
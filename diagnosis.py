import streamlit as st
import csv

st.set_page_config(page_title="銀行診断フォーム", page_icon="🏦", layout="centered")

# 💅 デザイン設定
st.markdown("""
    <style>
        body { background-color: #ffffff; }
        h1 { color: #003366; font-size: 30px; }
        .stButton>button {
            background-color: #005792;
            color: white;
            border-radius: 6px;
            padding: 10px 20px;
            font-size: 16px;
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

# 📋 入力エリア
st.markdown("### 📋 条件を入力してください")

area = st.selectbox("居住地", ["東京都", "埼玉県", "神奈川県", "千葉県"])
target_type = st.radio("属性", ["サラリーマン", "法人"])
income_input = st.number_input("給与年収（万円）", min_value=0, step=100)
financial_input = st.number_input("金融資産（万円）", min_value=0, step=100)
loan_input = st.number_input("既存借入金額（万円）", min_value=0, step=100)

# 円換算とカンマ付き表示
income = income_input * 10000
financial_assets = financial_input * 10000
loan_amount = loan_input * 10000
net_assets = financial_assets - loan_amount

# ✅ 表示用テキスト
st.markdown(f"**給与年収:** {income:,.0f} 円")
st.markdown(f"**金融資産:** {financial_assets:,.0f} 円")
st.markdown(f"**既存借入金額:** {loan_amount:,.0f} 円")
st.markdown(f"**純資産（自動計算）:** {net_assets:,.0f} 円")

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
                bank_area = row["area"]
                bank_target = row["target_type"]
                income_required = parse_amount(row["min_income"])
                assets_required = parse_amount(row["min_net_assets"])

                if (
                    area in bank_area and
                    (bank_target == "両方" or bank_target == target_type) and
                    income >= income_required and
                    net_assets >= assets_required
                ):
                    matched_banks.append(name)
                else:
                    reasons = []
                    if area not in bank_area:
                        reasons.append("エリア不一致")
                    if bank_target != "両方" and bank_target != target_type:
                        reasons.append("属性不一致")
                    if income < income_required:
                        reasons.append("給与年収が足りない")
                    if net_assets < assets_required:
                        reasons.append("純資産が足りない")
                    excluded_banks.append(f"{name}（理由：{', '.join(reasons)}）")
    except FileNotFoundError:
        st.error("⚠️ Book1.csv が見つかりません。同じフォルダーに配置してください。")

    # 🏁 診断結果
    st.markdown("### ✅ 該当する銀行")
    if matched_banks:
        for bank in matched_banks:
            st.markdown(f"<div class='matched-card'>✅ <strong>{bank}</strong></div>", unsafe_allow_html=True)
    else:
        st.warning("条件に合致する銀行はありません")

    st.markdown("### ❌ 条件に合わなかった銀行")
    if excluded_banks:
        for bank in excluded_banks:
            st.markdown(f"<div class='excluded-card'>❌ {bank}</div>", unsafe_allow_html=True)
    else:
        st.write("除外された銀行はありません")
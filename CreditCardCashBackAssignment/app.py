import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from cashback import calculate_cashback
from utils import load_card_rules, list_card_names

st.title("💳 Cashback Calculator")

uploaded_file = st.file_uploader("Upload transaction CSV", type=["csv"])
card_names = list_card_names()
card_name = st.selectbox("Select your Credit Card", card_names)

if uploaded_file and card_name:
    df = pd.read_csv(uploaded_file)

    try:
        card_data = load_card_rules(card_name)
        rules = card_data["rules"]

        cashback_df, summary = calculate_cashback(df, rules)

        st.subheader("📋 Cashback Details")
        st.dataframe(cashback_df)

        st.subheader("💰 Total Cashback Earned")
        total_cashback = cashback_df["Cashback"].sum()
        st.metric(label="Total Cashback", value=f"₹{total_cashback:.2f}")

        st.subheader("📊 Spend Distribution")
        spend_by_cat = df.groupby("Transaction Type")["Amount"].sum()
        fig, ax = plt.subplots()
        spend_by_cat.plot(kind="pie", autopct="%1.1f%%", ax=ax)
        ax.set_ylabel("")
        st.pyplot(fig)

        st.subheader("⬇️ Download Cashback Summary")
        st.download_button("Download CSV", cashback_df.to_csv(index=False), file_name="cashback_summary.csv")

    except Exception as e:
        st.error(f"Error: {e}")

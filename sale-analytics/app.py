import streamlit as st
import pandas as pd
import os
import google.generativeai as genai

st.set_page_config(page_title="11.11 Sale Analytics", layout="wide")

@st.cache_data
def load_data():
    rev_cat = pd.read_csv("results/revenue_by_category.csv")
    orders_hour = pd.read_csv("results/orders_per_hour.csv")
    region_sum = pd.read_csv("results/region_summary.csv")
    canc_pm = pd.read_csv("results/cancellation_by_payment.csv")
    aov_df = pd.read_csv("results/aov.csv")
    return rev_cat, orders_hour, region_sum, canc_pm, aov_df

rev_cat, orders_hour, region_sum, canc_pm, aov_df = load_data()

st.title("🛍️ 11.11 Sale Analytics Dashboard")

# Region Filter
regions = ["All"] + list(region_sum["region"].unique())
selected_region = st.selectbox("Select Region Filter", regions)

# Key Metrics Top Banner
total_revenue = region_sum["revenue"].sum()
total_orders = region_sum["order_count"].sum()
avg_aov = aov_df["avg_order_value"].iloc[0]
overall_canc_rate = canc_pm["cancelled_orders"].sum() / canc_pm["total_orders"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"₱{total_revenue:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Cancellation Rate", f"{overall_canc_rate:.2%}")
col4.metric("Avg Order Value", f"₱{avg_aov:,.2f}")

st.divider()

# Charts
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Revenue by Category")
    st.bar_chart(rev_cat.set_index("category")["total_revenue"])

with col_b:
    st.subheader("Orders per Hour")
    st.line_chart(orders_hour.set_index("hour")["order_count"])

st.divider()

# Generative AI Briefing
st.subheader("🤖 AI Sales Briefing")
if st.button("Generate Briefing"):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"""
        Using ONLY the following sales metrics from our 11.11 sale, write a 5-sentence executive briefing for the store owner with one concrete recommendation for next year's sale:
        - Total Revenue: ₱{total_revenue:,.2f}
        - Total Orders: {total_orders:,}
        - Overall Cancellation Rate: {overall_canc_rate:.2%}
        - Average Order Value: ₱{avg_aov:,.2f}
        """
        response = model.generate_content(prompt)
        st.success(response.text)
    except Exception as e:
        st.error(f"Could not generate briefing. Error: {e}")

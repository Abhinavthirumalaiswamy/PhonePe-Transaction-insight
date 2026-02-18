import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# 1. Database Connection
engine = create_engine("mysql+mysqlconnector://root:12345@localhost/phonepe_data")

# 2. UI Configuration
st.set_page_config(page_title="PhonePe Analysis", layout="wide")

# Main Bar Dropdown (Succinctly placed at the top)
menu = st.selectbox("📌 Select Business Scenario", [
    "1. Transaction Analysis Across States",
    "2. Market Expansion (2023)",
    "3. Insurance Engagement Analysis",
    "4. User Growth Strategy",
    "5. Insurance Pincode Analysis"
])

st.divider() # Visual separation between menu and content

# 3. Scenario Logic
try:
    if menu == "1. Transaction Analysis Across States":
        st.title("📊 Transaction Analysis Across States")
        df = pd.read_sql("SELECT State, SUM(Transacion_Count) AS Total_Txn, SUM(Transacion_Amount) AS Total_Value FROM aggregated_transaction GROUP BY State ORDER BY Total_Value DESC LIMIT 20", engine)
        c1, c2 = st.columns(2)
        c1.plotly_chart(px.bar(df, x="State", y="Total_Value", color="Total_Value", title="Top Regions by Value"), use_container_width=True)
        c2.plotly_chart(px.pie(df, values="Total_Txn", names="State", hole=0.4, title="Transaction Share"), use_container_width=True)
        st.dataframe(df, use_container_width=True)

    elif menu == "2. Market Expansion (2023)":
        st.title("📈 Market Expansion (2023)")
        df = pd.read_sql("SELECT State, SUM(Transacion_Count) AS Total_Transactions, SUM(Transacion_Amount) AS Total_Revenue FROM aggregated_transaction WHERE Year=2023 GROUP BY State ORDER BY Total_Revenue DESC LIMIT 10", engine)
        c1, c2 = st.columns(2)
        c1.plotly_chart(px.bar(df, x='State', y='Total_Revenue', color='Total_Revenue', title="Top 10 Revenue States"), use_container_width=True)
        c2.plotly_chart(px.pie(df, values='Total_Transactions', names='State', title="Volume Share"), use_container_width=True)
        st.dataframe(df, use_container_width=True)

    elif menu == "3. Insurance Engagement Analysis":
        st.title("🛡️ Insurance Engagement")
        df = pd.read_sql("SELECT State, District, SUM(Insurance_Count) AS total_engagement, SUM(Insurance_Amount) AS total_revenue FROM map_insurance GROUP BY State, District ORDER BY total_revenue DESC LIMIT 10", engine)
        c1, c2 = st.columns(2)
        c1.plotly_chart(px.bar(df, x="District", y="total_revenue", color="State", title="Revenue by District"), use_container_width=True)
        c2.plotly_chart(px.pie(df, values="total_engagement", names="District", hole=0.4, title="Engagement Share"), use_container_width=True)
        st.dataframe(df, use_container_width=True)

    elif menu == "4. User Growth Strategy":
        st.title("🚀 User Engagement (Q4 2023)")
        df = pd.read_sql("SELECT District, SUM(App_Opens) AS App_Opens, ROUND(SUM(App_Opens)/NULLIF(SUM(Registered_Users),0),2) AS Ratio FROM map_user WHERE Year=2023 AND Quarter=4 GROUP BY State, District ORDER BY Ratio DESC LIMIT 10", engine)
        c1, c2 = st.columns(2)
        c1.plotly_chart(px.bar(df, x='District', y='Ratio', title="Engagement Ratio"), use_container_width=True)
        c2.plotly_chart(px.pie(df, values='App_Opens', names='District', title="App Opens Distribution"), use_container_width=True)
        st.dataframe(df, use_container_width=True)

    elif menu == "5. Insurance Pincode Analysis":
        st.title("📍 Top Pincodes (2023 Q1)")
        df = pd.read_sql("SELECT State, CAST(Pincode AS CHAR) AS Pincode, SUM(Insurance_Count) AS Txn, SUM(Insurance_Amount) AS Value FROM top_insurance WHERE Year=2023 AND Quarter=1 GROUP BY State, Pincode ORDER BY Txn DESC LIMIT 10", engine)
        c1, c2 = st.columns(2)
        c1.plotly_chart(px.bar(df, x='Pincode', y='Txn', color='State', title="Transactions by Pincode"), use_container_width=True)
        c2.plotly_chart(px.pie(df, values='Value', names='Pincode', title="Value Share"), use_container_width=True)
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"❌ Error: {e}")
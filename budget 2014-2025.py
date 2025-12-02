import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------
# PAGE CONFIG
# -----------------------------------------------
st.set_page_config(
    page_title="Budget Analysis Dashboard",
    layout="wide",
    page_icon="💰"
)

# -----------------------------------------------
# STYLING (UI Enhancements)
# -----------------------------------------------
st.markdown("""
<style>
    .main { background-color: #f7f7f7; }
    .title {
        font-size: 36px;
        font-weight: 700;
        text-align: center;
        color: #2b5876;
        padding-bottom: 10px;
    }
    .subtitle {
        font-size: 18px;
        color: #555;
        text-align: center;
    }
    .card {
        padding: 20px;
        border-radius: 12px;
        background-color: white;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------
# SIDEBAR
# -----------------------------------------------
st.sidebar.title("📂 Upload Budget File")
uploaded = st.sidebar.file_uploader("Upload Excel or CSV", type=["csv", "xlsx"])

st.sidebar.markdown("---")
st.sidebar.write("📊 **Dashboard Options**")
view = st.sidebar.radio("Choose View", ["Summary", "Yearly Trend", "Category Breakdown"])

# -----------------------------------------------
# HEADER
# -----------------------------------------------
st.markdown('<p class="title">💰 Budget Analysis Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Analyse budgets from 2014–2025 (or any file you upload)</p>', unsafe_allow_html=True)

# -----------------------------------------------
# MAIN LOGIC
# -----------------------------------------------
if uploaded:
    try:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)

        st.success("File uploaded successfully!")

        # Ensure column names are recognized
        expected_cols = ["Year", "Category", "Amount"]
        if not all(col in df.columns for col in expected_cols):
            st.error("❌ File must contain columns: Year, Category, Amount")
            st.write("Columns found:", list(df.columns))
        else:

            # Display Data Table
            if st.checkbox("Show Data Table"):
                st.dataframe(df, use_container_width=True)

            # -------------------------------------------
            # VIEW 1: SUMMARY
            # -------------------------------------------
            if view == "Summary":
                total_budget = df["Amount"].sum()
                total_years = df["Year"].nunique()
                total_categories = df["Category"].nunique()

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown('<div class="card"><h3>Total Budget</h3><h2>₹{:,.2f}</h2></div>'.format(total_budget),
                                unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="card"><h3>Total Years</h3><h2>{total_years}</h2></div>',
                                unsafe_allow_html=True)
                with col3:
                    st.markdown(f'<div class="card"><h3>Categories</h3><h2>{total_categories}</h2></div>',
                                unsafe_allow_html=True)

            # -------------------------------------------
            # VIEW 2: YEARLY TREND
            # -------------------------------------------
            elif view == "Yearly Trend":
                yearly = df.groupby("Year")["Amount"].sum().reset_index()

                fig = px.line(yearly, x="Year", y="Amount",
                              markers=True,
                              title="📈 Year-by-Year Budget Trend")
                st.plotly_chart(fig, use_container_width=True)

            # -------------------------------------------
            # VIEW 3: CATEGORY BREAKDOWN
            # -------------------------------------------
            elif view == "Category Breakdown":
                category = df.groupby("Category")["Amount"].sum().reset_index()

                fig = px.bar(category, x="Category", y="Amount",
                             title="📊 Budget by Category",
                             text_auto=True)
                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error("⚠️ Error reading file.")
        st.write(e)

else:
    st.info("👈 Upload a file from the sidebar to start the analysis.")

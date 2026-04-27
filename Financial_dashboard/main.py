import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import io

# 1. Page Configuration
st.set_page_config(page_title="Financial Intel Dashboard", layout="wide", page_icon="📈")

# 2. Template Generation Logic
template_data = pd.DataFrame({
    "Date": ["2024-01-01", "2024-01-02", "2024-01-03"],
    "Revenue": [1200, 1500, 1100],
    "Expenses": [400, 600, 300],
    "Category": ["Marketing", "Software", "Operations"]
})
csv_template = template_data.to_csv(index=False).encode('utf-8')


# 3. Secure Data Loader
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            file_ext = uploaded_file.name.split('.')[-1].lower()
            if file_ext == 'csv':
                return pd.read_csv(uploaded_file)
            elif file_ext in ['xlsx', 'xls']:
                return pd.read_excel(uploaded_file)
            else:
                return "ERROR: Unsupported file type. Please use a standard Excel (.xlsx) or CSV file."
        except Exception as e:
            return f"ERROR: Could not read file. {e}"
    return "DUMMY"


# 4. Sidebar Configuration
with st.sidebar:
    st.title("⚙️ Dashboard Controls")

    st.header("📂 Getting Started")
    st.write("Upload your business records below to see your insights.")

    uploaded_file = st.file_uploader(
        "📁 Upload your Financial Spreadsheet (Excel or CSV)",
        type=["csv", "xlsx", "xls"],
        help="Supports .xlsx, .xls, and .csv files."
    )

    st.divider()

    st.subheader("📋 Preparation Guide")
    st.markdown("""
    Headers must be **exact**:
    * **Date**
    * **Revenue**
    * **Expenses**
    * **Category**
    """)

    st.divider()
    st.subheader("📥 Template")
    st.download_button(
        "Download Example Spreadsheet",
        csv_template,
        "business_template.csv",
        "text/csv"
    )



# 5. Data Loading & Validation
data_result = load_data(uploaded_file)

if isinstance(data_result, str) and data_result.startswith("ERROR"):
    st.error(data_result)
    st.stop()

if isinstance(data_result, str) and data_result == "DUMMY":
    df = pd.DataFrame({
        "Date": pd.date_range(start="2024-01-01", periods=12, freq="ME"),
        "Revenue": np.random.randint(8000, 18000, size=12),
        "Expenses": np.random.randint(4000, 9000, size=12),
        "Category": np.random.choice(['Marketing', 'Operations', 'Payroll', 'Software'], size=12)
    })
    st.toast("Running in Demo Mode.")
else:
    df = data_result

# Validation Logic
required_cols = ['Date', 'Revenue', 'Expenses', 'Category']
actual_cols = list(df.columns)
missing_cols = [col for col in required_cols if col not in actual_cols]

if missing_cols:
    st.header("⚠️ Action Required")
    st.error(f"Missing columns: **{', '.join(missing_cols)}**")
    st.info("Ensure your headers match the template in the sidebar.")
    st.stop()

# --- DASHBOARD RENDERING ---
try:
    df['Date'] = pd.to_datetime(df['Date'])
    st.title("📈 Financial Intelligence Dashboard")

    # Metrics
    total_rev = df["Revenue"].sum()
    total_exp = df["Expenses"].sum()
    net_profit = total_rev - total_exp
    margin = (net_profit / total_rev) * 100 if total_rev > 0 else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Revenue", f"${total_rev:,.0f}")
    m2.metric("Total Expenses", f"${total_exp:,.0f}")
    m3.metric("Net Profit", f"${net_profit:,.0f}")
    m4.metric("Profit Margin", f"{margin:.1f}%")

    st.divider()

    tab1, tab2 = st.tabs(["📈 Visual Analysis", "📑 Business Report"])

    with tab1:
        # Filter Logic
        with st.sidebar:
            st.header("🔍 Filters")
            selected_cats = st.multiselect("Category Filter", options=df["Category"].unique(),
                                           default=df["Category"].unique())

        f_df = df[df["Category"].isin(selected_cats)]

        c_a, c_b = st.columns(2)
        with c_a:
            st.subheader("Cash Flow Trend")
            #  LINE CHART
            fig_l = px.line(f_df, x="Date", y=["Revenue", "Expenses"],
                            color_discrete_sequence=["#A020F0", "#E0E0E0"],  # Purple and Gray
                            template="plotly_dark", markers=True)
            st.plotly_chart(fig_l, use_container_width=True)
        with c_b:
            st.subheader("Expense Distribution")
            # PIE CHART
            fig_p = px.pie(f_df, values='Expenses', names='Category', hole=0.5,
                           template="plotly_dark",
                           color_discrete_sequence=px.colors.sequential.Purp)
            st.plotly_chart(fig_p, use_container_width=True)

    with tab2:
        st.subheader("💡 Automated Insights")
        top_cat = df.groupby("Category")["Expenses"].sum().idxmax()
        st.info(f"🔍 **Observation:** Your highest spending is in **{top_cat}**.")

        st.subheader("Recent Records")
        st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)

except Exception as e:
    st.error(f"🤯 Dashboard Error: {e}")
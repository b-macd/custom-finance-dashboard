import streamlit as st
import pandas as pd


if "dataframes" not in st.session_state:
    st.session_state.dataframes = {}

st.title("Finance Dashboard")
st.subheader(f"Welcome, {st.session_state.username}!")
st.write("Use the navigation menu in the sidebar (on mobile, click the '>>' in the top left corner to access this.) to explore different sections of the dashboard.")
st.write("Dashboard Features:")
st.markdown("""
- **Accounts Overview**: Get a summary of your financial accounts.
- **Budget Builder**: Create and manage your budget effectively.
- **Monthly Expense Report**: Analyze your monthly expenses in detail.
- **Transfer Tracker**: Track transfers between your accounts.
""")

# upload file feature to store csv data in dataframs for other pages
st.info("Upload Your Financial Data in CSV format")
uploaded_files = st.file_uploader("Upload a CSV file containing your financial data", type=["csv"], accept_multiple_files=True,)

if uploaded_files:
    st.write(f"You have uploaded {len(uploaded_files)} file(s).")

    for uploaded_file in uploaded_files:
        st.write(f"Processing file: {uploaded_file.name}")
        st.session_state.dataframes[uploaded_file.name] = pd.read_csv(uploaded_file)



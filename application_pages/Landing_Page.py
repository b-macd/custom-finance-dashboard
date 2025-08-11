import streamlit as st
import pandas as pd
import hashlib

if "dataframes" not in st.session_state:
    st.session_state.dataframes = {}

def get_md5_hash(input_string):
    """
    Computes the MD5 hash of a given string.
    """
    md5_hash_object = hashlib.md5()
    md5_hash_object.update(input_string.encode('utf-8'))
    hex_digest = md5_hash_object.hexdigest()
    return hex_digest

#st.set_page_config(page_title="Finance Dashboard", page_icon=":money_with_wings:", layout="wide")
st.title("Landing Page")
st.subheader("Welcome to the Finance Dashboard")
st.write("This dashboard provides an overview of your financial data, including budget tracking, account summaries, and more.")
st.write("Use the navigation menu to explore different sections of the dashboard.")
st.write("To get started, please select a section from the sidebar.")
st.write("If you have any questions or need assistance, feel free to reach out!")
st.write("Happy budgeting and financial planning!")
st.write("Explore the features of this dashboard:")
st.markdown("""
- **Accounts Overview**: Get a summary of your financial accounts.
- **Budget Builder**: Create and manage your budget effectively.
- **Monthly Expense Report**: Analyze your monthly expenses in detail.
- **Transfer Tracker**: Track transfers between your accounts.
""")

# upload file feature to store csv data in dataframs for other pages
st.subheader("Upload Your Financial Data")
uploaded_files = st.file_uploader("Upload a CSV file containing your financial data", type=["csv"], accept_multiple_files=True,)

if uploaded_files:
    st.write(f"You have uploaded {len(uploaded_files)} file(s).")

    for uploaded_file in uploaded_files:
        st.write(f"Processing file: {uploaded_file.name}")
        st.session_state.dataframes[uploaded_file.name] = pd.read_csv(uploaded_file)



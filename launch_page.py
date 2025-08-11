import streamlit as st
import hashlib

def get_md5_hash(input_string):
    """
    Computes the MD5 hash of a given string.
    """
    md5_hash_object = hashlib.md5()
    md5_hash_object.update(input_string.encode('utf-8'))
    hex_digest = md5_hash_object.hexdigest()
    return hex_digest

st.set_page_config(layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def login():
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            hashed_password = get_md5_hash(password)
            if hashed_password == st.secrets[f"{username}"]:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
                

landing_page = st.Page(
    "application_pages/Landing_Page.py",
    title="Landing Page",
    icon=":material/home:",
)
app_1 = st.Page(
    "application_pages/Accounts_Overview.py",
    title="Accounts Overview",
    icon=":material/account_balance:",
)
app_2 = st.Page(
    "application_pages/Budget_Builder.py",
    title="Budget Builder",
    icon=":material/price_check:",
)
app_3 = st.Page(
    "application_pages/Monthly_Expense_Report.py",
    title="Monthly Expense Report",
    icon=":material/analytics:",
)
app_4 = st.Page(
    "application_pages/Transfer_Tracker.py",
    title="Transfer Tracker",
    icon=":material/query_stats:",
)

home_page = [landing_page]
application_pages = [app_1, app_2, app_3, app_4]

page_dict ={}
if st.session_state.username in ["Olivia"]:
    page_dict["Applications"] = application_pages

if st.session_state.logged_in == True:
    pg = st.navigation({"Home Page": home_page} | page_dict)
elif st.session_state.logged_in == False:
    pg = st.navigation([st.Page(login)])

pg.run()
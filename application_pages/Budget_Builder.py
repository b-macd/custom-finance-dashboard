import streamlit as st
import pandas as pd
import plotly.express as px

#st.set_page_config(page_title="Budget Dashboard", page_icon=":money_with_wings:", layout="wide")
st.title("Budget Dashboard")

# Initialize session state variables
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'num_income_sources' not in st.session_state:
    st.session_state.num_income_sources = 1
if 'income_data' not in st.session_state:
    st.session_state.income_data = []
if 'budget_df' not in st.session_state:
    st.session_state.budget_df = pd.DataFrame(columns=["Category", "Description", "Amount"])
if 'extra_expenses' not in st.session_state:
    st.session_state.extra_expenses = []

# Step 1: Get number of income sources
if st.session_state.step == 1:
    with st.form("income_count_form"):
        st.subheader("Income Sources")
        num_sources = st.number_input("How many sources of income do you have?", 
                                    min_value=1, 
                                    value=st.session_state.num_income_sources)
        if st.form_submit_button("Continue"):
            st.session_state.num_income_sources = num_sources
            st.session_state.step = 2
            st.rerun()

# Step 2: Income form
elif st.session_state.step == 2:
    with st.form("income_form"):
        st.subheader("Income Details")
        income_sources = []
        for i in range(st.session_state.num_income_sources):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                name = st.text_input(f"Income Source {i+1} Name", key=f"name_{i}")
            with col2:
                amount = st.number_input(f"Amount", min_value=0.0, key=f"amount_{i}")
            with col3:
                date = st.date_input(f"Direct Deposit Date", key=f"date_{i}")
            income_sources.append({"name": name, "amount": amount, "date": date})
        
        if st.form_submit_button("Continue to Expenses"):
            st.session_state.income_data = income_sources
            st.session_state.step = 3
            st.rerun()

# Step 3: Expenses form
elif st.session_state.step == 3:
    with st.form("expenses_form"):
        st.subheader("Expenses")
        # For each expense, create two columns: one for amount and one for due date
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your electricity bill:", key="electricity_bill", min_value=0)
        with col2:
            st.date_input("Due Date:", key="electricity_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your water bill:", key="water_bill", min_value=0)
        with col2:
            st.date_input("Due Date:", key="water_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your internet bill:", key="internet_bill", min_value=0)
        with col2:
            st.date_input("Due Date:", key="internet_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your mobile phone bill:", key="mobile_phone_bill", min_value=0)
        with col2:
            st.date_input("Due Date:", key="mobile_phone_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your home phone bill:", key="home_phone_bill", min_value=0)
        with col2:
            st.date_input("Due Date:", key="home_phone_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your 1st mortgage payment:", key="mortgage_payment", min_value=0)
        with col2:
            st.date_input("Due Date:", key="mortgage_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your 2nd mortgage payment:", key="mortgage_payment_2", min_value=0)
        with col2:
            st.date_input("Due Date:", key="mortgage_date_2")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your vehicle payment:", key="vehicle_payment", min_value=0)
        with col2:
            st.date_input("Due Date:", key="vehicle_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your student loan payment:", key="student_loan_payment", min_value=0)
        with col2:
            st.date_input("Due Date:", key="student_loan_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your Visa credit card payment:", key="credit_card_payment", min_value=0)
        with col2:
            st.date_input("Due Date:", key="visa_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your American Express credit card payment:", key="amex_payment", min_value=0)
        with col2:
            st.date_input("Due Date:", key="amex_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your Lowes credit card payment:", key="discover_payment", min_value=0)
        with col2:
            st.date_input("Due Date:", key="discover_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your personal loan payment:", key="personal_loan_payment", min_value=0)
        with col2:
            st.date_input("Due Date:", key="personal_loan_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your savings contribution:", key="savings_contribution", min_value=0)
        with col2:
            st.date_input("Due Date:", key="savings_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your investment contribution:", key="investment_contribution", min_value=0)
        with col2:
            st.date_input("Due Date:", key="investment_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your entertainment budget:", key="entertainment_budget", min_value=0)
        with col2:
            st.date_input("Due Date:", key="entertainment_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your groceries budget:", key="groceries_budget", min_value=0)
        with col2:
            st.date_input("Due Date:", key="groceries_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your transportation budget:", key="transportation_budget", min_value=0)
        with col2:
            st.date_input("Due Date:", key="transportation_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your healthcare budget:", key="healthcare_budget", min_value=0)
        with col2:
            st.date_input("Due Date:", key="healthcare_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your insurance budget:", key="insurance_budget", min_value=0)
        with col2:
            st.date_input("Due Date:", key="insurance_date")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.number_input("Enter your miscellaneous budget:", key="miscellaneous_budget", min_value=0)
        with col2:
            st.date_input("Due Date:", key="miscellaneous_date")
        
        st.markdown("#### Additional Expenses")
        # Button to add a new expense item
        if st.form_submit_button("Add Expense Item"):
            st.session_state.extra_expenses.append({"name": "", "amount": 0.0, "date": pd.Timestamp.today()})

        # Render input fields for each extra expense
        for idx, item in enumerate(st.session_state.extra_expenses):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.session_state.extra_expenses[idx]["name"] = st.text_input(
                    f"Extra Expense Name {idx+1}", value=item["name"], key=f"extra_name_{idx}")
            with col2:
                st.session_state.extra_expenses[idx]["amount"] = st.number_input(
                    f"Amount {idx+1}", min_value=0.0, value=item["amount"], key=f"extra_amount_{idx}")
            with col3:
                st.session_state.extra_expenses[idx]["date"] = st.date_input(
                    f"Due Date {idx+1}", value=item["date"], key=f"extra_date_{idx}")

        if st.form_submit_button("Generate Budget"):
            # Extract income categories, amounts, and dates from session state
            income_categories = [source["name"] for source in st.session_state.income_data]
            income_amounts = [source["amount"] for source in st.session_state.income_data]
            income_dates = [source["date"] for source in st.session_state.income_data]
            
            # Define expense descriptions and their corresponding session state keys
            expense_items = [
                ("Electricity", "electricity_bill", "electricity_date"),
                ("Water", "water_bill", "water_date"),
                ("Internet", "internet_bill", "internet_date"),
                ("Mobile Phone", "mobile_phone_bill", "mobile_phone_date"),
                ("Home Phone", "home_phone_bill", "home_phone_date"),
                ("Mortgage Payment 1", "mortgage_payment", "mortgage_date"),
                ("Mortgage Payment 2", "mortgage_payment_2", "mortgage_date_2"),
                ("Vehicle Payment", "vehicle_payment", "vehicle_date"),
                ("Student Loan Payment", "student_loan_payment", "student_loan_date"),
                ("Visa Credit Card Payment", "credit_card_payment", "visa_date"),
                ("American Express Credit Card Payment", "amex_payment", "amex_date"),
                ("Discover Credit Card Payment", "discover_payment", "discover_date"),
                ("Personal Loan Payment", "personal_loan_payment", "personal_loan_date"),
                ("Savings Contribution", "savings_contribution", "savings_date"),
                ("Investment Contribution", "investment_contribution", "investment_date"),
                ("Entertainment Budget", "entertainment_budget", "entertainment_date"),
                ("Groceries Budget", "groceries_budget", "groceries_date"),
                ("Transportation Budget", "transportation_budget", "transportation_date"),
                ("Healthcare Budget", "healthcare_budget", "healthcare_date"),
                ("Insurance Budget", "insurance_budget", "insurance_date"),
                ("Miscellaneous Budget", "miscellaneous_budget", "miscellaneous_date")
            ]
            
            # Create expense descriptions, amounts, and dates
            expense_descriptions = [item[0] for item in expense_items]
            expense_amounts = [-st.session_state[item[1]] for item in expense_items]
            expense_dates = [st.session_state[item[2]] for item in expense_items]
            
            # Add extra expenses to the expense lists
            for item in st.session_state.extra_expenses:
                expense_descriptions.append(item["name"])
                expense_amounts.append(-item["amount"])
                expense_dates.append(item["date"])

            # Fix: Update the Category list to match the new length
            total_expenses = len(expense_descriptions)
            budget_data = {
                "Category": ["Income"] * len(income_categories) + ["Expense"] * total_expenses,
                "Description": income_categories + expense_descriptions,
                "Amount": income_amounts + expense_amounts,
                "Date": income_dates + expense_dates
            }
            
            df_budget = pd.DataFrame(budget_data)
            # Sort the DataFrame by date
            df_budget = df_budget.sort_values(by="Date")
            st.session_state.budget_df = df_budget
            st.session_state.step = 4
            st.rerun()

elif st.session_state.step == 4:
    st.subheader("Budget Overview")
    if 'budget_df' in st.session_state and not st.session_state.budget_df.empty:
        df_budget = st.session_state.budget_df
        if not df_budget.empty:
            df_budget = df_budget[df_budget["Amount"] != 0]  # Remove zero amounts
            df_budget["Amount"] = df_budget["Amount"].astype(float)  # Ensure Amount is float
            # Display the budget data
            st.dataframe(df_budget)
            
            # Create a bar chart of the budget data
            fig = px.bar(df_budget, 
                         x="Description", 
                         y="Amount", 
                         color="Category",
                         title="Budget Overview",
                         labels={"Description": "Budget Item", "Amount": "Amount ($)"}
                        )
            st.plotly_chart(fig)
            # Calculate total income and expenses
            total_income = df_budget[df_budget["Category"] == "Income"]["Amount"].sum()
            total_expenses = df_budget[df_budget["Category"] == "Expense"]["Amount"].sum() * -1  # Make positive for display
            net_budget = total_income - total_expenses

            # Display total income, expenses, and net budget
            st.subheader("Budget Summary")
            st.write(f"Total Income: ${total_income:,.2f}")
            st.write(f"Total Expenses: ${total_expenses:,.2f}")
            st.write(f"Net Budget: ${net_budget:,.2f}")
            # Display a message based on the net budget
            if net_budget > 0:
                st.success("You have a positive budget balance!")
            elif net_budget < 0:
                st.error("You have a negative budget balance. Consider reducing expenses.")
            else:
                st.info("Your budget is balanced.")
            
            if st.button("Save Budget Data"):
                # Save the budget data to a CSV file
                df_budget.to_csv("budget_data.csv", index=False)
                # Display a message indicating the budget data has been saved
                st.success("Budget data has been saved to 'budget_data.csv'. You can download it using the button below.")
                # Save the budget data to a CSV file
                st.download_button(
                    label="Download Budget Data",
                    data=df_budget.to_csv(index=False).encode('utf-8'),
                    file_name='budget_data.csv',
                    mime='text/csv'
                )
            # Create separate dataframes for income and expenses
            income_df = df_budget[df_budget["Category"] == "Income"].copy()
            expense_df = df_budget[df_budget["Category"] == "Expense"].copy()
            
            # Combine all transactions and sort by date
            all_transactions = pd.concat([
                income_df[["Date", "Amount"]],
                expense_df[["Date", "Amount"]]
            ]).sort_values("Date")
            
            # Calculate running balance
            all_transactions["Running_Balance"] = all_transactions["Amount"].cumsum()
            
            # Create the line chart
            fig_line = px.line(
                all_transactions,
                x="Date",
                y="Running_Balance",
                title="Account Balance Over Time",
                labels={
                    "Date": "Date",
                    "Running_Balance": "Balance ($)"
                }
            )
            
            # Customize the layout
            fig_line.update_layout(
                hovermode="x unified",
                showlegend=False
            )
            
            # Color the line based on whether balance is positive or negative
            fig_line.update_traces(
                line=dict(
                    color="green",
                    width=2
                ),
                name="Balance"
            )
            
            # Add a reference line at y=0
            fig_line.add_hline(
                y=0,
                line_dash="dash",
                line_color="red",
                opacity=0.5
            )
            
            # Display the line chart
            st.plotly_chart(fig_line)
    
# Step 4: Results
#elif st.session_state.step == 4:
    # Your existing budget display code here
    # ... (starting from line 73 in your original code)

#else:
#    st.error("An unexpected error occurred. Please try again.")

# Add a reset button
if st.session_state.step > 1:
    if st.button("Start Over"):
        st.session_state.step = 1
        st.session_state.num_income_sources = 1
        st.session_state.income_data = []
        st.session_state.extra_expenses = []
        st.rerun()
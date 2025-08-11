import streamlit as st
import pandas as pd
import plotly.express as px

df1 = st.selectbox("Select Fixed Account Data", options=list(st.session_state.dataframes.keys()), index=0)
df = st.session_state.dataframes[df1]

df2 = st.selectbox("Select Variable Account Data", options=list(st.session_state.dataframes.keys()), index=1)
df_variable = st.session_state.dataframes[df2]

st.title("Accounts Overview")
st.subheader("Overview of Financial Data")
with st.expander("View Raw Data for Fixed Account"):
    st.dataframe(df)
with st.expander("View Raw Data for Variable Account"):
    st.dataframe(df_variable)
# Create category mapping
category_mapping = {
    'Food & Dining': 'Eating Out',
    'Fast Food': 'Eating Out',
    'Coffee Shops': 'Eating Out',
    'Restaurants': 'Eating Out',
    'Electricity': 'Bills & Utilities',
    'Water': 'Bills & Utilities',
    'Utilities': 'Bills & Utilities',
    'Internet': 'Bills & Utilities',
    "Mobile Phone": 'Bills & Utilities',
    'Home Phone': 'Bills & Utilities',
    'Mortgage Payment': 'Mortgage & Rent',
    'Sports': 'Entertainment',
    'Hair': 'Personal Care',
    'Home': 'Home Improvement',
    'Lawn & Garden': 'Home Improvement',
    'Gas':'Auto & Transport',
    'Television': 'Entertainment',
    'Movies': 'Entertainment',
    'Music': 'Entertainment',
    'Books': 'Entertainment',    
    # Add more mappings as needed
}

# Apply mapping to the Category column
df['Category'] = df['Category'].replace(category_mapping)
df_variable['Category'] = df_variable['Category'].replace(category_mapping)

#st.dataframe(df)
df_variable_summed = df_variable
df_variable_summed = df_variable_summed.drop(columns=["Status", "Date"])
df_variable_summed = df_variable_summed.groupby('Category').sum().reset_index()


df_summed = df
df_summed = df_summed.drop(columns=["Status", "Date"])
# Group by Category and sum the Amounts
df_summed = df_summed.groupby('Category').sum().reset_index()
#st.dataframe(df_summed)

# Calculate totals for fixed account
positive_total_fixed = df_summed[df_summed['Amount'] > 0]['Amount'].sum()
negative_total_fixed = df_summed[df_summed['Amount'] < 0]['Amount'].sum()

# Calculate totals for variable account
positive_total_variable = df_variable_summed[df_variable_summed['Amount'] > 0]['Amount'].sum()
negative_total_variable = df_variable_summed[df_variable_summed['Amount'] < 0]['Amount'].sum()

# Display totals using columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Fixed Account Totals")
    st.write(f"Income: ${positive_total_fixed:,.2f}")
    st.write(f"Expenses: ${negative_total_fixed:,.2f}")
    st.write(f"Net: ${(positive_total_fixed + negative_total_fixed):,.2f}")

with col2:
    st.subheader("Variable Account Totals")
    st.write(f"Income: ${positive_total_variable:,.2f}")
    st.write(f"Expenses: ${negative_total_variable:,.2f}")
    st.write(f"Net: ${(positive_total_variable + negative_total_variable):,.2f}")

# Fixed Account Running Balance
df['Date'] = pd.to_datetime(df['Date'])
df_sorted = df.sort_values('Date')
df_sorted['Running_Balance'] = df_sorted['Amount'].cumsum()

# Group transactions by date for hover info for fixed account
hover_data = (df_sorted.groupby('Date')
             .agg({
                 'Description': lambda x: x.tolist(),  # Keep as list for zip
                 'Amount': lambda x: x.tolist(),       # Keep as list for zip
                 'Running_Balance': 'last'
             })
             .reset_index())

# Create combined description and amount strings
hover_data['Transaction_Details'] = hover_data.apply(
    lambda row: '<br>'.join([f"{desc} (${amt:,.2f})" 
                            for desc, amt in zip(row['Description'], row['Amount'])]), 
    axis=1
)

fig_line_fixed = px.line(
    hover_data,
    x='Date',
    y='Running_Balance',
    title='Fixed Account Running Balance',
    labels={
        'Date': 'Date',
        'Running_Balance': 'Balance ($)'
    }
)

# Update hover template with combined transaction details
fig_line_fixed.update_traces(
    hovertemplate="<b>Date: %{x}</b><br><br>" +
    "Transactions:<br>%{customdata[0]}<br><br>" +
    "Balance: $%{y:,.2f}<br>",
    customdata=hover_data[['Transaction_Details']].values
)

# Do the same for variable account
df_variable['Date'] = pd.to_datetime(df_variable['Date'])
df_variable_sorted = df_variable.sort_values('Date')
df_variable_sorted['Running_Balance'] = df_variable_sorted['Amount'].cumsum()

# Group transactions by date for hover info for variable account
hover_data_variable = (df_variable_sorted.groupby('Date')
             .agg({
                 'Description': lambda x: x.tolist(),  # Use Description instead of Original Description
                 'Amount': lambda x: x.tolist(),       # Keep as list for zip
                 'Running_Balance': 'last'
             })
             .reset_index())

# Create combined description and amount strings for variable account
hover_data_variable['Transaction_Details'] = hover_data_variable.apply(
    lambda row: '<br>'.join([f"{desc} (${amt:,.2f})" 
                            for desc, amt in zip(row['Description'], row['Amount'])]), 
    axis=1
)

fig_line_variable = px.line(
    hover_data_variable,
    x='Date',
    y='Running_Balance',
    title='Variable Account Running Balance',
    labels={
        'Date': 'Date',
        'Running_Balance': 'Balance ($)'
    }
)

# Update hover template with combined transaction details
fig_line_variable.update_traces(
    hovertemplate="<b>Date: %{x}</b><br><br>" +
    "Transactions:<br>%{customdata[0]}<br><br>" +
    "Balance: $%{y:,.2f}<br>",
    customdata=hover_data_variable[['Transaction_Details']].values
)

# Rest of your layout customization
for fig in [fig_line_fixed, fig_line_variable]:
    fig.update_layout(
        hovermode="x unified",
        showlegend=False
    )
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="red",
        opacity=0.5
    )

# Display the line graphs
st.plotly_chart(px.bar(df_summed, x='Category', y='Amount', title='Fixed Account').update_layout(xaxis_title='Category', yaxis_title='Total Amount'), use_container_width=True)
st.plotly_chart(fig_line_fixed, use_container_width=True)
st.plotly_chart(px.bar(df_variable_summed, x='Category', y='Amount', title='Variable Account').update_layout(xaxis_title='Category', yaxis_title='Total Amount'), use_container_width=True)
st.plotly_chart(fig_line_variable, use_container_width=True)


radio_selection = st.radio("Advanced Options", options=["View totals by transaction type", "View totals by transaction type by keyword"], index=0, key="advanced_options", horizontal=True)
list_of_descriptions = df['Description'].unique().tolist()
decriptions_variable = df_variable['Description'].unique().tolist()
for desc in decriptions_variable:
    if desc not in list_of_descriptions:
        list_of_descriptions.append(desc)
if radio_selection == "View totals by transaction type":
    with st.expander("View totals by transaction type"):
        st.write("This section allows you to view totals by transaction type for both fixed and variable accounts.")
        st.write("You can select multiple transaction types to see their combined amounts.")
        descriptions = st.multiselect("Select a Transaction Type", options=list_of_descriptions)
        # combine amounts for the selected description across both dataframes
        if not descriptions:
            st.warning("Please select at least one transaction type to view the combined amount.")
            st.stop()
        combined_amounts_total = 0
        for desc in descriptions:
            combined_amounts = df[df['Description'] == desc]['Amount'].sum() + df_variable[df_variable['Description'] == desc]['Amount'].sum()
            if combined_amounts == 0:
                st.warning(f"No transactions found for the transaction type: {desc}")
                continue
            # Display the combined amount for each selected description
            combined_amounts_total += combined_amounts
            st.info(f"Transaction type: {desc} \n\n Amount: ${(combined_amounts*-1):,.2f}")

        st.warning(f"Total Combined Amount for Selected Transactions: \n\n ${(combined_amounts_total*-1):,.2f}")

elif radio_selection == "View totals by transaction type by keyword":
    with st.expander("View totals by transaction type by keyword"):
        st.write("This section allows you to view totals by transaction type for both fixed and variable accounts.")
        st.write("You can search for transaction types by keyword to see their combined amounts.")
        keyword = st.text_input("Enter a keyword to search for transaction types:")
        if keyword:
            filtered_descriptions = [desc for desc in list_of_descriptions if keyword.lower() in desc.lower()]
            if not filtered_descriptions:
                st.warning(f"No transaction types found containing the keyword: {keyword}")
            else:
                combined_filtered_amounts_total = 0
                for desc in filtered_descriptions:
                    combined_amounts = df[df['Description'] == desc]['Amount'].sum() + df_variable[df_variable['Description'] == desc]['Amount'].sum()
                    if combined_amounts == 0:
                        st.warning(f"No transactions found for the transaction type: {desc}")
                        continue
                    # Display the combined amount for each filtered description
                    combined_filtered_amounts_total += combined_amounts
                    st.info(f"Transaction type: {desc} \n\n Amount: ${(combined_amounts*-1):,.2f}")
                st.warning(f"Total Combined Amount for Filtered Transactions: \n\n ${(combined_filtered_amounts_total*-1):,.2f}")
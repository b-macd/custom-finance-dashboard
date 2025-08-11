import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Monthly Expense Report")

if st.session_state.dataframes == {}:
    st.info("No data found. Please load your data first from the Home Page.")
else:
    # List all CSV files in the data directory

    selected_csv = st.selectbox("Select a CSV file", st.session_state.dataframes.keys())

    # Load data
    df = st.session_state.dataframes[selected_csv]
    df['Date'] = pd.to_datetime(df['Date'])

    # Filter for expenses only (negative amounts)
    df_expenses = df[df['Amount'] < 0].copy()
    df_expenses['Month'] = df_expenses['Date'].dt.to_period('M').astype(str)
    df_expenses['Day'] = df_expenses['Date'].dt.day
    df_expenses['Amount'] = df_expenses['Amount'].abs()

    # Group by month and day, sum expenses
    daily_expenses = df_expenses.groupby(['Month', 'Date']).agg({'Amount': 'sum'}).reset_index()

    # Let user select month
    months = daily_expenses['Month'].unique()
    selected_month = st.selectbox("Select Month", sorted(months, reverse=True))

    # Filter for selected month
    month_data = daily_expenses[daily_expenses['Month'] == selected_month]

    # Plot
    fig = px.line(
        month_data,
        x='Date',
        y='Amount',
        title=f"Daily Expenses for {selected_month}",
        labels={'Amount': 'Total Daily Expenses ($)', 'Date': 'Date'},
        markers=True
    )
    fig.update_traces(line_color='red')
    fig.update_layout(yaxis_tickformat='$,.2f')

    st.plotly_chart(fig, use_container_width=True)

    # --- Third graph: Top Expenses by Description for Each Month ---
    st.subheader("Top Expenses by Description for Each Month")

    # Get unique months sorted (most recent first)
    months_sorted = sorted(df_expenses['Month'].unique(), reverse=True)

    for month in months_sorted:
        month_desc = df_expenses[df_expenses['Month'] == month]
        desc_sum = (
            month_desc.groupby('Description')['Amount']
            .sum()
            .sort_values()  # Smallest (most negative) at top
            .reset_index()
        )
        # Only show if there are expenses for the month
        if not desc_sum.empty:
            fig_bar = px.bar(
                desc_sum,
                x='Description',
                y='Amount',
                orientation='v',  # Vertical bars
                title=f"Expenses by Description for {month}",
                labels={'Amount': 'Total Expenses ($)', 'Description': 'Description'},
                color='Amount',
                color_continuous_scale='Reds'
            )
            fig_bar.update_layout(
                yaxis_tickformat='$,.2f',
                xaxis_title="Description",
                yaxis_title="Total Expenses ($)",
                showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)
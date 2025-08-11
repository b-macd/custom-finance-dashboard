import streamlit as st
import pandas as pd
import plotly.express as px


st.title("Transfer Tracker")
st.markdown("Track and visualize your transfer transactions between accounts.")

# Multi-select for accounts to compare
selected_files = st.multiselect("Select account CSV files to track transfers:", st.session_state.dataframes.keys(), default=list(st.session_state.dataframes.keys()))

if len(selected_files) < 2:
    st.info("Select at least two accounts to visualize transfers.")
    st.stop()

# Load all selected files into a dictionary of DataFrames
dfs = {}
for fname in selected_files:
    df = st.session_state.dataframes[fname]
    df['Date'] = pd.to_datetime(df['Date'])
    dfs[fname] = df

# Combine all transactions into one DataFrame, add a column for account name
all_tx = pd.concat([
    df.assign(Account=fname) for fname, df in dfs.items()
], ignore_index=True)

# Filter for transfer transactions
transfer_tx = all_tx[all_tx['Category'].str.contains('Transfer', case=False)]

st.subheader("All Transfer Transactions")
st.dataframe(transfer_tx)

# Visualize transfers: Sankey diagram (money flow between accounts)
# Try to infer source/target from Description and Account
transfer_tx['Source'] = transfer_tx.apply(
    lambda row: row['Account'] if row['Amount'] < 0 else row['Description'], axis=1
)
transfer_tx['Target'] = transfer_tx.apply(
    lambda row: row['Description'] if row['Amount'] < 0 else row['Account'], axis=1
)

# Aggregate transfer amounts by Source/Target
sankey_data = transfer_tx.groupby(['Source', 'Target'])['Amount'].sum().reset_index()

# Prepare Sankey diagram
import plotly.graph_objects as go

sources = list(sankey_data['Source'].unique())
targets = list(sankey_data['Target'].unique())
labels = list(set(sources + targets))
label_map = {label: i for i, label in enumerate(labels)}

st.subheader("Matched Transfers Sankey (by Amount and Date)")

# Create a transfer key for matching: (abs(amount), date)
transfer_tx['Transfer_Key'] = list(zip(transfer_tx['Date'], transfer_tx['Amount'].abs()))

# Split outgoing and incoming transfers
outgoing = transfer_tx[transfer_tx['Amount'] < 0].copy()
incoming = transfer_tx[transfer_tx['Amount'] > 0].copy()

# Merge on Transfer_Key to find matches
matched = pd.merge(
    outgoing,
    incoming,
    on='Transfer_Key',
    suffixes=('_out', '_in')
)

# Only keep matches with different accounts
matched = matched[matched['Account_out'] != matched['Account_in']]

# Prepare Sankey data
sankey_matched = matched.groupby(['Account_out', 'Account_in'])['Amount_out'].sum().reset_index()

sources = list(sankey_matched['Account_out'].unique())
targets = list(sankey_matched['Account_in'].unique())
labels = list(set(sources + targets))
label_map = {label: i for i, label in enumerate(labels)}

import plotly.graph_objects as go

fig_matched = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
    ),
    link=dict(
        source=[label_map[src] for src in sankey_matched['Account_out']],
        target=[label_map[tgt] for tgt in sankey_matched['Account_in']],
        value=sankey_matched['Amount_out'].abs(),
        color="rgba(44, 160, 44, 0.7)"
    )
)])

fig_matched.update_layout(title_text="Matched Money Transfers Between Accounts (by Amount and Date)", font_size=12)
st.plotly_chart(fig_matched, use_container_width=True)

# Find matched keys
matched_keys = set(matched['Transfer_Key'])

# Unmatched outgoing transfers
unmatched_outgoing = outgoing[~outgoing['Transfer_Key'].isin(matched_keys)]
# Unmatched incoming transfers
unmatched_incoming = incoming[~incoming['Transfer_Key'].isin(matched_keys)]

# Prepare unmatched Sankey links
unmatched_outgoing_links = unmatched_outgoing[['Account', 'Description', 'Amount']]
unmatched_outgoing_links = unmatched_outgoing_links.rename(columns={'Account': 'Source', 'Description': 'Target', 'Amount': 'Value'})
unmatched_incoming_links = unmatched_incoming[['Description', 'Account', 'Amount']]
unmatched_incoming_links = unmatched_incoming_links.rename(columns={'Description': 'Source', 'Account': 'Target', 'Amount': 'Value'})

# Combine matched and unmatched links
all_links = pd.concat([
    sankey_matched.rename(columns={'Account_out': 'Source', 'Account_in': 'Target', 'Amount_out': 'Value'}),
    unmatched_outgoing_links,
    unmatched_incoming_links
], ignore_index=True)

# Prepare Sankey diagram
all_sources = list(all_links['Source'].unique())
all_targets = list(all_links['Target'].unique())
all_labels = list(set(all_sources + all_targets))
all_label_map = {label: i for i, label in enumerate(all_labels)}

fig_all = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=all_labels,
    ),
    link=dict(
        source=[all_label_map[src] for src in all_links['Source']],
        target=[all_label_map[tgt] for tgt in all_links['Target']],
        value=all_links['Value'].abs(),
        color="rgba(44, 160, 44, 0.7)"
    )
)])

fig_all.update_layout(title_text="All Money Transfers (Matched and Unmatched)", font_size=12)
st.plotly_chart(fig_all, use_container_width=True)

# Define additional merchant targets
merchant_targets = ["Amazon", "Target", "Paypal", "Costco", "Kroger"]

# Find transactions to these merchants (case-insensitive match in Description)
merchant_tx = all_tx[
    all_tx['Description'].str.lower().str.contains(
        '|'.join([m.lower() for m in merchant_targets])
    )
]

# Prepare merchant links (treat account as source, merchant as target)
merchant_links = merchant_tx[['Account', 'Description', 'Amount']].copy()
merchant_links = merchant_links.rename(columns={'Account': 'Source', 'Description': 'Target', 'Amount': 'Value'})

# Define categories for "Eating Out"
eating_out_categories = ["Fast Food", "Restaurants", "Coffee Shops", "Food & Dining"]

# Find transactions for "Eating Out"
eating_out_tx = all_tx[all_tx['Category'].isin(eating_out_categories)]

# Prepare links: account as source, "Eating Out" as target
eating_out_links = eating_out_tx[['Account', 'Amount']].copy()
eating_out_links['Target'] = "Eating Out"
eating_out_links = eating_out_links.rename(columns={'Account': 'Source', 'Amount': 'Value'})

# Combine all links: matched, unmatched, merchant, and "Eating Out"
all_links_expanded = pd.concat([
    sankey_matched.rename(columns={'Account_out': 'Source', 'Account_in': 'Target', 'Amount_out': 'Value'}),
    unmatched_outgoing_links,
    unmatched_incoming_links,
    merchant_links,
    eating_out_links[['Source', 'Target', 'Value']]
], ignore_index=True)

# Prepare Sankey diagram
all_sources_expanded = list(all_links_expanded['Source'].unique())
all_targets_expanded = list(all_links_expanded['Target'].unique())
all_labels_expanded = list(set(all_sources_expanded + all_targets_expanded))
all_label_map_expanded = {label: i for i, label in enumerate(all_labels_expanded)}

fig_expanded = go.Figure(data=[go.Sankey(
    node=dict(
        pad=80,
        thickness=30,
        line=dict(color="black", width=0.5),
        label=all_labels_expanded,
    ),
    link=dict(
        source=[all_label_map_expanded[src] for src in all_links_expanded['Source']],
        target=[all_label_map_expanded[tgt] for tgt in all_links_expanded['Target']],
        value=all_links_expanded['Value'].abs(),
        color="rgba(160, 44, 44, 0.7)"
    )
)])

fig_expanded.update_layout(title_text="All Transfers Including Key Merchant Expenditures", font_size=12, height=720)  # Increase height as needed

# Sankey diagram code remains the same
st.plotly_chart(fig_expanded, use_container_width=True)

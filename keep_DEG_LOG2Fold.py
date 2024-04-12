#This script will in the end keep only log2FC from rows that have at least one UpRegulated or DownRegulated in the value_log2FC.
#Values of log2FC between 1 and -1 were nullified as they do no meet DEG criteria. The output of this script is usefull to build
#heatmaps and to be used as source to analyse specific GO categories. Replace NAN for null in the input before running this.
#This script is the second, after ids_up_down_DEG.py

import pandas as pd

data = pd.read_csv("deseq2_fungi_hydric_DEG.tsv", sep='\t')

# Filter columns with headers containing "log2" and "adjusted"
filtered_cols = data.columns[data.columns.str.contains('vinifera|Swiss|UniProt|log2|adjusted', case=False)]
filtered_data = data[filtered_cols].copy()  # Create a copy to work with

# Find rows where none of the 'value_log' columns have 'UpRegulated' or 'DownRegulated'
value_log_cols = filtered_data.columns[filtered_data.columns.str.contains('value_log')]
condition_notdeg = ~filtered_data[value_log_cols].isin(['UpRegulated', 'DownRegulated']).any(axis=1)

# Apply the condition for columns containing 'log2FC'
log2_cols = filtered_data.columns[filtered_data.columns.str.startswith('log2FC')]
filtered_data[log2_cols] = filtered_data[log2_cols].apply(lambda col: col.apply(lambda x: 'null' if isinstance(x, float) and -1 < x < 1 else x))

# Move the loop for handling 'value_log2FC' columns here
value_log2FC_cols = filtered_data.columns[filtered_data.columns.str.startswith('value_log2FC')]
for value_col, log_col in zip(value_log2FC_cols, log2_cols):
    null_condition = filtered_data[value_col].isnull()
    filtered_data[log_col] = filtered_data.apply(
        lambda row: 'null' if null_condition[row.name] else row[log_col],
        axis=1
    )

# Remove rows that meet the 'NotDEG' condition
filtered_data = filtered_data[~condition_notdeg]

# Filter columns again to keep only "V_vinifera_ID" and "log" columns
final_filtered_cols = filtered_data.columns[filtered_data.columns.str.startswith(('V_vinifera_ID', 'Swiss', 'UniProt', 'log'))]
filtered_data = filtered_data[final_filtered_cols]

# Save to CSV
filtered_data.to_csv('filter_deseq2_fungi_hydric_DEG.tsv', sep='\t', index=False, na_rep='null')

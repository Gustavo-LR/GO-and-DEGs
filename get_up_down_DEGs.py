#This script is usefull to get UpRegulated and DownRegulated seqIDs from a file already filtered with only log2FC values
#of DEGs, seqID and annotations. The values between -1 and 1 were purged by keep_DEG_LOG2Fold.py (which provides the input for this script)

import pandas as pd

# Read the TSV file into a dataframe
df = pd.read_csv('filter_deseq2_fungi_hydric_DEG.tsv', delimiter='\t')

# Identify columns containing "log2FC"
log2FC_columns = [col for col in df.columns if 'log2FC' in col]

# Separate positive and negative values for each log2FC column
for col in log2FC_columns:
    col_name = col.replace('log2FC_', '')  # Remove the 'log2FC_' prefix
    positive_ids = df['V_vinifera_ID'][df[col] > 0]
    negative_ids = df['V_vinifera_ID'][df[col] < 0]

    # Create filenames for positive and negative IDs
    positive_filename = f'upregulated_{col_name}_seqID.txt'
    negative_filename = f'downregulated_{col_name}_seqID.txt'

    # Write positive IDs to the respective file
    positive_ids.to_csv(positive_filename, index=False)

    # Write negative IDs to the respective file
    negative_ids.to_csv(negative_filename, index=False)

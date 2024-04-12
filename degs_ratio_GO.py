import pandas as pd

# This script will create a new column after a column starting with upregulated and finishing with _count, and fill
# this new column with the division of the upregulated_count value by the sum of upregulated_count and downregulate_count
# values, to obtain the % of upregulated. This script also purges up/downreg_count with only zeros.
# Read the input file
df = pd.read_csv("ancestor_fungi_hydric_comb_DEG_modified.tsv", sep='\t')

# Iterate over the columns and duplicate those containing "PI_", in this case all treatment columns contains PI_
for column in df.columns:
    if column.startswith("upregulated") and column.endswith("_count"):
        new_column = "%" + column
        df.insert(df.columns.get_loc(column) + 1, new_column, df.iloc[:, df.columns.get_loc(column)] / (df.iloc[:, df.columns.get_loc(column)] + df.iloc[:, df.columns.get_loc(column) - 2]))

# Remove rows where all the columns ending with "seqID_count" contain zeros
zero_columns = [col for col in df.columns if col.endswith("seqID.txt_count")]
df = df.loc[~(df[zero_columns].sum(axis=1) == 0)]

# Write the modified DataFrame to a new file
df.to_csv("ancestor_fungi_hydric_comb_DEG_final.tsv", sep='\t', index=False)

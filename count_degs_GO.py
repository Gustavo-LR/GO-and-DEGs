import pandas as pd

# This script will create a new column after every treatment column and count the number of seqIDs using the comma separator as reference
# Read the input file
df = pd.read_csv("ancestor_fungi_hydric_DEG_edit.tsv", sep='\t')

# Iterate over the columns and duplicate those containing "PI_", in this case all treatment columns contains PI_
for column in df.columns:
    if "PI_" in column:
        new_column = column + "_count"
        df.insert(df.columns.get_loc(column) + 1, new_column, df[column].apply(lambda x: len(str(x).split(',')) if pd.notna(x) else 0))

# Write the modified DataFrame to a new file
df.to_csv("ancestor_fungi_hydric_DEG_modified.tsv", sep='\t', index=False)

#this script will generate a table containing the seqID in the first colunm and all go terms
#(specifc term and all its ancestors) in the second column. The two inputs are
#a bl2go annotation table containing only the seqID and BP GOIDs (comma sepparated with no spaces,
#and lines without GO terms removed, in this script data) and another is the output from
#fetch_ancestors.R, which is one column with the GOID and another colunm with the GOID and
#every ancestor term (comma delimited, without spaces and with the ,all removed, data2). This script is
#used by go_ancestor_to_DEG_4.py. Sometimes, go.db and bl2GO databases have some differences
#and the output from fetch_ancestors.R doesn't include every entry from bl2GO, add those manually
#without the ancestorship (or do the ancestorship manually, which is quite laborious, not recommended).

import pandas as pd

# Read the first dataframe
data = pd.read_csv("pn40024_t2t_cds_all_nr_table_clean_edit.txt", sep='\t')

# Split the 'GOIDs' column into multiple columns based on commas
data['GOIDs'] = data['GOIDs'].str.split(',')

# Explode the dataframe to have one row per term
data = data.explode('GOIDs')

# Read the second dataframe with a different header
data2 = pd.read_csv('pn40024_t2t_cds_all_nr_BP_goID_ancestor.tsv', sep='\t')
data2_dict = dict(zip(data2['GO_Term'], data2['Ancestor_Terms']))

# Map the terms individually
data['GO_Ancestors'] = data['GOIDs'].map(data2_dict)

# Aggregate the mapped values back into a single list for each original row
result = data.groupby('SeqName')['GO_Ancestors'].agg(list).reset_index()

# Create a new DataFrame with desired columns
final_result = pd.DataFrame({
    'SeqName': result['SeqName'],
    'GO_Ancestors': result['GO_Ancestors'].apply(lambda x: ','.join(x))
})

# Save the result to a new file
final_result.to_csv('pn40024_t2t_cds_all_nr_table_clean_BP_ancestor.tsv', sep='\t', index=None, na_rep='NAN')

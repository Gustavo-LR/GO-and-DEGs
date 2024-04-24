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

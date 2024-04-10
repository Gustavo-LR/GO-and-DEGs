#This script identifies DEGs from a DESEq2 table output. First, it will double the columns containing log2FC and adjustedP
#and include a prefix value_ to modify according to the rules below. First (conditions1), if value_adjustedP is smaller than 0.05, the value will
#be replaced by Significative. Then, a second rule will be applied (conditions): if the value_log2FC is greater than 1, replace by UpRegulated,
#if smaller than -1, replace by DownRegulated, if between 1 and -1, NotDEG. Finally, the cutoff of value_adjustedP is applied to value_log2FC:
#in the same line if value_adjusted is null, the value from value_log2FC will be replace by null as well. This script can be modified to be more or less
#permissive by changing conditions and conditions1 values.

import pandas as pd
import numpy as np

data = pd.read_csv("deseq2_fungi_hydric_effect.tsv", sep='\t')
df = pd.DataFrame(data)

# Double columns containing 'log2FC' and 'adjustedP' and add prefix 'value_'
log2_cols = df.columns[df.columns.str.contains('log2FC')]
adjusted_cols = df.columns[df.columns.str.contains('adjustedP')]

for col in log2_cols:
    new_col = f"value_{col}"
    df.insert(df.columns.get_loc(col) + 1, new_col, df[col])

for col in adjusted_cols:
    new_col = f"value_{col}"
    df.insert(df.columns.get_loc(col) + 1, new_col, df[col])

def conditions1(x):
    if x < 0.05:
        return 'Significative'
    else:
        return 'null'

func1 = np.vectorize(conditions1)
copy_cols = df.columns[df.columns.str.contains('value_adjusted')]
DEG_class1 = df[copy_cols].applymap(conditions1)
df[copy_cols] = DEG_class1

def conditions(x):
    x = float(x)
    if x > 1:
        return "UpRegulated"
    elif x < -1:
        return "DownRegulated"
    else:
        return "NotDEG"

func = np.vectorize(conditions)
copy_cols1 = df.columns[df.columns.str.contains('value_log2')]
DEG_class2 = df[copy_cols1].applymap(conditions)
df[copy_cols1] = DEG_class2

null_idx = np.where(df == 'null')

for i, j in zip(null_idx[0], null_idx[1]):
    if j > 0:
        df.iloc[i, j - 2] = 'null'



df.to_csv('deseq2_fungi_hydric_effect_DEG.tsv', sep='\t', index=False, na_rep='null')
print(df)

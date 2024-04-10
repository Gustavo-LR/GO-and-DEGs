#This script uses a input file with the GOID, Go TERM and the seqID for each treatment, and split
#the DESEq2 table with log2fold change values according to each GO TERM. Thus, it is possible to see
#the log2fold change values of each GO category, and also the Uni/SwissProt annotation for the DEGS
#in that category.

#file content: filter_deseq2_fungi_hydric_DEG.tsv is the file containing the seqID, annotation and log2fold change values
#and ancestor_fungi_hydric_DEG_modified.tsv is the file with the seqIDs DEGs sorted by GO category.

import pandas as pd
import re

def sanitize_filename(filename):
    #Sanitize filename by removing forbidden characters for filenames, which are abundant in GO TERM
    return re.sub(r'[\\/*?:"<>|]', '', filename)

def process_table(input_file):
    # Read the table
    df = pd.read_csv(input_file, delimiter='\t')

    for index, row in df.iterrows():
        raw_output_file = row.iloc[1]  # Get the name from the second column
        output_file = sanitize_filename(raw_output_file) + '.tsv'  # Add .tsv extension

        seq_columns = [col for col in df.columns if col.endswith('seqID')]  # Select columns ending with seqID
        seq_data = df.loc[index, seq_columns]  # Get data from selected columns for the current row
        seq_data = seq_data.dropna().astype(str)  # Drop NaN values and convert to string
        seq_ids = "\n".join(",".join(seq_data).split(","))  # Join by comma, then split by comma, and separate by new line
        unique_seq_ids = sorted(set(seq_ids.split("\n")))  # Remove duplicates and sort
        unique_seq_ids = [re.sub(r'\.3$', '', seq_id) for seq_id in unique_seq_ids] #remove .3 suffix from seqid

        with open('filter_deseq2_fungi_hydric_DEG.tsv', 'r') as filter_file:
            # Write the first line (header) from filter_file to the output
            first_line = next(filter_file).strip()
            with open(output_file, 'a') as f:
                f.write(first_line + '\n')

            # Write subsequent lines based on matching IDs
            for line in filter_file:
                if any(seq_id in line for seq_id in unique_seq_ids):
                    with open(output_file, 'a') as f:  # Change 'w' to 'a' for append mode
                        f.write(line.strip() + '\n')  # Write the line followed by a newline

if __name__ == "__main__":
    input_file = 'ancestor_fungi_hydric_DEG_modified.tsv'
    process_table(input_file)

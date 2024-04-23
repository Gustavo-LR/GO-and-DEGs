import os

#This script will replace GO terms from the second colunm of a input for the corresponding IDs from the genes

#list_file_path contains the list of files containing the GO terms with ancestors for each treatment, separating upregulated and downregulated,
#generated by go_ancestor_to_DEG.py

#in the end, just use the command paste with all the output files form this script and the result is a .tsv containing the GO terms
#and the IDs from the genes side-by-syde. vitis_vinifera_nr_BP_GO_ancestor.txt is the second colunm from *_ancestor.tsv from
#fetch_abcestors.R, after replacing commas for new line and sort uniq, i.e. 
# cut -f2 vitis_vinifera_nr_go_table_clean_BP.txt | tr "," "\n" | sed -re 's/\s+$//' | sort | uniq > vitis_vinifera_nr_BP_GO.txt

#this script is the 5th, after go_ancestor_to_DEG.py


# Read content from the list file and create a list of input file paths
list_file_path = 'vitis_vinifera_go_table_BP_ancestor_list.txt'
with open(list_file_path, 'r') as list_file:
    input_file_paths = [line.strip() for line in list_file]

# Iterate through each input file path
for file1_path in input_file_paths:
    # Generate the output file name based on the input file name
    output_file_name = file1_path[36:]

    # Read content from file1 and create a dictionary mapping GO terms to sequences
    go_dict = {}
    with open(file1_path, 'r') as file1:
        for line in file1:
            seq_id, go_terms = line.strip().split('\t')
            go_terms_list = go_terms.split(',')
            for go_term in go_terms_list:
                if go_term not in go_dict:
                    go_dict[go_term] = []
                go_dict[go_term].append(seq_id)

    # Read content from file2 and create a list of GO terms
    file2_path = 'vitis_vinifera_nr_BP_GO_ancestor.txt'
    with open(file2_path, 'r') as file2:
        go_terms_to_search = [line.strip() for line in file2]

    # Create a dictionary to store the results
    result_dict = {go_term: list(set(go_dict.get(go_term, []))) for go_term in go_terms_to_search}

    # Write the results to the output file with header
    output_file_path = f'ancestor_{output_file_name}'
    with open(output_file_path, 'w') as file3:
        file3.write("GO Term\t" + output_file_name + "\n")  # Writing header
        for go_term, seq_ids in result_dict.items():
            file3.write(f"{go_term}\t{','.join(seq_ids)}\n")

    # Use sed to remove the second line from the output file
    os.system(f"sed -i '2d' {output_file_path}")


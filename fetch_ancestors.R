#This script uses GO.db to inform all the ancestors terms of a GO term list. The input is a list of GO terms,
#and the output is a .tsv file containing all the ancestor GO terms for each GO term informed in the input.
#This is important to collapse the GO terms from blast2go annotation in superior categories, and it is
#vital to group the genes in superior GO categories and have a better overview of the biological process.

library(GO.db)

#file_list.txt contains only vitis_vinifera_nr_BP_GO but it is possible to use for multiple files.
#This input file cointains all the GO IDs from blast2go reference genome annotation
# Read the list of prefixes from the text file
prefix_list <- readLines("file_list.txt")

# Iterate over the list of prefixes
for (term_BP in prefix_list) {
  # Read the GO terms from the text file, and add .txt to match the input files
  go_terms <- readLines(paste0(term_BP, ".txt"))

  # Convert the GOBPANCESTOR object to a list
  ancestor_list <- as.list(GOBPANCESTOR)

  # Create an empty data frame to store the results
  result_df <- data.frame(GO_Term = character(), Ancestor_Terms = character(), stringsAsFactors = FALSE)

  # Iterate over the GO terms and retrieve their ancestor terms
  for (term in go_terms) {
    term <- trimws(term)
    if (term %in% names(ancestor_list)) {
      ancestor <- ancestor_list[[term]]
      if (length(ancestor) > 0) {
        ancestor <- paste(ancestor, collapse = ", ")  # Collapse the ancestor terms into a single string
        result_df <- rbind(result_df, data.frame(GO_Term = term, Ancestor_Terms = paste(term, ancestor, sep = ", "), stringsAsFactors = FALSE))
      }
    }
  }

  # Remove ", NA" from the Ancestor_Terms column
  result_df$Ancestor_Terms <- gsub(", NA", "", result_df$Ancestor_Terms)

  output_file <- paste0(term_BP, "_ancestor.tsv")
  write.table(result_df, file = output_file, sep = "\t", row.names = FALSE, quote = FALSE)
}


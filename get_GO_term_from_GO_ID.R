# This R script will use a single colunm input with GO ids and output a two colunms file with the GO ids and GO term name
library(GO.db)

# Read the GO terms from the file (excluding the header), this is a list of GO ids
go_terms <- readLines("ancestor_fungi_hydric_DEG_go_ids.txt")[-1]

keys <- head(keys(GO.db))

result_df = select(GO.db, keys=go_terms, columns=c("TERM"),
      keytype="GOID")

# Write the result data frame to a file
write.table(result_df, file = "ancestor_fungi_hydric_DEG_go_ids_mapped.txt", sep = "\t", quote = FALSE, row.names = FALSE)

#This script uses GO.db to fetch the complete hierarchy defined at parent_goid.
# Load necessary library
library(GO.db)

# Convert the object to a list
xx <- as.list(GOBPCHILDREN)  # Use GOBPCHILDREN for Biological Process ontology

# Remove GO identifiers that do not have any children
xx <- xx[!is.na(xx)]

# Define the GO term of interest
parent_goid <- "GO:0006952"

# Open a connection to a file
file_conn <- file("go_defense_hierarchy.txt", "w")

# Function to print GO term details and its children to the file
print_go_terms_and_children <- function(goid, depth = 0) {
  indent <- paste(rep("\t", depth), collapse = "")
  writeLines(paste(indent, goid, "\t", Term(GOTERM[[goid]]), "\n"), file_conn)
  
  if (goid %in% names(xx)) {
    child_goids <- xx[[goid]]
    for (child_goid in child_goids) {
      print_go_terms_and_children(child_goid, depth + 1)
    }
  }
}

# Check if the parent GO term has children
if (parent_goid %in% names(xx)) {
  # Get the children GO identifiers for the specified parent GO term
  goids <- xx[[parent_goid]]
  
  # Loop through each child GO identifier and print its details and their children
  for (goid in goids) {
    print_go_terms_and_children(goid)
  }
} else {
  writeLines(paste("The GO term", parent_goid, "does not have any children or is not found in the GOBPCHILDREN object.\n"), file_conn)
}

# Close the file connection
close(file_conn)

#!/usr/bin/env Rscript

###### GTF files: 1-based
###### Bed files: 0-based

options(stringsAsFactors = FALSE)

############### Libraries: 

suppressPackageStartupMessages(library(optparse))
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(reshape2))

##### Option list using Python's style: 

option_list <- list(
  
  make_option(c("-i", "--input"), type = "character", default = "stdin",
              help = "input file [default=%default]", metavar = "character"),
  make_option("--header", default = FALSE, 
              help = "the input file has header [default=%default]"),
  make_option(c("-o", "--output"), type = "character", default = "Gtf.to.Bed.out.bed",
              help="output file name. Must have a bed extension (e.g. 'What.ever.bed') [default= %default]", 
              metavar="character"),
  make_option(c("-t", "--type"), type = "character", default = "long",
              help = "This script can convert GTF file into 12 fields (long) or 4 fields (short) [default= %default]", 
              metavar = "character")
  
)

opt_parser <-  OptionParser(option_list=option_list)
opt <- parse_args(opt_parser)

############ Read the input data


if (opt$input == "stdin") {
  
  Input <- read.delim(file("stdin"), h=opt$header)
  
} else {
  
  Input <- read.delim(opt$input, h=opt$header)
  
}

### Debugging in RStudio: 
# Input <- read.delim("/users/rg/ramador/D_me/RNA-seq/ncRNAs/lncRNA_Identification/Final_Agreement_lncRNAs/TransDecoder/Files/tmp.Transcripts.lncRNA.2845.GTF.txt",
#                     header = opt$header)

if(opt$type == "long"){
  
  ### Change the GTF 1-based count to BED 0-based
  ### Formula: 0-based: start = start-1; end = end
  
  ### 1) Chr, start, end:
  
  Bed_file <- Input[,c(1,4,5)]
  
  Bed_file$V4 <- (Bed_file[,2] -1)
  
  ### 4) ID 
  
  ID <- strsplit(Input[,9], split = ";", fixed = TRUE) %>% lapply(function(x){y <- x[2]}) %>% unlist()
  
  ID <- sub(" ", "", ID) 
  
  ID <- colsplit(ID, " ", c("Type", "ID"))
  
  Bed_file$ID <- ID$ID
  
  rm(ID)
  
  ### 5) A score between 0 and 1000; 6th filed of the original GTF 
  
  Bed_file$V6 <- Input[,6]
  
  ### 6) Strand
  
  Bed_file$Strand <- Input[,7] 
  
  ### 7) thickStart; 2nd field 
  
  Bed_file$Second_field <- Input[,2]
  
  ### 8) thickEnd; third field  
  
  Bed_file$Third_field <- Input[,3]
  
  ### 9) itemRgb
  
  Bed_file$V8 <- Input[,8]
  
  ### 10) blockCount; Gene_ID
  
  Gene_ID <- strsplit(Input[,9], split = ";", fixed = TRUE) %>% lapply(function(x){y <- x[1]}) %>% unlist()
  Gene_ID <- colsplit(Gene_ID, " ", c("Type", "ID") )[,2]
  
  Bed_file$Gene_ID <- Gene_ID
  
  ### 11) blockSizes; Transcript_name 
  
  Transcript_name <- strsplit(Input[,9], split = ";", fixed = TRUE) %>% lapply(function(x){y <- x[4]}) %>% unlist()
  Transcript_name <- sub(" ", "", Transcript_name)
  
  Bed_file$Transcript_name <- colsplit(Transcript_name, " ", c("Type", "ID"))[,2]
  
  ### 12) blockStarts
  
  Bed_file$V12 <- Input[,6]
  
  write.table(Bed_file, file = opt$output, sep = "\t", quote = FALSE, col.names = FALSE, row.names = FALSE)
  
  
} else if (opt$type == "short"){
  
  ### Change the GTF 1-based count to BED 0-based
  ### Formula: 0-based: start = start-1; end = end
  
  ### 1) Chr, start, end:
  
  Bed_file <- Input[,c(1,4,5)]
  
  Bed_file$V4 <- (Bed_file[,2] -1)
  
  ### 2) ID 
  
  ID <- strsplit(Input[,9], split = ";", fixed = TRUE) %>% lapply(function(x){y <- x[2]}) %>% unlist()
  
  ID <- sub(" ", "", ID) 
  
  ID <- colsplit(ID, " ", c("Type", "ID"))
  
  Bed_file$ID <- ID$ID
  
  cat("The ID used is the 'Transcript_ID'", "\n")
  cat("GTF file into 'short' Bed file", "\n")
  
  write.table(Bed_file, file = opt$output, sep = "\t", quote = FALSE, col.names = FALSE, row.names = FALSE)
  
}





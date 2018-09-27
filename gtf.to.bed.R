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
  make_option(c("-f", "--field"), type = "character", default = 2,
              help = "The second field ('Transcript_ID') is used to produce the Bed file [default= %default]"),
  make_option(c("-o", "--output"), type = "character", default = "Gtf.to.Bed.out.bed",
              help="output file name. Must have a bed extension (e.g. 'What.ever.bed') [default= %default]", 
              metavar="character")
  
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

### Change the GTF 1-based count to BED 0-based
### Formula: 0-based (BED_file): start = start-1; end = end
### More-information: http://genome.ucsc.edu/blog/the-ucsc-genome-browser-coordinate-counting-systems/

### 1) Chr, start, end:
  
Bed_file <- Input[,c(1,4,5)]
  
Bed_file$V4 <- (Bed_file[,2] -1)
  
### 2) ID 

  ID <- strsplit(Input[,9], split = ";", fixed = TRUE) %>% 
    lapply(function(x){y <- x[ as.numeric(opt$field) ]; trimws(y) }) %>% unlist() 
  
ID <- colsplit(ID, " ", c("Type", "ID"))
  
Bed_file$ID <- ID$ID
  
cat("The ID:", opt$field ,"was used to produce the Bed_file", "\n")
cat("GTF file into Bed file", "\n")
  
write.table(Bed_file, file = opt$output, sep = "\t", quote = FALSE, col.names = FALSE, row.names = FALSE)
  




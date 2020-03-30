### Generate a tmp plot of 100 from 182 DGE lncRNA
### March 30th 2020
### Libraries: 
library(tidyverse)
library(magrittr)
library(ggrepel)
options(stringsAsFactors = F)
setwd('/users/rg/ramador/D_me/RNA-seq/Conservation.Analysis/sequence_conservation/MAFs/analysis_MAFs_182_Genes_lncRNA_DGE/')
# Set global ggplot theme: 
theme_set(theme_light())

### Input data: 
maf_table <- read_tsv("Data//Alignments.output.table", col_names=F) %>%
    select(-X2)
dge <- read_tsv("Data//DGE.lncRNA.india.crg.genomiclocation.all.PCG.pairs.exonic.cutoff.mRNAs.expression.NA.0.GC.Descr.L3.cat.lincRNA.tsv")
gene_length <- read_tsv("Data//GeneID.Gene_Name.Gene_Type.Length.tsv") %>%
    select(Gene_ID, Length)
number_exons <- read_tsv("Data//All.annotated.lncRNAs.with.all.info.v1.tsv") %>%
    select(Gene_ID, Number_isoforms, Mean_isoform_length, Mean_number_exons)


### Obtain length of DGE:
dge %<>% left_join(., gene_length, by="Gene_ID") %>%
    rename(lncRNA_length=Length) %>% 
    select(Gene_ID:Chr,lncRNA_length , L3:phastCons124way)

## write.table(dge, file="Results/DGE.lncRNA.india.crg.genomiclocation.all.PCG.pairs.exonic.cutoff.mRNAs.expression.NA.0.GC.Descr.L3.cat.lincRNA.length.tsv",
##             row.names = F, col.names = T, quote=F, sep="\t")

## dge %>% filter(lncRNA_length < 199) %>%
##     select(Gene_Name, lncRNA_length, type, location, direction)

colnames(maf_table)[c(1:3)] <- c("Gene_ID", "Number_sps", "Aligned_bases")

lncRNAs <- dge %>% distinct(Gene_ID, .keep_all = TRUE) %>%
    select(Gene_ID, Gene_Name, lncRNA_length, type, location)


### Do the merge: Percentage of alignment >= 50% and in more than 8 sps

df_plot <- maf_table %>% inner_join(., lncRNAs, by="Gene_ID") %>%
    select(Gene_ID, Gene_Name, Number_sps:Aligned_bases ,
           lncRNA_length, type, location) %>%
    mutate(percentage_alig=round(Aligned_bases/lncRNA_length,digits=2)) %>%
    arrange(desc(percentage_alig)) %>%
    select(Gene_ID:Number_sps, percentage_alig, type:location) %>%
    mutate(percentage_alig=ifelse(percentage_alig >= 1,
                                  1, percentage_alig)) %>%
    mutate(type=str_to_title(type)) %>%
    mutate(highlight_color=ifelse(
               percentage_alig >= 0.5 & Number_sps >= 8,
               "yes", "no")) %>%
    mutate(Conservation= ifelse(highlight_color == "yes", Gene_Name, "")) %>%
    left_join(., number_exons, by="Gene_ID") 
    

## write.table(df_plot, file = "Results/tmp.df.plot.MAF.tsv",
##             sep="\t", quote = F, row.names=F, col.names = T)


##### Plot: 
## pdf(file="tmp.MAF.pdf", width=15, height = 8.7)

ggplot(data=df_plot, aes(percentage_alig,Number_sps, label= Conservation))+
    geom_point(aes(color=highlight_color))+facet_grid(. ~ type)+
    geom_text_repel()+
    xlab("aligned bases/ length alignment")+
    ylab("Number of aligned species")+
    scale_y_continuous(breaks = seq(0, 27, 3))+
    theme(strip.text = element_text(size = 15),
          axis.text.y = element_text(face = "bold"),
          axis.text.x = element_text(face = "bold"),
          axis.title.y = element_text(face="bold"),
          axis.title.x = element_text(face="bold"),
          legend.position = "none")+
    scale_color_manual(values = c("black", "red"))

dev.off()



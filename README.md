# Utils

### Content:

1. [Rows into columns](#rows)
2. [Print a range of fields](#interval)
3. [Convert GTF into a Bed file](#convert)
4. [DNA reverse complementary](#complementary)
5. [Flybase Orthology relationship](#ortho)
6. [Synteny analysis](#synteny)
7. [Convert a txt file into a csv](#csv)
8. [Merge all Gene-Expression values from the grape-nf pipeline](#ge)
9. [QC_Bam.files](#qc)
10. [Obtain a window around the TSS of some genes](#tss)
11. [GTF analysis](#gtf)

## 1) <a id='rows'></a> Rows into columns:

*rows.to.columns.count.sh*

**Description:**

Receives rows and convert them into columns and count them

**Usage:**

```{r}

head -1 some_file.txt | Utils/rows.to.columns.count.sh

```
**Example of output:**

<pre>
    Rows to Columns script:
    -----------------------

1   GENE
2   EVENT
3   COORD
4   LENGTH
5   FullCO

    End of the script
    -----------------
</pre>

## 2) <a id='interval'></a> Print a range of fields

*Print.fields.interval.awk*

**Description:**

Some times you have a tab separated file and you want to print a interval of fields using **awk** and it is prone to errors to type manually the fields using the following code:

```{r}

awk -F "\t" '{print $2, "\t", $3, "\t", $4}' file.txt

```
**Usage:**

```{r}

awk -v start=2 -v end=5 -f Utils/Print.fields.interval.awk  file.txt

```
With the example above it will print the fields from *2* until *5*

## 3) <a id='convert'></a> Convert GTF into a Bed file

*gtf.to.bed.R*

**Description:**

Within GTF files the 4th and 5th fields are the start and end of a genomic feature (*gene, transcript, exon, etc.*). However *GTFs* are **1-based (closed intervals)** whereas *Beds* are **0-counted (half-open intervals)**. This script does the conversion and prints the Bed file. Also it can calculate the **length** of a genomic features (*gene, transcript, exon, etc. --length=TRUE*).

For ID printing default is 2 (the second feature of the **9th** field of a GTF file) this can be changed, for example 1 if you want *Gene_ID*, if 9th file of the GTF file is the following:

| gene_id (1)  |  gene_symbol (2) |  transcript_id (3) |  transcript_symbol (4)  |
|----------|:-------------:|------:| ------:|
| "FBgn0031208" | "CG11023" | "FBtr0300689" | "CG11023-RB" |

**Usage:**

```{r}

cat GTF.file.gtf | Utils/gtf.to.bed.R

```
## 4) <a id='complementary'></a> DNA reverse complementary

*DNA.reverse.complementary.py*

**Description:**

The aim of this script is to change the direction of a DNA sequence from 5'-3' to 3'-5' and vice versa.

**Usage:**

```{r}

cat DNA.sequence.negative.strand.fasta | Utils/DNA.reverse.complementary.py

```
## 5) <a id='ortho'></a> Flybase Orthology relationship

*Flybase_orthoParalogs.py*

*Written in Python 3.5.4*

**Description:**

Script to create a file including all orthology relationships for the 4 fly species [*D_me*, *D_sechelia* (phylogenetically close), *D_persimilis* (halfway), & *D_willistoni* (far away)]

**WARNING:** prints all orthologs, including paralogs; paralogs are assigned with the same *myID*

**5.1) gene_list:** one column with gene_id like: FBgn0031208<br>
**5.2) orthologs_list:** obtained from the [Flybase](http://flybase.org/)

```{r}

python Flybase_orthoParalogs.py gene_list orthologs_list output_name

```
**Example output:**

| D_me  |  D_sec | D_per |  D_wil  |  myID |
|----------|:-------------:|------:| ------:| ------:|
| FBgn0031208				 | FBgn0177630 | FBgn0150621  | FBgn0212170 | myID1 |
| 		FBgn0031208		 | FBgn0177629 | FBgn0150620  | FBgn0212170 | myID1 |
| FBgn0031208	| FBgn0177629 | FBgn0160043  | FBgn0212170 | myID1  |
| 	FBgn0002121		 | FBgn0171620 | FBgn0151538  | FBgn0226562  | myID2 |
| 	FBgn0031209			 | FBgn0171619 | FBgn0151527  | FBgn0218492 | myID3 |

## 6) <a id='synteny'></a> Synteny analysis

*synteny_Flies.4sp.py*

*Written in Python 3.5.4*

**Description:**

```{r}

python synteny_Flies.4sp.py  dme_geneorder.list.txt\
dpse.gene.order.list.txt\
Orthologs.out\
Out.synteny.txt\
3 3 1 'yes'

```
## 7) <a id='csv'></a> Convert a txt file into a csv

*convert.txt.to.csv.py*

*Written in Python 3.5.4*

**Description:**

```{r}

cat file.txt | python ~/Utils/convert.txt.to.csv.py

cat file.txt | python ~/Utils/convert.txt.to.csv.py --output="Important.file.csv"


```
## 8) <a id='ge'></a> Merge all Gene-Expression values from the grape-nf pipeline

*generate.ExpressionMatrix.py* <br>
*Written in Python.3.5*

**Description:**

When you run the [grape-nf](https://github.com/guigolab/grape-nf) pipeline you obtain a file called: **pipeline.db** which it contains the description of results and their *absolute file path* . In order to merge all the results of quantification (RSEM: gene/transcript-expression) in **one dataframe** use the script: *generate.ExpressionMatrix.py* as is shown below:

### 8.1) To obtain expression values in TPMs:

```{r}

~/Utils/generate.ExpressionMatrix.py --input=pipeline.db

```
### 8.2) To obtain expression values in FPKMs:

```{r}

~/Utils/generate.ExpressionMatrix.py --input=pipeline.db --type=FPKM

```

### 8.3) To obtain expression values in Counts:

```{r}

~/Utils/generate.ExpressionMatrix.py --input=pipeline.db --type=Count

```


## 9) <a id='qc'></a> QC_Bam.files

This folder contains 4 scripts to obtain QC of aligned **bam** files. <br>
The whole pipeline relies that input file has to be called: **input_bamQC.tsv** if not it chrashes.

### 9.1) Input file

If you just run [grape-nf](https://github.com/guigolab/grape-nf) run: *bamqc_input.py* in the following way:

```{r}

python ~/Utils/QC_Bam.files/bamqc_input.py pipeline.db\
input_bamQC.tsv

```
### 9.2) QC

### [Qualimap:](http://qualimap.bioinfo.cipf.es/)

*Qualimap_array.sh*: job array

*Description:* You don't need to worry to create cluster_out folder or any type of subdirectory. Uses the current directory so no absolute paths are needed.

*Modify:*

* **1)** Must modify: **-t** according of the number of bam files that you want to analyze.
* **2)** You can modify the number of parallel jobs by modify: **-tc**
* **3)** You can also modify the **gtf file**, currently is using: **gtf dm6 r6.29**

```{r}

qsub Qualimap_array.sh

```
### [Picard](https://broadinstitute.github.io/picard/)

*Picard_array.sh*: **CollectAlignmentSummaryMetrics** and **CollectGcBiasMetrics** <br/>
*Picard_array.sh*: job array

*Description:* Run in the same folder as *Qualimap_array.sh*. And don't worry for the rest.

*Modify:*
* **1)** Must modify: **-t** according of the number of bam files that you want to analyze.
* **2)** You can modify the number of parallel jobs by modify: **-tc**
* **3)** You can modify **reference genome**.

```{r}

qsub Picard_array.sh

```
### 9.3) Merge all the QC results

*merge.QC_files.sh*

*Description:* this is not a array script you need to run it. The suffix of the input files are: *_metrics.txt*, *_bamqc.txt* and *_GC_summary.txt*. The final output filename is: **QC_Data.csv**

* **1)** Copy the **header** file
Modify:  **path**. <br/>




## 10) <a id='tss'></a> Obtain a window around the TSS

*ObtainWindow_TSS.bed.py* <br/>
*Written in Python.3.5*

**Description:**

It receives as an input **1)** a bed file, **2)** a window interger number, and **3)** the outputname bed file. In the example below it uses a 50 bp window around the TSS of all genes within bed file to obtain the promoters bed file.

```{r}

python ~/Utils/ObtainWindow_TSS.bed.py input_BedFile.bed 50 output_name.bed

```

## 11) <a id='gtf'></a> GTF analysis:

*GTF.analysis.GeneIDName.py*

**Description:**

This script has two options either **gene** or **transcript**. For **gene** from a gtf file you obtain: gene id, gene name, gene type, gene length and strand. For **transcript** you obtain gene id, gene name, transcript id, transcript name, transcript type (it is the same as gene type), transcript length and strand.

**Gene Usage:**

```{r}

/Utils/GTF.analysis.GeneIDName.py  --input=dme.r6.29.gtf --output=gene.example.tsv

```
**Transcript Usage:**

```{r}

Utils/GTF.analysis.GeneIDName.py  --input=dme.r6.29.gtf --output=transcript.example.tsv --type=transcript

```

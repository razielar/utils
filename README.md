# Utils

### Content:

1. [Rows into columns](#rows)
2. [Print a range of fields](#interval)
3. [Convert GTF into a Bed file](#convert)
4. [DNA reverse complementary](#complementary)

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

# Utils

### Content:

1. [Rows into columns](#rows)
2. [Print a specific field interval](#interval)

## 1) <a id='rows'></a> Rows into columns:

Description:

Receives rows and convert them into columns and count them

Usage:

```{r}

head -1 some_file.txt | Utils/rows.to.columns.count.sh

```
Example of output:

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

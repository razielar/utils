"""Generate UCSC tracks."""

import sys
import argparse

parser = argparse.ArgumentParser(
    description='Generate UCSC tracks for copy/paste')

parser.add_argument("-p", "--path",
                    help="folder where bigwigs are saved use 'pwd'")
parser.add_argument("-m", "--metadata",
                    help="metadata tsv file to obtain: ID[0] and Name[2]; with not header")
parser.add_argument("-s", "--strand", default="Yes",
                    help="Yes if stranded rna-seq having + and - strand; [default= %(default)s]")
parser.add_argument("-u", "--unique", default="Yes",
                    help="Yes if are unique bigwig files; [default= %(default)s]")
parser.add_argument("-o", "--output",
                    default="output.generate.track.UCSC.txt",
                    help="output name; [default= %(default)s]")

args = parser.parse_args()


def obtain_path(input_path):
    """Obtain the absolute path."""
    path = input_path.split('/')[5:]
    insert_elements = ['public-docs.crg.es', 'rguigo', 'Data', 'ramador']
    path = insert_elements+path
    path = "/".join(path)
    return(path)


def manage_met(met_input):
    """Manage metadata."""
    final = []
    with open(met_input, 'r') as metadata:
        for i in metadata:
            i = i.strip().split('\t')
            result = [j.strip() for j in i]
            final.append(result)
    return(final)


def main(result_name, metadata, strand, unique, path):
    """Main function to generate the USCS tracks."""
    with open(result_name, 'w') as result:
        for i in metadata:
            if strand == "Yes" and unique == "Yes":
                strands = ["minus", "plus"]
                for count, j in enumerate(strands):
                    track_name = "track type=bigWig name=\"Unique_{0}-{1}\"".format(
                        j, i[1])
                    description = " description=\"{}\"".format(i[1])
                    bigwig_file = "bigDataUrl=https://{0}/{1}.Unique.{2}Raw.bw".format(
                        path, i[0], j)
                    ucsc_file = track_name+description+" "+bigwig_file
                    print("{0}: {1}".format(count+1, ucsc_file))
                    result.write("{0}\n".format(ucsc_file))
            elif strand == "Yes" and unique == "No":
                print("Need to add this part")
            elif strand == "No" and unique == "Yes":
                print("check GitHub")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        parser.print_help()
        sys.exit(1)
    path = obtain_path(input_path=args.path)
    meta_data = manage_met(met_input=args.metadata)
    main(result_name=args.output, metadata=meta_data, strand=args.strand,
         unique=args.unique, path=path)

## Obtain CRISPR spacers from MinCED
ls MAGs/*.fa | xargs -n1 basename > MAGs.list
for f in `cat MAGs.list` # list of symbiont MAGs
do
minced -spacers /gpfs/data/rbeinart/mhauer/phage_LauBasin/symbiont_MAGs/${f} output_${f}.txt output_${f}.gff
done

# Count # of spacers per MAG
python3 count_sequences_per_MAG.py

## put all spacer fa sequences from MinCED in one directory
mkdir spacers
cd spacers
ln -s ../*fa .

### concatenate all spacers files but add the file name to the headers in the process
## Create or overwrite the output file
output_file="concatenated.fa"

## Remove the output file if it exists to start fresh
if [ -f "$output_file" ]; then
    rm "$output_file"
fi

## Loop over each .fa file in the directory
for file in *.fa; do
   # # Use sed to modify the headers and append to the output file
    sed -e "s/^>/>$(basename "$file" .fa)_/" "$file" >> "$output_file"
done
cd ../

# use cd-hit to cluster CRISPR spacers 
cd-hit -i concatenated.fa -o cdhit_output.fasta -c 0.85 -s 1 -d 0

## taxonomically classify spacers
# make list file
ls *.fa > list.list
# remove .fa from filename
sed -i 's/.fa//g' list.list

for f in `cat list.list`
do
blastn -query ${f}.fa -db nt_viruses -perc_identity 100.0 -max_target_seqs 5 -word_size 20 -out virus_word20/${f}_blast.out -outfmt "6 std stitle"
done

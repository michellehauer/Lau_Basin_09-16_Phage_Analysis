# in a directory with all the spacers and the best genome representatives as given by dRep
python3 rename.py # adds file name to the headers
python3 clean_headers.py # cleans the headers
python3 check.py # checks if the cleaning was successful
python3 cat.py # concatenates all fasta files
makeblastdb -in clean/cat.fasta -dbtype nucl
blastn -query clean/cat.fasta -db clean/cat.fasta -word_size 20 -max_target_seqs 1 -out word20.tsv -outfmt '6 qseqid sseqid pident leng>
blastn -query clean/cat.fasta -db clean/cat.fasta -outfmt 5 -out clean/blastn2.xml


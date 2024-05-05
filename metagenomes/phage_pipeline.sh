## Use VIBRANT to obtain lytic and lysogenic phage content in metagenomes
source activate py39
for file in *.fasta # metagenome files
do
/gpfs/data/rbeinart/Software/VIBRANT/VIBRANT_run.py -i "$file"
done
source deactivate

## Softlink all of the lysogenic and lytic files to a directory, extract the contigs for downstream analyses
mkdir phage
ls *.fa | sed 's/\.fa$//' > phage/metagenomes.list # make list file of metagenomes
cd phage

for f in `cat metagenomes.list`
do
ln -s ../VIBRANT_${f}/VIBRANT_phages_${f}/${f}.phages_lysogenic.fna
done

for f in `cat metagenomes.list`
do
ln -s ../VIBRANT_${f}/VIBRANT_phages_${f}/${f}.phages_lytic.fna
done

# Extract contigs
ls *.fna > phage.list
mkdir contigs

for f in `cat phage.list`
do 
while read line
do if [[ ${line:0:1} == '>' ]]
then outfile=${f%.fna}_${line#>}.fna
echo $line > $outfile
else echo $line >> contigs/$outfile
fi
done < ${f}
done

# get phage contig lengths for all contigs, 2009-2022:
cd contigs
python3 get_sequence_lengths.py

# Obtain geNomad taxonomic classifications
source activate genomad
for f in *fna
do
genomad annotate ${f} genomad_output genomad_db
done
conda deactivate

cd ../../
mkdir drep
cd drep
## Run dRep to obtain species groups from phage in metagenomes
source activate drep
dRep dereplicate --S_algorithm ANImf --SkipMash -nc .5 -sa .95 -l 10000 -N50W 0 -sizeW 1 --ignoreGenomeQuality --clusterAlg single MAGs_drep_output -g {path_to_phage_contigs}/*fna
conda deactivate


### Run VIBRANT on 2022 MAGs to ID lysogenic and AMG content
mkdir VIBRANT
cd VIBRANT

source activate py39

for file in *.fa # for all symbiont MAG .fa files
do
/gpfs/data/rbeinart/Software/VIBRANT/VIBRANT_run.py -i "$file"
done

conda deactivate py39

### softlink all of the lysogenic files to a directory, extract the contigs for downstream analyses
mkdir lysogenic_phage
ls *.fa | sed 's/\.fa$//' > lysogenic_phage/MAG.list # make list file of MAGs
cd lysogenic_phage

for f in `cat MAG.list`
do
ln -s ../VIBRANT_${f}/VIBRANT_phages_${f}/${f}.phages_lysogenic.fna
done

# Extract contigs from VIBRANT lysogenic .fna files, adding file name to the headers for downstream clarity
ls *.fna > lysogens.list
mkdir contigs

for f in `cat lysogens.list`
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
for f in *fna
do
genomad annotate ${f} genomad_output genomad_db
done

cd ../../
mkdir drep
cd drep
## Run dRep to obtain species groups from phage in MAGs
source activate drep
# MAGs
dRep dereplicate --S_algorithm ANImf --SkipMash -nc .5 -sa .95 -l 10000 -N50W 0 -sizeW 1 --ignoreGenomeQuality --clusterAlg single MAGs_drep_output -g {path_to_phage_contigs}/*fna
conda deactivate


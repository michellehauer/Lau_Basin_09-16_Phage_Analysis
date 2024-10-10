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

# get phage contig lengths for all contigs:
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
dRep dereplicate --S_algorithm ANImf --SkipMash -nc .5 -sa .95 -l 10000 -N50W 0 -sizeW 1 --ignoreGenomeQuality --clusterAlg single metagenome_drep_output -g {path_to_phage_contigs}/*fna
conda deactivate

### Run iPhop to predict the phage hosts
conda activate iphop_env
mkdir iphop_db
cd iphop_db
#download the db
wget https://portal.nersc.gov/cfs/m342/iphop/db/iPHoP.latest_rw.tar.gz
tar -zxvf iPHoP.latest_rw.tar.gz
#check db integrity
iphop download --db_dir iphop_db/Aug_2023_pub_rw/ --full_verify
conda deactivate iphop_env

# prepare to add my symbiont MAGs to the db
conda activate /project/pi_rbeinart_uri_edu/michelle/conda/gtdb_2.1.1 
conda env config vars set GTDBTK_DATA_PATH="release214"
# add my symbiont mags (added 09-22 MAGs)
gtdbtk de_novo_wf --genome_dir /project/pi_rbeinart_uri_edu/michelle/iphop/symbiont_MAGs --bacteria --outgroup_taxon p__Patescibacteria --out_dir symbiont_MAGs_GTDB-tk_results2/ --cpus 32 --force --extension fasta
conda deactivate
## there is a bug in the version of iphop so i had to manually change the ar53 file  in iphop_db2/Aug_2023_pub_rw/db_infos/), cp gtdbtk.ar53.decorated.tree gtdbtk.ar122.decorated.tree”, https://bitbucket.org/srouxjgi/iphop/issues/98/filenotfounderror-errno-2-no-such-file-or is the iphop issue discussion
conda activate iphop_env
iphop add_to_db --fna_dir symbiont_MAGs/ --gtdb_dir symbiont_MAGs_GTDB-tk_results/ --out_dir April_2024_pub_rw_w_MAG_hosts --db_dir /project/pi_rbeinart_uri_edu/michelle/iphop/iphop_db2/Aug_2023_pub_rw
cd phage_contigs
python3 add_filenames_to_headers.py .
cat *fna > ../cat_phage.fasta
cd ../
# run iphop
iphop predict --fa_file cat_phage.fasta --db_dir April_2024_pub_rw_w_MAG_hosts/ --out_dir iphop_output/ -t 4

#PBS -q new
#PBS -l nodes=1:ppn=20
export PATH=/brain/shulab/.conda/envs/ldsc/bin:$PATH
export PYTHONPATH=/brain/shulab/.conda/envs/ldsc/lib/python2.7/site-packages/


file_path=/brain/shulab/dxy/tools/ldsc/sumstats_final/nodal/ne
files=""
for i in {1..246}
do
files=${files}","${file_path}${i}".sumstats.gz"
done
#echo ${files}


for attr in fluid
do
/brain/shulab/dxy/tools/ldsc/ldsc/ldsc.py --rg /brain/shulab/dxy/tools/ldsc/sumstats_final/${attr}.sumstats.gz${files} --ref-ld-chr /brain/shulab/dxy/tools/ldsc/ldsc/1000G_Phase3_baselineLD_v2.2_ldscores/baselineLD.@ --w-ld-chr /brain/shulab/dxy/tools/ldsc/ldsc/1000G_Phase3_weights_hm3_no_MHC/weights.hm3_noMHC.@ --out /brain/shulab/dxy/tools/ldsc/rg_final/rsid_correct/ne_rg_${attr}
done

#PBS -q new
#PBS -l nodes=1:ppn=15
export PATH=/brain/shulab/.conda/envs/ldsc/bin:$PATH
export PYTHONPATH=/brain/shulab/.conda/envs/ldsc/lib/python2.7/site-packages/

#for attr in fluid
#do
#/brain/shulab/dxy/tools/ldsc/ldsc/munge_sumstats.py --sumstats /brain/shulab/dxy/tools/plink/gwas_cog/result/rsid/gwas_result_set_${attr}_rsid.txt --snp rsID --N-col OBS_CT --a1 A1 --a2 REF --chunksize 500000 --out /brain/shulab/dxy/tools/ldsc/sumstats_final/${attr} --merge-alleles /brain/shulab/dxy/tools/ldsc/ldsc/w_hm3.snplist
#done

for region in {1..246}
do
/brain/shulab/dxy/tools/ldsc/ldsc/munge_sumstats.py --sumstats /brain/shulab/dxy/tools/plink/gwas_nodal/ne/gwas_result_set_ne_region${region}_rsid.txt --snp rsID --N-col OBS_CT --a1 A1 --a2 REF --chunksize 500000 --out /brain/shulab/dxy/tools/ldsc/sumstats_final/validation/ne${region} --merge-alleles /brain/shulab/dxy/tools/ldsc/ldsc/w_hm3.snplist
done

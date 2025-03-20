#PBS -q new
#PBS -l nodes=1:ppn=25
export LD_LIBRARY_PATH=/brain/shulab/software/glibc-2.14/lib

/brain/shulab/dxy/tools/plink/plink2 --bfile /brain/shulab/dxy/tools/plink/preprocess/gwas_clean_set --pheno /brain/shulab/dxy/tools/plink/data/pheno_global_rich.txt --glm omit-ref hide-covar cols=+a1freq --covar /brain/shulab/dxy/tools/plink/data/cov_letter.txt --variance-standardize --out /brain/shulab/dxy/tools/plink/gwas_univariate3/gwas_result_set


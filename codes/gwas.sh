#!/bin/bash
# ------------------------------------------------------------------------------
# GWAS Analysis Script using PLINK2
# Description: Performs univariate GWAS with variance standardization
# ------------------------------------------------------------------------------

# PBS 资源配置
#PBS -q new
#PBS -l nodes=1:ppn=25
#PBS -N gwas_analysis
#PBS -j oe

# ==========================================
# 1. 环境与路径配置
# ==========================================
export LD_LIBRARY_PATH=/path/to/your/glibc-2.14/lib:$LD_LIBRARY_PATH

# 软件路径
PLINK2="/path/to/bin/plink2"

# 数据目录
PROJECT_DIR="/home/user/project_gwas"
GENO_PREFIX="$PROJECT_DIR/data/genotypes/gwas_clean_set"
PHENO_FILE="$PROJECT_DIR/data/phenotype/pheno_global_rich.txt"
COVAR_FILE="$PROJECT_DIR/data/covariates/cov_letter.txt"

# 输出目录
OUT_DIR="$PROJECT_DIR/results/univariate"
mkdir -p $OUT_DIR

# ==========================================
# 2. 执行 PLINK2 GWAS 分析
# ==========================================
echo "Starting GWAS analysis at $(date)"

$PLINK2 \
    --bfile $GENO_PREFIX \
    --pheno $PHENO_FILE \
    --covar $COVAR_FILE \
    --glm omit-ref hide-covar cols=+a1freq \
    --variance-standardize \
    --out $OUT_DIR/gwas_result_set

echo "Analysis finished at $(date)"

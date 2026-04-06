#!/bin/bash
# ------------------------------------------------------------------------------
# LDSC Summary Statistics Munging Script
# Description: Formats GWAS summary stats for LD Score Regression (LDSC)
# ------------------------------------------------------------------------------

# PBS Configuration
#PBS -q new
#PBS -l nodes=1:ppn=15
#PBS -N ldsc_munging

# ==========================================
# 1. 环境配置
# ==========================================

CONDA_ENV_PATH="/path/to/your/conda/envs/ldsc"
export PATH=$CONDA_ENV_PATH/bin:$PATH
export PYTHONPATH=$CONDA_ENV_PATH/lib/python2.7/site-packages/

# 定义 LDSC 脚本路径
MUNGE_SCRIPT="/path/to/ldsc/munge_sumstats.py"
# 定义 HapMap3 参照文件路径
HM3_SNPLIST="/path/to/ldsc/w_hm3.snplist"

# ==========================================
# 2. 路径配置
# ==========================================
PROJECT_DIR="/home/user/project_gwas"
INPUT_DIR="$PROJECT_DIR/gwas_results/nodal_ne"
OUTPUT_DIR="$PROJECT_DIR/ldsc/formatted_sumstats"

mkdir -p $OUTPUT_DIR

# ==========================================
# 3. 批量处理 246 个脑区
# ==========================================
echo "Starting munging for 246 regions at $(date)"

for region in {1..246}
do
    echo "Processing Region ${region}..."
    
    python $MUNGE_SCRIPT \
        --sumstats $INPUT_DIR/gwas_result_set_ne_region${region}_rsid.txt \
        --snp rsID \
        --N-col OBS_CT \
        --a1 A1 \
        --a2 REF \
        --chunksize 500000 \
        --merge-alleles $HM3_SNPLIST \
        --out $OUTPUT_DIR/ne${region}
done

echo "Munging complete at $(date)"

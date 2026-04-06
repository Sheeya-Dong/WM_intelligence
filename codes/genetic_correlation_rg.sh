#!/bin/bash
# ------------------------------------------------------------------------------
# LDSC Genetic Correlation (rg) Analysis
# Description: Estimates genetic correlation between Fluid Intelligence and 
#              246 Nodal Efficiency (NE) brain regions.
# ------------------------------------------------------------------------------

# PBS Configuration
#PBS -q new
#PBS -l nodes=1:ppn=20
#PBS -N ldsc_rg

# ==========================================
# 1. 环境与路径配置
# ==========================================
# 软链接或通用路径映射
CONDA_ENV="/path/to/your/conda/envs/ldsc"
export PATH=$CONDA_ENV/bin:$PATH
export PYTHONPATH=$CONDA_ENV/lib/python2.7/site-packages/

# LDSC 软件与参照数据路径
LDSC_PY="/path/to/ldsc/ldsc.py"
REF_LD="/path/to/ldsc/reference/1000G_Phase3_baselineLD_v2.2_ldscores/baselineLD.@"
W_LD="/path/to/ldsc/reference/1000G_Phase3_weights_hm3_no_MHC/weights.hm3_noMHC.@"

# 数据目录
PROJECT_DIR="/home/user/project_gwas"
SUMSTATS_DIR="$PROJECT_DIR/ldsc/sumstats"
OUTPUT_DIR="$PROJECT_DIR/ldsc/rg_results"
mkdir -p $OUTPUT_DIR

# ==========================================
# 2. 构建批量文件列表 (246 个脑区)
# ==========================================
# 字符串拼接
brain_files=""
for i in {1..246}
do
    # 拼接并以逗号分隔，注意 LDSC 的 --rg 参数要求格式为 trait1.sumstats.gz,trait2.sumstats.gz,...
    if [ -z "$brain_files" ]; then
        brain_files="${SUMSTATS_DIR}/nodal/ne${i}.sumstats.gz"
    else
        brain_files="${brain_files},${SUMSTATS_DIR}/nodal/ne${i}.sumstats.gz"
    fi
done

# ==========================================
# 3. 执行 LDSC 遗传相关性分析
# ==========================================
echo "Starting rg analysis for fluid intelligence..."

for attr in fluid
do
    python $LDSC_PY \
        --rg "${SUMSTATS_DIR}/${attr}.sumstats.gz,${brain_files}" \
        --ref-ld-chr $REF_LD \
        --w-ld-chr $W_LD \
        --out ${OUTPUT_DIR}/ne_rg_${attr}
done

echo "Analysis complete at $(date)"

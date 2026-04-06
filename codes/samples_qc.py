import pandas as pd
import numpy as np
from pathlib import Path

# ==========================================
# 1. 路径配置
# ==========================================
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data" / "ukb"
RAW_DATA_PATH = Path("E:/sample_QC/ukb676304.csv")  # 外部超大原始数据路径

# 确保输出目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# 2. 核心功能函数
# ==========================================

def merge_imaging_genetics(imaging_id_file, genetic_id_file):
    """合并影像数据与基因数据共有的 Sample"""
    df_imaging = pd.read_csv(imaging_id_file, header=None, names=['eid'])
    
    # 读取基因 ID 文件
    df_genetic = pd.read_csv(genetic_id_file, sep=' ', header=None)
    df_genetic = df_genetic.iloc[:, :2]
    df_genetic.columns = ['eid', 'iid']
    
    # 取交集
    df_merged = pd.merge(df_imaging, df_genetic, on='eid')
    return df_merged

def run_sample_qc(input_df, raw_pheno_path):
    # 定义需要提取的 UKB Field ID
    target_fields = {
        'eid': 'eid',
        '22006-0.0': 'genetic_ethnic',
        '22020-0.0': 'used_in_pca',
        '31-0.0': 'self_reported_sex',
        '22001-0.0': 'genetic_sex',
        '22019-0.0': 'sex_aneuploidy',
        '22027-0.0': 'heterozygosity_outlier',
        '22021-0.0': 'genetic_kinship'
    }
    
    # 仅读取必要的列以节省内存
    df_raw = pd.read_csv(raw_pheno_path, usecols=list(target_fields.keys()))
    df_raw = df_raw.rename(columns=target_fields)
    
    # 与待处理 ID 合并
    df_qc = pd.merge(df_raw, input_df, on='eid')
    
    # 筛选条件:
    # 1. 自述性别与基因性别一致
    # 2. 排除性染色体非整倍体
    # 3. 排除杂合度或缺失率异常
    # 4. 遗传背景为 Unrelated White British
    # 5. 排除亲缘关系过近者 (Ten or more third-degree relatives)
    mask = (
        (df_qc['self_reported_sex'] == df_qc['genetic_sex']) &
        (df_qc['sex_aneuploidy'].isnull()) &
        (df_qc['heterozygosity_outlier'].isnull()) &
        (df_qc['genetic_ethnic'] == df_qc['used_in_pca']) &
        (df_qc['genetic_kinship'] != 10)
    )
    
    return df_qc[mask]

# ==========================================
# 3. 执行流程
# ==========================================

if __name__ == "__main__":
    # A. 合并初步 ID
    merged_ids = merge_imaging_genetics(
        imaging_id_file = DATA_DIR / "id_all.csv",
        genetic_id_file = DATA_DIR / "c1.txt"
    )
    
    # B. 执行 QC 筛选
    final_qc_df = run_sample_qc(merged_ids, RAW_DATA_PATH)
    
    # C. 保存结果
    output_path = DATA_DIR / "id_qc_final.csv"
    final_qc_df.to_csv(output_path, index=None)
    
    print(f"Done! Final sample size: {len(final_qc_df)}")
    print(f"Result saved to: {output_path}")

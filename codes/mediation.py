import pandas as pd
import numpy as np
from pathlib import Path
from pingouin import mediation_analysis

# ==========================================
# 1. 路径配置
# ==========================================
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "mediation" / "data" / "med_fluid_prs_26655.csv"
OUTPUT_DIR = PROJECT_ROOT / "mediation" / "results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 定义变量
X_VAR = 'prs'
Y_VAR = 'fluid'
COVARS = ['age', 'sex'] # 中心站列将动态添加
REGIONS = [f'ne{i}' for i in range(1, 247)]

# ==========================================
# 2. 数据加载与标准化
# ==========================================

def preprocess_data(path):
    df = pd.read_csv(path)
    
    # 动态获取 center 的 dummy 列
    center_cols = [c for c in df.columns if 'center_' in c]
    all_covars = COVARS + center_cols
    
    # 执行 Z-score 标准化
    # 排除不需要标准化的列 (eid, sex, centers)
    exclude_cols = ['eid', 'sex'] + center_cols
    target_cols = [c for c in df.columns if c not in exclude_cols]
    
    df[target_cols] = df[target_cols].apply(lambda x: (x - x.mean()) / x.std())
    
    return df, all_covars

# ==========================================
# 3. 中介分析
# ==========================================

def run_batch_mediation(df, regions, x, y, covars, n_boot=5000, seed=1):
    """
    对多个中介变量进行批处理分析
    """
    results = []
    
    for i, m in enumerate(regions):
        print(f"[{i+1}/{len(regions)}] Analyzing Mediator: {m}...")
        
        # 执行中介分析
        # Indirect effect (Path c') 通常位于 stats.loc[4]
        stats = mediation_analysis(
            data=df, x=x, m=m, y=y, 
            covar=covars, alpha=0.05, 
            seed=seed, n_boot=n_boot
        )
        
        # 提取关键路径系数
        # Path a (X -> M), Path b (M -> Y), Total (X -> Y), Indirect (Path c')
        res_dict = {
            'region': m,
            'a': stats.loc[0, 'coef'],
            'b': stats.loc[1, 'coef'],
            'total': stats.loc[2, 'coef'],
            'indirect': stats.loc[4, 'coef'],
            'indirect_se': stats.loc[4, 'se'],
            'indirect_p': stats.loc[4, 'pval'],
            'indirect_ci_lower': stats.loc[4, 'CI[2.5%]'],
            'indirect_ci_upper': stats.loc[4, 'CI[97.5%]'],
            'a_sig': stats.loc[0, 'sig'],
            'b_sig': stats.loc[1, 'sig'],
            'indirect_sig': stats.loc[4, 'sig']
        }
        results.append(res_dict)
        
    return pd.DataFrame(results).set_index('region')

# ==========================================
# 4. 执行流程
# ==========================================

if __name__ == "__main__":
    # A. 预处理
    data, final_covars = preprocess_data(DATA_PATH)
    
    # B. 运行分析
    final_results = run_batch_mediation(
        data, REGIONS, X_VAR, Y_VAR, final_covars, n_boot=5000, seed=1
    )
    
    # C. 计算中介比例 (Mediation Ratio)
    final_results['mediation_ratio'] = final_results['indirect'] / final_results['total']
    
    # D. 保存
    final_results.to_csv(OUTPUT_DIR / "mediation_results_summary.csv")
    print(f"Results saved to {OUTPUT_DIR}")

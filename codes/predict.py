import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import pearsonr
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import KFold, GridSearchCV

# ==========================================
# 1. 路径配置
# ==========================================
PROJECT_ROOT = Path(__file__).resolve().parents[1] # 假设脚本在 /scripts 文件夹
INPUT_DIR = PROJECT_ROOT / "predict" / "final"
OUTPUT_DIR = PROJECT_ROOT / "predict" / "final" / "kf3"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COGS = ['fluid']

# ==========================================
# 2. plsr交叉验证函数
# ==========================================

def run_plsr_prediction(X, y, n_splits=3, seeds=range(1, 101)):
    """
    执行带 GridSearch 的 PLSR 预测并计算平均相关系数
    """
    all_seeds_ave_corr = []
    
    for seed in seeds:
        # 使用随机种子进行样本置换以保证鲁棒性
        kf = KFold(n_splits=n_splits, shuffle=True, random_state=seed)
        fold_corrs = []
        
        for train_index, test_index in kf.split(X):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            
            # PLSR 回归与超参数搜索 (n_components)
            model = PLSRegression(scale=True)
            param_grid = {'n_components': range(2, 10)}
            gsearch = GridSearchCV(model, param_grid, cv=n_splits)
            gsearch.fit(X_train, y_train)
            
            # 预测与相关性评估
            y_pred = gsearch.predict(X_test).flatten()
            corr, _ = pearsonr(y_pred, y_test)
            fold_corrs.append(corr)
            
        all_seeds_ave_corr.append(np.mean(fold_corrs))
        
    return np.array(all_seeds_ave_corr)

# ==========================================
# 3. 主程序流程
# ==========================================

def main():
    summary_results = pd.DataFrame(
        index=COGS, 
        columns=['mean0', 'std0', 'mean1', 'std1', 'mean2', 'std2']
    )

    for cog in COGS:
        # A. 加载数据
        file_path = INPUT_DIR / f"{cog}_nodal_eff_prs_best.csv"
        df = pd.read_csv(file_path)
        
        # B. 数据预处理: Z-score 标准化 (排除非特征列)
        feature_cols = [col for col in df.columns if col not in ['eid', cog]]
        df[feature_cols] = df[feature_cols].apply(lambda x: (x - x.mean()) / x.std())
        
        # C. 定义特征子集
        # 请根据实际列名修改以下逻辑以增强鲁棒性
        subsets = [
            df.iloc[:, 2:248],    # Subset 0: e.g., Eff only
            df.iloc[:, 248:494],  # Subset 1: e.g., PRS only
            df.iloc[:, 2:494]     # Subset 2: e.g., Combined
        ]
        
        subset_names = ['eff', 'prs', 'eff_prs']
        ttest_results = pd.DataFrame(columns=subset_names)

        # D. 迭代不同特征集进行预测
        for i, X_subset in enumerate(subsets):
            print(f"Processing {cog} - Subset {subset_names[i]}...")
            
            y = df[cog].values
            X = X_subset.values
            
            # 核心计算
            ave_corrs = run_plsr_prediction(X, y)
            
            # 记录结果
            summary_results.loc[cog, f'mean{i}'] = np.mean(ave_corrs)
            summary_results.loc[cog, f'std{i}'] = np.std(ave_corrs)
            ttest_results[subset_names[i]] = ave_corrs

        # E. 保存中间结果 (T-test 列表)
        ttest_output = OUTPUT_DIR / f"plsr_predict_{cog}_ttest.csv"
        ttest_results.to_csv(ttest_output, index=False)

    # F. 保存汇总结果
    summary_output = OUTPUT_DIR / "plsr_summary_stats.csv"
    summary_results.to_csv(summary_output)
    print(f"\nAll tasks complete.\nSummary:\n{summary_results}")

if __name__ == "__main__":
    main()

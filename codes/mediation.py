import pandas as pd
import numpy as np
from pingouin import mediation_analysis
from statsmodels.stats.multitest import fdrcorrection

data = pd.read_csv("/Users/sheeya/Documents/project/gwas_wm/mediation/data/med_fluid_prs_26655.csv")
zs = lambda v: (v - v.mean(0)) / v.std(0)
for colname, column in data.items():
    if colname != "sex" and colname != "eid" and colname != "center_0" and colname != "center_1" and colname != "center_2" and colname != "center_3":
        data[colname] = zs(column)
print(data)

regions = [f'ne{i}' for i in range(1, 247)]
df_cols = ['a','b','total','c','ratio','c_se','c_p','c_ci1','c_ci2','a_sig','b_sig','c_sig'] + [f'c_sig_seed{i}' for i in range(2, 11)]
df_beta_p = pd.DataFrame(data=None, index=regions,columns= df_cols)
for i in range(1,11):
    for region in regions:
        stats = mediation_analysis(data=data, x='prs', m=region, y='fluid', covar=['age','sex','center_0','center_1','center_2','center_3'], alpha=0.05, seed=i, n_boot=5000)
        print(stats)
        if i == 1:
            df_beta_p.loc[region, 'a'] = stats.loc[0, 'coef']
            df_beta_p.loc[region, 'b'] = stats.loc[1, 'coef']
            df_beta_p.loc[region, 'total'] = stats.loc[2, 'coef']
            df_beta_p.loc[region, 'c'] = stats.loc[4, 'coef']
            df_beta_p.loc[region, 'c_se'] = stats.loc[4, 'se']
            df_beta_p.loc[region, 'c_p'] = stats.loc[4, 'pval']
            df_beta_p.loc[region, 'c_ci1'] = stats.loc[4, 'CI[2.5%]']
            df_beta_p.loc[region, 'c_ci2'] = stats.loc[4, 'CI[97.5%]']
            df_beta_p.loc[region, 'a_sig'] = stats.loc[0, 'sig']
            df_beta_p.loc[region, 'b_sig'] = stats.loc[1, 'sig']
            df_beta_p.loc[region, 'c_sig'] = stats.loc[4, 'sig']
        else:
            col = 'c_sig_seed'+str(i)
            df_beta_p.loc[region, col] = stats.loc[4, 'sig']
        print(df_beta_p)

df_beta_p['ratio'] = df_beta_p['c'] / df_beta_p['total']
print(df_beta_p)



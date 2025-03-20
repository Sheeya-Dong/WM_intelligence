import pandas as pd
import numpy as np
import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import ttest_1samp
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.multitest import fdrcorrection

#phenotypic correlation

ne = pd.read_csv("/Users/sheeya/Documents/project/gwas_wm/data/pheno/NE.csv")
new_columns = {f'region{i}': f'ne{i}' for i in range(1, 247)}
new_columns['eid'] = 'eid'
ne = ne.rename(columns=new_columns)

cog_cov = pd.read_csv("/Users/sheeya/Documents/project/gwas_wm/data/cognition/cog_prs_pheno_cov.txt",sep='\t')
cog_cov = cog_cov.drop(['FID'],axis=1)
cog_cov.rename(columns={'IID': 'eid'}, inplace=True)
cog_cov = cog_cov.loc[:,['eid','fluid','sex','age','center']]
# cog_cov = cog_cov.loc[:,['eid','fluid', 'edu_years', 'reaction', 'pairs', 'numeric_memory','trail1','trail2','digit','sex','age','center']]
cog_cov.replace('NA', np.nan, inplace=True)
cog_cov = cog_cov.dropna()
cog_cov["sex"].replace("female", 0, inplace=True)
cog_cov["sex"].replace("male", 1, inplace=True)
cog_cov["center"].replace("c0", 0, inplace=True)
cog_cov["center"].replace("c1", 1, inplace=True)
cog_cov["center"].replace("c2", 2, inplace=True)
cog_cov["center"].replace("c3", 3, inplace=True)
cog_cov_encoded = pd.get_dummies(cog_cov, columns=['center'], prefix='center')
# print(cog_cov_encoded)

matrix = pd.merge(ne,cog_cov_encoded)
wbu = pd.read_csv("/Users/sheeya/Documents/project/gwas_wm/data/id/id_final.csv")
matrix = pd.merge(matrix,wbu)
print(matrix)
matrix = matrix.iloc[:,1:]

#两两偏相关
ne = ne.iloc[:,1:]
wm = ne.columns.tolist()
cognitives = ['fluid']
# cognitives = ['fluid', 'edu_years', 'reaction', 'pairs', 'numeric_memory','trail1','trail2','digit']
df_corr = pd.DataFrame(data=None,columns=cognitives,index=wm) # Correlation matrix
df_p = pd.DataFrame(data=None,columns=cognitives,index=wm)  # Matrix of p-values
print(df_corr)
print(df_p)

for x in cognitives:
    for y in wm:
        # tmp = matrix.dropna(subset=[x,y])
        rp0 = pg.partial_corr(matrix, x=x, y=y, covar=['sex', 'age','center_0','center_1','center_2','center_3'])
        r_eg0, p_eg0 = rp0['r'], rp0['p-val']
        print(x+': r = %.2lf, p = %.3lf'%(r_eg0,p_eg0))
        df_corr.loc[y,x] = r_eg0.iloc[0]
        df_p.loc[y,x] = p_eg0.iloc[0]

df_corr = df_corr.astype('float')
df_p = df_p.astype('float')

corrected_df_p = df_p.apply(lambda col: fdrcorrection(col)[1])
mask = corrected_df_p>0.05
df_corr_sig = df_corr
df_corr_sig[mask] = 0


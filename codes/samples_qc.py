import pandas as pd
import numpy as np

#求dti和基因都有的sample
all = pd.read_csv(r"D:\project\gwas_wm\data\ukb\id_all.csv",header=None)
all.columns = ['eid']
print(all)
chr = pd.read_csv(r"D:\project\gwas_wm\data\ukb\c1.txt",sep=' ',header=None)
chr.columns = ['eid','iid','a','b']
print(chr)
result = pd.merge(all,chr)
print(result)
result.to_csv("D:/project/gwas_wm/data/ukb/dti_chr.csv",index=None)

#后续筛选需要的指标形成表
list = ['eid', '22006-0.0', '22020-0.0', '31-0.0', '22001-0.0','22019-0.0','22027-0.0','22021-0.0'] # Genetic ethnic grouping, Used in genetic principal components, self-reported sex, genetic sex, Sex chromosome aneuploidy, Outliers for heterozygosity or missing rate, Genetic kinship to other participants
print(list)

eid = pd.read_csv(r"D:\project\gwas_wm\data\ukb\dti_chr.csv")
print(eid)

file = r"E:\sample_QC\ukb676304.csv"
my_table = pd.read_csv(file, usecols=list)
result = pd.merge(my_table,eid)
print(result)
result.to_csv('D:/project/gwas_wm/data/ukb/table_dti_chr.csv', index=None)

# White British Unrelated(WBU)
ethnic = pd.read_csv("/Users/sheeya/Documents/project/gwas_wm/data/id/table_dti_chr.csv")
index = (ethnic['31-0.0'] == ethnic['22001-0.0']) & (ethnic['22019-0.0'].isnull()) & (ethnic['22027-0.0'].isnull()) & (ethnic['22006-0.0'] == ethnic['22020-0.0']) & (ethnic['22021-0.0'] != 10)
out = ethnic[index]
print(out)
out.to_csv('/Users/sheeya/Documents/project/gwas_wm/data/id/id_qc.csv', index=None)  # After sample_qc：26655 people

# # 其他种族Unrelated(validation)
# ethnic = pd.read_csv("/Users/sheeya/Documents/project/gwas_wm/data/id/table_dti_chr.csv")
# index = (ethnic['31-0.0'] == ethnic['22001-0.0']) & (ethnic['22019-0.0'].isnull()) & (ethnic['22027-0.0'].isnull()) & (ethnic['22006-0.0'].isnull()) & (ethnic['22020-0.0'] == 1) & (ethnic['22021-0.0'] != 10)
# out = ethnic[index]
# out.insert(1, 'iid', out['eid'])
# out.rename(columns={'eid':'fid'},inplace=True)
# out = out.loc[:,['fid','iid']]
# print(out)
# out.to_csv('/Users/sheeya/Documents/project/gwas_wm/data/id/id_validation.txt', index=None, sep='\t')  # After sample_qc：4249 people


# 提取智力gwas的pheno和cov
# 有基因数据的sample
# chr = pd.read_csv("/Users/sheeya/Documents/project/gwas_wm/data/id/c1.txt", sep=' ', header=None)
# chr.columns = ['eid', 'iid', 'a', 'b']
# chr = chr.loc[:, ['eid']]
# print(chr)
# # 排除有dti影像的sample
# id_final = pd.read_csv("/Users/sheeya/Documents/project/gwas_wm/data/id/id_final.csv")
# obj = chr.append(id_final)
# bu = obj.drop_duplicates(keep=False)
# print(bu)
#
# my_table = pd.read_csv("/Users/sheeya/Documents/project/gwas_wm/data/pheno/ukb676304_usecols.csv")
# ethnic = pd.merge(bu, my_table)
# print(ethnic)
#
# index = (ethnic['31-0.0'] == ethnic['22001-0.0']) & (ethnic['22019-0.0'].isnull()) & (ethnic['22027-0.0'].isnull()) & (ethnic['22006-0.0'] == ethnic['22020-0.0']) & (ethnic['22021-0.0'] != 10)
# res = ethnic[index]
# res.insert(1, 'IID', res['eid'])
# print(res)


import math
import joblib
import pandas as pd
import numpy as np
from scipy.stats import spearmanr,pearsonr
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, GridSearchCV
from skimage.metrics import mean_squared_error
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import mean_absolute_error
from matplotlib import pyplot as plt
from scipy import stats
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import make_scorer



cogs = ['fluid']
mean_std = pd.DataFrame(index=cogs,columns=['mean0', 'std0', 'mean1','std1', 'mean2', 'std2'])
for cog in cogs:
    data = pd.read_csv("/Users/sheeya/Documents/project/gwas_wm/predict/final/"+cog+"_nodal_eff_prs_best.csv")
    # # ne列
    data = data.iloc[:,list(range(0, 248)) + list(range(494, 740))]
    # # nle列
    # data = data.iloc[:, list(range(0, 2)) + list(range(248, 494))+ list(range(740, 986))]
    zs = lambda v: (v-v.mean(0))/v.std(0)
    for colname,column in data.items():

        if colname != "eid":
            data[colname] = zs(column)

    # index = [[2, 494], [494, 986], [2, 986]]
    index = [[2, 248], [248, 494], [2, 494]]
    ttest_list = pd.DataFrame(data=None,columns=['eff', 'prs', 'eff_prs'])
    for i in range(3):
        ave_list = []
        for seed in range(1,101):
            corr_list = []
            X = data.iloc[:, index[i][0]:index[i][1]]
            y = data.loc[:, cog]
            print(X)
            X = np.array(X)
            y = np.array(y)
            np.random.seed(seed)
            np.random.shuffle(X)
            print(seed)
            print(X)
            np.random.seed(seed)
            np.random.shuffle(y)
            print(y)
            kf = KFold(n_splits=3,shuffle=False)
            for train_index, test_index in kf.split(X):
                # print("TRAIN:", len(train_index), "TEST:", len(test_index))
                X_train, X_test = X[train_index], X[test_index]
                y_train, y_test = y[train_index], y[test_index]
                #plsr
                model = PLSRegression(scale=True)
                param_grid = {'n_components': range(2,10)}
                gsearch = GridSearchCV(model, param_grid, cv = kf)
                gsearch.fit(X_train, y_train)
                y_pred = gsearch.predict(X_test)
                y_pred = y_pred.flatten()
                y_pred = np.array(y_pred)
                y_test = np.array(y_test)
                corr = pearsonr(y_pred,y_test).statistic
                print(corr)
                corr_list.append(corr)
            corr_list = np.array(corr_list)
            ave = corr_list.mean()
            ave_list.append(ave)
        ave_list = np.array(ave_list)
        mean = ave_list.mean()
        std = ave_list.std()
        mean_col_name = 'mean' + str(i)
        std_col_name = 'std' + str(i)
        mean_std.loc[cog,mean_col_name] = mean
        mean_std.loc[cog, std_col_name] = std
        ave_list = pd.DataFrame(ave_list)
        ttest_list[ttest_list.columns[i]] = ave_list
    print(ttest_list)
    ttest_list.to_csv("/Users/sheeya/Documents/project/gwas_wm/predict/final/kf3/plsr_predict_"+cog+"_with_ne_ttest.csv",index=None)
print(mean_std)
mean_std.to_csv("/Users/sheeya/Documents/project/gwas_wm/predict/final/kf3/plsr_mean_std_with_ne.csv")
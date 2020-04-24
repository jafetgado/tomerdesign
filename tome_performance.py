"""
Evaluate TOME performance with Monte Carlo cross validation (MCCV)
"""






# Imports
#============#

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

import resreg

import warnings
warnings.filterwarnings("ignore")





# Get data and features
#==============================#

aalist = list('ACDEFGHIKLMNPQRSTVWY')
def getAAC(seq):
    aac = np.array([seq.count(x) for x in aalist])/len(seq)
    return aac

data = pd.read_excel('data/sequence_ogt_topt.xlsx', index_col=0)
aac = np.array([getAAC(seq) for seq in data['sequence']])
ogt = data['ogt'].values.reshape((data.shape[0],1))
X = np.append(aac, ogt, axis=1)
sc = StandardScaler()
X = sc.fit_transform(X)
y = data['topt'].values







# Evaluate TOMER performance (i.e. without resampling)
#========================================================#
bins = [30, 50, 65, 85]  # For splitting target values into bins
m = 100    # Number of regressors in REBAGG ensemble

r2_store, mse_store, mcc_store, f1_store = [], [], [], [] # Empty lists for storing results
mse_bins_store  = []
    
# Monte Carlo cross validation (MCCV) 
for rrr in range(50):
    #print(f'{rrr+1} of 50')
    # Resample test set (uniform distribution)
    train_indices, test_indices = resreg.uniform_test_split(X, y, bins=bins, 
                                            bin_test_size=70, verbose=False, 
                                            random_state=rrr*11)
    X_train, y_train = X[train_indices,:], y[train_indices]
    X_test, y_test = X[test_indices,:], y[test_indices]
    
    
    # Fit regressor and apply to uniform test set
    reg = RandomForestRegressor(n_estimators=10, n_jobs=-1, random_state=rrr*11)
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)

    
    # Evaluate regressor performance on test set
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    mcc = resreg.matthews_corrcoef(y_test, y_pred, bins)
    relevance_true = resreg.sigmoid_relevance(y_test, cl=None, ch=65)
    relevance_pred = resreg.sigmoid_relevance(y_pred, cl=None, ch=65)
    f1 = resreg.f1_score(y_test, y_pred, error_threshold=5, 
                     relevance_true=relevance_true, relevance_pred=relevance_pred,
                     relevance_threshold=0.5, k=1e4)
    mse_bins = resreg.bin_performance(y_test, y_pred, bins, metric='MSE')
    
    
    # Store performance results
    r2_store.append(r2)
    mse_store.append(mse)
    mcc_store.append(mcc)
    f1_store.append(f1)
    mse_bins_store.append(mse_bins)
    
    
# Performance statistics
r2_mean, r2_std = np.mean(r2_store), np.std(r2_store)
mse_mean, mse_std = np.mean(mse_store), np.std(mse_store)
f1_mean, f1_std = np.mean(f1_store), np.std(f1_store)
mcc_mean, mcc_std = np.mean(mcc_store), np.std(mcc_store)
mse_bins_store = pd.DataFrame(mse_bins_store)
mse_bins_mean = np.mean(mse_bins_store, axis=0)
mse_bins_std = np.std(mse_bins_store, axis=0)

# Combine all performance data and write to excel spreadsheet
means = [r2_mean, mse_mean, f1_mean, mcc_mean] + list(mse_bins_mean)
stds = [r2_std, mse_std, f1_std, mcc_std] + list(mse_bins_std)
store = [means, stds]
final_store = pd.DataFrame(store).transpose()
final_store.index = ['r2', 'mse', 'f1', 'mcc'] + \
                      ['mse_bin{0}'.format(x) for x in range(1,6)]
final_store.columns = ['means', 'stds']
final_store.to_excel('results/TOME.xlsx')

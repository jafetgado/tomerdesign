"""
Template script for hyperparameter tuning with HPC

Evaluates the performance of a strategy for a single 
set of hyperparameter combinations)
"""




# Imports
#============#

import numpy as np
import pandas as pd
import joblib
import itertools

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

import resreg

import warnings
warnings.filterwarnings("ignore")




# Get dataset and features
#==============================#

aalist = list('ACDEFGHIKLMNPQRSTVWY')
def getAAC(seq):
    aac = np.array([seq.count(x) for x in aalist])/len(seq)
    return aac

data = pd.read_excel('sequence_ogt_topt.xlsx', index_col=0)
aac = np.array([getAAC(seq) for seq in data['sequence']])
ogt = data['ogt'].values.reshape((data.shape[0],1))
X = np.append(aac, ogt, axis=1)
sc = StandardScaler()
X = sc.fit_transform(X)
y = data['topt'].values



# Strategies and hyperparameters
#======================================#

# Hyperparameter range
cl_vals = [25.0, 30.0, None]
ch_vals = [72.2, 60.0]
ks = [5, 10, 15]
deltas = [0.1, 0.5, 1.0]
overs = [0.5, 0.75]
unders = [0.5, 0.75]
sizes = [300, 600]
sample_methods = ['balance', 'extreme', 'average']
size_methods = ['balance', 'variation']
all_params = {}


# Hyperparameter combinations (grid search)
all_params['RO'] = list(itertools.product(cl_vals, ch_vals, sample_methods))
all_params['SMOTER'] = list(itertools.product(cl_vals, ch_vals, sample_methods, ks))
all_params['GN'] = list(itertools.product(cl_vals, ch_vals, sample_methods, deltas))
all_params['WERCS'] = list(itertools.product(cl_vals, ch_vals, overs, unders))
all_params['WERCS-GN'] = list(itertools.product(cl_vals, ch_vals, overs, unders, deltas))
all_params['REBAGG-RO'] = list(itertools.product(cl_vals, ch_vals, size_methods, 
                              sizes))
all_params['REBAGG-SMOTER'] = list(itertools.product(cl_vals, ch_vals, size_methods, 
                                   sizes, ks))
all_params['REBAGG-GN'] = list(itertools.product(cl_vals, ch_vals, size_methods, 
                               sizes, deltas))
all_params['REBAGG-WERCS'] = list(itertools.product(cl_vals, ch_vals, sizes, overs, 
                                  unders))
all_params['REBAGG-WERCS-GN'] = list(itertools.product(cl_vals, ch_vals, sizes, overs, 
                                     unders, deltas))
strategies = list(all_params.keys())




# Evaluate performance for a single strategy and hyperparameter combination
#===========================================================================#

bins = [30, 50, 65, 85]  # For splitting target values into bins
m = 100    # Number of regressors in REBAGG ensemble

# Specify strategy and param (instead of a lengthy for loop of combinations)
strategy = 'RO'   # Replace RO for this calculation
params = all_params[strategy]  
param = params[8]   # Replace 8 for this calculation


# Implement calculation for only specified strategy and param
r2_store, mse_store, mcc_store, f1_store = [], [], [], [] # Empty lists for storing results
mse_bins_store  = []

# Monte Carlo cross validation (MCCV) loop
for rrr in range(50):
    # Resample validation set (uniform distribution)
    train_indices, test_indices = resreg.uniform_test_split(X, y, bins=bins, 
                                            bin_test_size=70, verbose=False, 
                                            random_state=rrr)
    X_train, y_train = X[train_indices,:], y[train_indices]
    X_test, y_test = X[test_indices,:], y[test_indices]
    
    
    # Unpack hyperparameters, resample training data, and fit regressors
    reg = DecisionTreeRegressor(random_state=rrr) if 'REBAGG' in strategy else \
              RandomForestRegressor(n_estimators=10, n_jobs=-1, random_state=rrr)
              
    if strategy=='RO':
        cl, ch, sample_method = param
        relevance = resreg.sigmoid_relevance(y_train, cl=cl, ch=ch)
        X_train, y_train = resreg.random_oversample(X_train, y_train, relevance,
                                    relevance_threshold=0.5, over=sample_method,
                                    random_state=rrr)
        reg.fit(X_train, y_train)
    
    elif strategy=='SMOTER':
        cl, ch, sample_method, k = param
        relevance = resreg.sigmoid_relevance(y_train, cl=cl, ch=ch)
        X_train, y_train = resreg.smoter(X_train, y_train, relevance, 
                                 relevance_threshold=0.5, k=k, over=sample_method,
                                 random_state=rrr)
        reg.fit(X_train, y_train)
    
    elif strategy=='GN':
        cl, ch, sample_method, delta = param
        relevance = resreg.sigmoid_relevance(y_train, cl=cl, ch=ch)
        X_train, y_train = resreg.gaussian_noise(X_train, y_train, relevance, 
                          relevance_threshold=0.5, delta=delta, over=sample_method,
                          random_state=rrr)
        reg.fit(X_train, y_train)
    
    elif strategy=='WERCS':
        cl, ch, over, under = param
        relevance = resreg.sigmoid_relevance(y_train, cl=cl, ch=ch)
        X_train, y_train = resreg.wercs(X_train, y_train, relevance, over=over, 
                                        under=under, noise=False, random_state=rrr)
        reg.fit(X_train, y_train)
    
    elif strategy=='WERCS-GN':
        cl, ch, over, under, delta = param
        relevance = resreg.sigmoid_relevance(y_train, cl=cl, ch=ch)
        X_train, y_train = resreg.wercs(X_train, y_train, relevance, over=over, 
                                 under=under, noise=True, delta=delta, random_state=rrr)
        reg.fit(X_train, y_train)
   
    elif strategy=='REBAGG-RO':
        cl, ch, size_method, s = param
        relevance = resreg.sigmoid_relevance(y_train, cl=cl, ch=ch)
        rebagg = resreg.Rebagg(m=m, s=s, base_reg=reg)
        rebagg.fit(X_train, y_train, relevance, relevance_threshold=0.5, 
                   sample_method='random_oversample', size_method=size_method, 
                   random_state=rrr)
    
    elif strategy=='REBAGG-SMOTER':
        cl, ch, size_method, s, k = param
        relevance = resreg.sigmoid_relevance(y_train, cl=cl, ch=ch)
        rebagg = resreg.Rebagg(m=m, s=s, base_reg=reg)
        rebagg.fit(X_train, y_train, relevance, relevance_threshold=0.5, 
                   sample_method='smoter', size_method=size_method, k=k,
                   random_state=rrr)
        
    elif strategy=='REBAGG-GN':
        cl, ch, size_method, s, delta = param
        relevance = resreg.sigmoid_relevance(y_train, cl=cl, ch=ch)
        rebagg = resreg.Rebagg(m=m, s=s, base_reg=reg)
        rebagg.fit(X_train, y_train, relevance, relevance_threshold=0.5, 
                   sample_method='gaussian', size_method=size_method, delta=delta, 
                   random_state=rrr)

    elif strategy=='REBAGG-WERCS':
        cl, ch, s, over, under = param
        relevance = resreg.sigmoid_relevance(y_train, cl=cl, ch=ch)
        rebagg = resreg.Rebagg(m=m, s=s, base_reg=reg)
        rebagg.fit(X_train, y_train, relevance=relevance, sample_method='wercs', 
                    over=over, under=under, random_state=rrr)
   
    elif strategy=='REBAGG-WERCS-GN':
        cl, ch, s, over, under, delta = param
        relevance = resreg.sigmoid_relevance(y_train, cl=cl, ch=ch)
        rebagg = resreg.Rebagg(m=m, s=s, base_reg=reg)
        rebagg.fit(X_train, y_train, relevance=relevance, sample_method='wercs-gn', 
                    over=over, under=under, delta=delta, random_state=rrr)
        
    
    # Validate fitted regressors on uniform validation set
    if 'REBAGG' in strategy:
        y_pred = rebagg.predict(X_test)
    else:
        y_pred = reg.predict(X_test)
    
    
    # Evaluate regressor performance on validation set
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
mse_bins_mean, mse_bins_std = np.mean(mse_bins_store, axis=0), np.std(mse_bins_store, axis=0)

# Combine all performance data and write to excel spreadsheet
means = [r2_mean, mse_mean, f1_mean, mcc_mean] + list(mse_bins_mean)
stds = [r2_std, mse_std, f1_std, mcc_std] + list(mse_bins_std)
store = [param] + means + stds


# Save performance results as a binary file (to be read and analyzed later)
joblib.dump(store, f'hpc/joblib_files/{strategy}_{8}.pkl')


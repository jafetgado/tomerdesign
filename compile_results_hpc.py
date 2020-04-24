"""
Compile result of performance evaluation with HPC
(Retrieve stored result from joblib files and write to spreadsheet)
"""




# Imports
#============#

import numpy as np
import pandas as pd
import itertools
import joblib
import subprocess

from sklearn.preprocessing import StandardScaler

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





# Retreive result for each strategy and write to spreadsheet
#=============================================================#    
for strategy in strategies:
    final_store = []  # For storing results
    params = all_params[strategy]
    
    for i_param in range(len(params)):
        param = params[i_param]
        result = joblib.load(f'hpc/joblib_files/{strategy}_{i_param}.pkl')
        final_store.append(result)
    
    final_store = pd.DataFrame(final_store)
    final_store.columns = ['params', 'r2', 'mse', 'f1', 'mcc',
                           'mse_bin1', 'mse_bin2', 'mse_bin3', 'mse_bin4', 'mse_bin5', 
                           'r2_std', 'mse_std', 'f1_std', 'mcc_std', 
                           'mse_bin1_std', 'mse_bin2_std','mse_bin3_std', 'mse_bin4_std', 
                           'mse_bin5_std']
    final_store.to_excel('results/{0}.xlsx'.format(strategy))



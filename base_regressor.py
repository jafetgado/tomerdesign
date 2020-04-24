"""
Investigate the effect of different base regressors
"""



# Imports
#============#

import numpy as np
import pandas as pd
import itertools

from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

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






# Functions for implementing MCCV
#=================================================#

bins = [30, 50, 65, 85]

def implementMCCV(reg):
    '''Test the performance of a base regressor (reg) with REBAGG-RO resampling 
    (m=100, s=600, cl=None, ch=72.2).'''
    
    r2_store, mcc_store, f1_store = [], [], []
    for rrr in range(50):
        if rrr%10 == 0:
            print(rrr)
        # Resample validation set (uniform distribution)
        train_indices, test_indices = resreg.uniform_test_split(X, y, bins=bins, 
                                                    bin_test_size=70, verbose=False, 
                                                    random_state=rrr)
        X_train, y_train = X[train_indices,:], y[train_indices]
        X_test, y_test = X[test_indices,:], y[test_indices]
        
        
        # Fit rebagg to training data   
        relevance = resreg.sigmoid_relevance(y_train, cl=None, ch=72.2)
        rebagg = resreg.Rebagg(m=100, s=600, base_reg=reg)
        rebagg.fit(X_train, y_train, relevance, relevance_threshold=0.5, 
                   sample_method='random_oversample', size_method='variation',
                   random_state=rrr)
        y_pred = rebagg.predict(X_test)
    
    
        # Evaluate regressor performance on test set
        r2 = r2_score(y_test, y_pred)
        mcc = resreg.matthews_corrcoef(y_test, y_pred, bins)
        relevance_true = resreg.sigmoid_relevance(y_test, cl=None, ch=65)
        relevance_pred = resreg.sigmoid_relevance(y_pred, cl=None, ch=65)
        f1 = resreg.f1_score(y_test, y_pred, error_threshold=5, 
                         relevance_true=relevance_true, relevance_pred=relevance_pred,
                         relevance_threshold=0.5, k=1e4)
        
        # Store performance results
        r2_store.append(r2)
        mcc_store.append(mcc)
        f1_store.append(f1)
    
    # Performance statistics
    r2_mean, r2_std = np.mean(r2_store), np.std(r2_store)
    f1_mean, f1_std = np.mean(f1_store), np.std(f1_store)
    mcc_mean, mcc_std = np.mean(mcc_store), np.std(mcc_store)
    
    # Combine all performance data and write to excel spreadsheet
    store = [r2_mean, f1_mean, mcc_mean, r2_std, f1_std, mcc_std]
    
    # Return result
    return store






# Base regressors and hyperparameter range
#=================================================#
regressors = ['SVR', 'KNR', 'ENET', 'BAYR', 'MLPR']
ks = [3, 5, 7, 10, 15, 20, 30]
cs_svr = 10.0 ** np.arange(-1,3)
gamma_svr = 10.0 ** np.arange(-3,1)
alphas = 10.0 ** np.arange(-3,3)
alpha_mlpr = 10.0 ** np.arange(-5,1)






# Optimize hyperparameters for each regressor type
#======================================================#
for regressor in regressors:
    print(regressor)
    if regressor == 'SVR':
        params = list(itertools.product(cs_svr, gamma_svr))
        store_svr = []
        for param in params:
            print(param)
            C, gamma = param
            reg = SVR(kernel='rbf', C=C, gamma=gamma)
            performance = implementMCCV(reg)
            store_svr.append(performance)
        
    elif regressor == 'KNR':
        store_knr = []
        for k in ks:
            print(k)
            reg = KNeighborsRegressor(n_neighbors=k)
            performance = implementMCCV(reg)
            store_knr.append(performance)
    
    elif regressor == 'ENET':
        store_enet = []
        for alpha in alphas:
            print(alpha)
            reg = ElasticNet(alpha=alpha)
            performance = implementMCCV(reg)
            store_enet.append(performance)
    
    elif regressor == 'BAYR':
        reg = BayesianRidge()
        performance = implementMCCV(reg)
        store_bayr = [performance]

            
    
        
        


# Save results
#====================#           
store_all = [store_svr, store_knr, store_enet, store_bayr]
params_all = [itertools.product(cs_svr, gamma_svr),
              [3, 5, 7, 10, 15, 20, 30],
              10.0 ** np.arange(-3,3),
              ['Default']]
              

for store, params, regressor in zip(store_all, params_all, regressors):
    df = pd.DataFrame(store)
    df.columns =  ['r2', 'f1', 'mcc', 'r2_std', 'f1_std', 'mcc_std']
    df.index = params                  
    df.to_excel(f'results/base_regressors/{regressor}.xlsx')
        


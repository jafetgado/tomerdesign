"""
Prepare final improved model (TOMER)
""" 






# Imports
#============#

import numpy as np
import pandas as pd
import joblib

from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler
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




# Fit TOMER with Rebagg ensemble to all 2,917 sequences
#========================================================#
base_reg = DecisionTreeRegressor(random_state=0)
rebagg = resreg.Rebagg(m=100, s=600, base_reg=base_reg)
relevance = resreg.sigmoid_relevance(y, cl=None, ch=72.2)
rebagg.fit(X, y, relevance=relevance, relevance_threshold=0.5, 
           sample_method='random_oversample', size_method='variation', random_state=0)



# Save final model
#========================#
joblib.dump(rebagg, 'results/final_model/tomer_rebagg.pkl')
joblib.dump(sc, 'results/final_model/standard_scaler.pkl')
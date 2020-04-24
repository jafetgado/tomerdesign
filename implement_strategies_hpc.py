"""
Apply resampling strategies to improve Topt prediction
(Use HPC to parallelize and speed up computation)
"""




# Imports
#============#

import numpy as np
import pandas as pd
import itertools
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





# Apply each strategy and evaluate performance
#==============================================#
with open('template.py', 'r') as temp:
    py_template = temp.read()
subprocess.call('cp resreg.py hpc/', shell=True)

    
for strategy in strategies:
    params = all_params[strategy]
    
    for i_param in range(len(params)):
        param = params[i_param]
        
        # Write python script to evaluate performance
        with open(f'hpc/{strategy}_{i_param}.py', 'w') as pytemp:
            edited = py_template.replace('STRATEGY', strategy)
            edited = edited.replace('I_PARAM', str(i_param))
            pytemp.write(edited)
        
        # Write bash script to submit python job to HPC scheduler (PBS)
        with open(f'hpc/{strategy}_{i_param}.sh', 'w') as bash:
            bash.write(f'''#!/bin/bash
#PBS -N {strategy}_{i_param}
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/{strategy}_{i_param}.out
#PBS -e hpc/{strategy}_{i_param}.err

cd /home/japheth/tomer_design_hpc

python hpc/{strategy}_{i_param}.py''')
            
        # Submit python job to HPC scheduler (PBS)
        subprocess.call(f'qsub hpc/{strategy}_{i_param}.sh',
                        shell=True)






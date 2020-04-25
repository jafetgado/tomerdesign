**TOMER Design**
========================================

Investigating the effects of resampling strategies on the performance of enzyme optimum temperature prediction, and development of an improved machine-learning method (TOMER).

Results and findings are published in:

Gado, J.E., Beckham, G.T., and Payne, C.M (2020). Improving enzyme optimum temperature prediction with resampling strategies and ensemble learning.


Python scripts
----------------
* ``tome_performance.py``: evaluate predictive performance without resampling dataset (TOME).
* ``implement_strategies.py``: implement resampling strategies and evaluate performance (slow, using a single processor).
* ``template.py``: template script for evaluating performance with each hyperparameter combination of the resampling strategies with HPC.
* ``implement_strategies_hpc.py``: submit Python scripts (hpc/\*.py) for all strategies in the format of *template.py* as batch jobs (hpc/\*.sh) to a PBS scheduler. Results are saved as pickle files (hpc/joblib_files/\*.pkl). Standard output and error are written to hpc/\*.out and hpc/\*.err.
* ``compile_results_hpc.py`` combine results of batch jobs (saved as pickle files) and write them to a single spreadsheet (results/\*.xlsx).
* ``base_regressor.py``: evaluate the effect of different base learners on the performance of the Rebagg ensemble. Results are saved in results/base_regressor/\*.xlsx.
* ``plots.py``: plot results
* ``tomer_final_model.py``: prepare improved model with entire dataset (2,917 proteins).


Prerequisites
---------------

(version used in this work)

1. Python (3.6.6)
2. Numpy (1.14.2)
3. Pandas (0.24.1)
4. Scikit-learn (0.21.2)
5. Joblib (0.13.2)
6. Resreg

"""
Plot results of TOMER study
"""




# Imports
#============#

import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde

import matplotlib.pyplot as plt
from matplotlib import ticker
import seaborn as sns

import resreg

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

import warnings
warnings.filterwarnings("ignore")






# Get data and features
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






# Figure 1A: Distribution of test set (random vs uniform)
#============================================================#
fnt='Arial'
ticks_font = {'fontname':fnt, 'size':'16'}
legend_font = {'family':fnt, 'size':'16'}
label_font = {'family':fnt, 'size':'18'}
plt.rcParams['figure.figsize'] = [6,3.818]
params = {'mathtext.default': 'regular' }        
plt.rcParams.update(params)
plt.rc('font', size=14)


bins = [30, 50, 65, 85]
for rrr in range(50):
    # Uniform distribution
    train_indices, test_indices = resreg.uniform_test_split(X, y, bins=bins, 
                                                bin_test_size=70, verbose=False, 
                                                random_state=rrr*5)
    y_test_uniform = y[test_indices]    
        
    # Normal distribution
    np.random.seed(seed=rrr*5)
    test_indices = np.random.choice(range(len(y)), 350, replace=False)
    y_test_normal = y[test_indices]
    
    # Plot distribution
    sns.kdeplot(y_test_normal, color='darkblue', linestyle='-', linewidth=0.5, bw=7)
    sns.kdeplot(y_test_uniform, color='darkred', linestyle='-', linewidth=0.5, bw=7)

plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0), useMathText=True)
plt.axhline(y=1.0, color='darkblue', linestyle='-', label='normal')  # Just for legend
plt.axhline(y=1.0, color='darkred', linestyle='-', label='uniform')
plt.legend(frameon=False, prop=legend_font)
plt.xlim((0,120))
plt.ylim((0, 0.030))
plt.xticks(**ticks_font)
plt.yticks(**ticks_font)
plt.xlabel(u'T$_{opt} $ (\N{DEGREE SIGN}C)', **label_font)
plt.ylabel('Density', labelpad=10, **label_font)
plt.tight_layout()
plt.savefig('plots/fig1a_uniform_test_dist.pdf')
plt.show()
plt.close()






# Figure 1B and 1C: Relevance function
#=====================================#
fnt='Arial'
ticks_font = {'fontname':fnt, 'size':'16'}
legend_font = {'family':fnt, 'size':'14'}
label_font = {'family':fnt, 'size':'18'}
title_font = {'family':fnt, 'size':'18'}
plt.rcParams['figure.figsize'] = [6,3.5]
params = {'mathtext.default': 'regular' }        
plt.rcParams.update(params)
plt.rc('font', size=12)

formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((0,0))

# One-sided
yrange = np.arange(0, 120.1, step=0.5)
cl1, ch1 = None, np.percentile(y, 90)
rel = resreg.sigmoid_relevance(yrange, cl1, ch1)

ax = plt.subplot()
ax.plot(yrange, rel, label='Relevance', color='crimson', linewidth=2)
#ax.axhline(0.5, linestyle='--', color='grey')
ax.hlines(0.5, xmin=0, xmax=120, linestyle='--', color='grey')
ax.vlines(72.2, ymin=0, ymax=0.5, linestyle='--', color='grey')
ax.text(x=5, y=0.53, s=u't$_{R}$=0.5', fontdict=legend_font)

kde = gaussian_kde(y, bw_method=0.4)
dens = kde.evaluate(yrange)
ax2 = ax.twinx()
ax2.plot(yrange, np.ones(len(yrange))*99, color='crimson', label='Relevance')  # Just for legend
ax2.plot(yrange, dens, color='black', label='Density')

higher_shade = np.arange(72, 120.1, step=1)
ax2.fill_between(higher_shade, kde.evaluate(higher_shade), color='grey', alpha=0.5)

ax.set_ylim((0, 1.22))
ax2.set_ylim((0, 0.035))

yt2 = np.arange(0,0.0351,0.005)
yt2_text = [f'{a:.3f}' for a in yt2]
ax2.set_yticks(yt2)
ax2.set_yticklabels(yt2_text, fontdict=ticks_font)
ax2.yaxis.set_major_formatter(formatter)
yt1 = np.arange(0,1.21,0.2)
yt1_text = [f'{a:.1f}' for a in yt1]
ax.set_yticks(yt1)
ax.set_yticklabels(yt1_text, fontdict=ticks_font)


plt.xlim((-0.5, 120.5))

ax.set_xticklabels(np.arange(-20,121,20), fontdict=ticks_font)
ax2.legend(prop=legend_font, loc='upper center', frameon=False, ncol=2)
ax.set_ylabel('Relevance', labelpad=10, fontdict=label_font)
ax2.set_ylabel('Density', labelpad=10, fontdict=label_font)
ax.set_xlabel(u'T$_{opt} $ (\N{DEGREE SIGN}C)', fontdict=label_font)

plt.tight_layout()
plt.savefig('plots/fig1b_onesided_relevance.pdf')
plt.show()
plt.close()




# Two-sided 
yrange = np.arange(0, 120.1, step=0.5)
cl1, ch1 = [np.percentile(y, pp) for pp in [10, 90]]
rel = resreg.sigmoid_relevance(yrange, cl1, ch1)

ax = plt.subplot()
ax.plot(yrange, rel, label='Relevance', color='crimson', linewidth=2)
#ax.axhline(0.5, linestyle='--', color='grey')
ax.hlines(0.5, xmin=0, xmax=120, linestyle='--', color='grey')
ax.vlines(25, ymin=0, ymax=0.5, linestyle='--', color='grey')
ax.vlines(72.2, ymin=0, ymax=0.5, linestyle='--', color='grey')
ax.text(x=5, y=0.53, s=u't$_{R}$=0.5', fontdict=legend_font)

kde = gaussian_kde(y, bw_method=0.4)
dens = kde.evaluate(yrange)
ax2 = ax.twinx()
ax2.plot(yrange, np.ones(len(yrange))*3, color='crimson', label='Relevance')  # Just for legend
ax2.plot(yrange, dens, color='black', label='Density')

lower_shade = np.arange(0, 25.1, step=1)
higher_shade = np.arange(72, 120.1, step=1)
ax2.fill_between(lower_shade, kde.evaluate(lower_shade), color='grey', alpha=0.5)
ax2.fill_between(higher_shade, kde.evaluate(higher_shade), color='grey', alpha=0.5)

ax.set_ylim((0, 1.25))
ax2.set_ylim((0, 0.035))

yt1 = np.arange(0,1.21,0.2)
yt1_text = [f'{a:.1f}' for a in yt1]
ax.set_yticks(yt1)
ax.set_yticklabels(yt1_text, fontdict=ticks_font)
yt2 = np.arange(0,0.0351,0.005)
yt2_text = [f'{a:.3f}' for a in yt2]
ax2.set_yticks(yt2)
ax2.set_yticklabels(yt2_text, fontdict=ticks_font)
ax2.yaxis.set_major_formatter(formatter)

plt.xlim((-0.5, 120.5))

ax.set_xticklabels(np.arange(-20,121,20), fontdict=ticks_font)
ax2.legend(prop=legend_font, loc='upper center', frameon=False, ncol=2)
ax.set_ylabel('Relevance', labelpad=10, fontdict=label_font)
ax2.set_ylabel('Density', labelpad=10, fontdict=label_font)
ax.set_xlabel(u'T$_{opt} $ (\N{DEGREE SIGN}C)', fontdict=label_font)

plt.tight_layout()
plt.savefig('plots/fig1c_twosided_relevance.pdf')
plt.show()
plt.close()






# Table 3: Best hyperparameter combination for resampling strategies
#=====================================================================#
strategies = ['RO', 'SMOTER', 'GN', 'WERCS', 'WERCS-GN', 'REBAGG-RO', 
              'REBAGG-SMOTER', 'REBAGG-GN', 'REBAGG-WERCS', 'REBAGG-WERCS-GN']
best = pd.DataFrame()
for strategy in strategies:
    filename = f'results/{strategy}.xlsx'
    ex = pd.read_excel(filename, index_col=0)
    ex_sorted = ex.sort_values('r2', ascending=False)
    best[strategy] = ex_sorted.iloc[0,:]
best = best.transpose()
best_params = best['params']
best_params.to_excel('results/best_params.xlsx')






# Figure 2A: Best R2 of resampling strategies
#================================================#
ex_tome = pd.read_excel('results/TOME.xlsx', index_col=0)
div = np.sqrt(50)/1.96   # 95% confidence interval
strategies = ['RO', 'SMOTER', 'GN', 'WERCS', 'WERCS-GN', 'REBAGG-RO', 
              'REBAGG-SMOTER', 'REBAGG-GN', 'REBAGG-WERCS', 'REBAGG-WERCS-GN']
shortform = ['TOME', 'RO', 'SMOTER', 'GN', 'WERCS', 'WERCS-GN', 'BAGG-RO', 'BAGG-SMT', 
             'BAGG-GN', 'BAGG-WERCS','BAGG-WRGN']
r2s, r2stds = [ex_tome.loc['r2', 'means']], [ex_tome.loc['r2', 'stds']]
for strategy in strategies:
    ex = pd.read_excel('results/{0}.xlsx'.format(strategy), index_col=0)
    ex = ex.sort_values(['r2'], ascending=False)
    r2s.append(ex['r2'].iloc[0])
    r2stds.append(ex['r2_std'].iloc[0])

fnt='Arial'
ticks_font = {'fontname':fnt, 'size':'19'}
label_font = {'family':fnt, 'size':'26'}
plt.rcParams['figure.figsize'] = [6,6.3]

markersize = 9
capsize = 6
elinewidth = 2
color = 'blue'
ecolor = color

plt.errorbar(range(len(r2s)), r2s, fmt='o', yerr=r2stds/div, 
             color=color, ecolor=ecolor, elinewidth=elinewidth, markersize=markersize, 
             capsize=capsize)

plt.ylim(0.50,0.65)
plt.xticks(range(len(shortform)), shortform, rotation=90, **ticks_font)
plt.yticks(**ticks_font)
plt.ylabel('R$^2$', labelpad=10, **label_font)
plt.tight_layout()
plt.savefig('plots/fig2a_best_r2.pdf')
plt.show()
plt.close()






# Figure 2B: Best MCC of resampling strategies
#================================================#
ex_tome = pd.read_excel('results/TOME.xlsx', index_col=0)
div = np.sqrt(50)/1.96
strategies = ['RO', 'SMOTER', 'GN', 'WERCS', 'WERCS-GN', 'REBAGG-RO', 
              'REBAGG-SMOTER', 'REBAGG-GN', 'REBAGG-WERCS', 'REBAGG-WERCS-GN']
shortform = ['TOME', 'RO', 'SMOTER', 'GN', 'WERCS', 'WERCS-GN', 'BAGG-RO', 'BAGG-SMT', 
             'BAGG-GN', 'BAGG-WERCS','BAGG-WRGN']
mccs, mccstds = [ex_tome.loc['mcc', 'means']], [ex_tome.loc['mcc', 'stds']]
for strategy in strategies:
    ex = pd.read_excel('results/{0}.xlsx'.format(strategy), index_col=0)
    ex = ex.sort_values(['mcc'], ascending=False)
    mccs.append(ex['mcc'].iloc[0])
    mccstds.append(ex['mcc_std'].iloc[0])

fnt='Arial'
ticks_font = {'fontname':fnt, 'size':'19'}
label_font = {'family':fnt, 'size':'26'}
plt.rcParams['figure.figsize'] = [6,6.3]

markersize = 9
capsize = 6
elinewidth = 2
color = 'blueviolet'
ecolor = color

plt.errorbar(range(len(mccs)), mccs, fmt='o', yerr=mccstds/div, 
             color=color, ecolor=ecolor, elinewidth=elinewidth, markersize=markersize, 
             capsize=capsize)

plt.ylim(0.20,0.28)
plt.xticks(range(len(shortform)), shortform, rotation=90, **ticks_font)
plt.yticks(np.arange(0.20, 0.29, step=0.02), **ticks_font)
plt.ylabel('MCC', labelpad=10, **label_font)
plt.tight_layout()
plt.savefig('plots/fig2b_best_mcc.pdf')
plt.show()
plt.close()






# Figure 2C: Best F1 of resampling strategies
#================================================#
ex_tome = pd.read_excel('results/TOME.xlsx', index_col=0)
div = np.sqrt(50)/1.96
strategies = ['RO', 'SMOTER', 'GN', 'WERCS', 'WERCS-GN', 'REBAGG-RO', 
              'REBAGG-SMOTER', 'REBAGG-GN', 'REBAGG-WERCS', 'REBAGG-WERCS-GN']
shortform = ['TOME', 'RO', 'SMOTER', 'GN', 'WERCS', 'WERCS-GN', 'BAGG-RO', 'BAGG-SMT', 
             'BAGG-GN', 'BAGG-WERCS','BAGG-WRGN']
f1s, f1stds = [ex_tome.loc['f1', 'means']], [ex_tome.loc['f1', 'stds']]
for strategy in strategies:
    ex = pd.read_excel('results/{0}.xlsx'.format(strategy), index_col=0)
    ex = ex.sort_values(['f1'], ascending=False)
    f1s.append(ex['f1'].iloc[0])
    f1stds.append(ex['f1_std'].iloc[0])

fnt='Arial'
ticks_font = {'fontname':fnt, 'size':'19'}
label_font = {'family':fnt, 'size':'26'}
plt.rcParams['figure.figsize'] = [6,6.3]

markersize = 9
capsize = 6
elinewidth = 2
color = 'forestgreen'
ecolor = color

plt.errorbar(range(len(f1s)), f1s, fmt='o', yerr=f1stds/div, 
             color=color, ecolor=ecolor, elinewidth=elinewidth, markersize=markersize, 
             capsize=capsize)

plt.ylim(0.12,0.30)
plt.xticks(range(len(shortform)), shortform, rotation=90, **ticks_font)
plt.yticks(np.arange(0.12, 0.32, step=0.04), **ticks_font)
plt.ylabel('F$_1$ score', labelpad=10, **label_font)
plt.tight_layout()
plt.savefig('plots/fig2c_best_f1.pdf')
plt.show()
plt.close()






# Figure 2D: MSE over bins
#===============================#
strategies = ['TOME', 'RO', 'SMOTER', 'GN', 'WERCS', 'WERCS-GN', 'REBAGG-RO', 
              'REBAGG-SMOTER', 'REBAGG-GN', 'REBAGG-WERCS', 'REBAGG-WERCS-GN']

shortform = ['TOME', 'RO', 'SMOTER', 'GN', 'WERCS', 'WERCS-GN', 'BAGG-RO', 'BAGG-SMT', 
             'BAGG-GN', 'BAGG-WERCS','BAGG-WRGN']
mse_list, std_list = [], []
for strategy in strategies:
    if strategy is 'TOME':
        ex = pd.read_excel('results/TOME.xlsx', index_col=0)
        mse = ex.loc[['mse_bin1', 'mse_bin2', 'mse_bin3', 'mse_bin4', 'mse_bin5'], 'means']
        mse_list.append(mse.values)
        std = ex.loc[['mse_bin1', 'mse_bin2', 'mse_bin3', 'mse_bin4', 'mse_bin5'], 'stds']
        std_list.append(std.values)
    else:    
        ex = pd.read_excel('results/{0}.xlsx'.format(strategy), index_col=0)
        ex = ex.sort_values(['r2'], ascending=False)
        mse = ex.iloc[0,:].loc[['mse_bin1', 'mse_bin2', 'mse_bin3', 'mse_bin4', 'mse_bin5']]
        mse_list.append(mse.values)
        std = ex.iloc[0,:].loc[['mse_bin1_std', 'mse_bin2_std', 'mse_bin3_std', 'mse_bin4_std', 'mse_bin5_std']]
        std_list.append(std.values)

msedf = pd.DataFrame(mse_list)
stddf = pd.DataFrame(std_list)

fnt='Arial'
ticks_font = {'fontname':fnt, 'size':'11'}
legend_font = {'family':fnt, 'size':'9'}
label_font = {'family':fnt, 'size':'14'}
plt.rcParams['figure.figsize'] = [7.75,3]

xx = np.arange(len(msedf)) * 7
div = np.sqrt(50)/1.96
add = [-2, -1, 0, 1, 2]
error_kw=dict(lw=0.75, capsize=1.0, capthick=0.75)

pltout = []
legend_label = ['0-30', '30-50', '50-65', '65-85', '85-120']
legend_label = [x + '\N{DEGREE SIGN}C' for x in legend_label]
color = [ 'dimgrey', 'blue', 'green', 'peru', 'brown']
for i in range(len(msedf.columns)):
    out = plt.bar(xx + i - 2, msedf.iloc[:,i], yerr=stddf.iloc[:,i]/div,
                  color=color[i], linewidth=1.10, edgecolor='black', width=1.0, 
                  error_kw=error_kw)
    pltout.append(out[0])

plt.xticks(xx, shortform, rotation=90, **ticks_font)
plt.yticks(**ticks_font)
plt.ylim((0, 800))
plt.ylabel('MSE', **label_font)
plt.legend(pltout, legend_label, frameon=0, numpoints=1, shadow=0, loc='upper right', 
           bbox_to_anchor=(1.0,1.0), ncol=3, prop=legend_font)
plt.tight_layout()
plt.savefig('plots/fig2d_msebins.pdf')
plt.show()
plt.close()
    





# Figure 2E: Distribution after resampling
#============================================#
fnt='Arial'
ticks_font = {'fontname':fnt, 'size':'18'}
legend_font = {'family':fnt, 'size':'13'}
label_font = {'family':fnt, 'size':'20'}
title_font = {'family':fnt, 'size':'22'}
plt.rcParams['figure.figsize'] = [6,4.8]

params = {'mathtext.default': 'regular' }        
plt.rcParams.update(params)
plt.rc('font', size=12)


strategies = ['None', 'RO', 'SMOTER', 'GN', 'WERCS', 'WERCS-GN']
bins = [30, 50, 65, 85]
lw = 2
style1 = '-'
style2 = '--'

for strategy in strategies:
    train_indices, test_indices = resreg.uniform_test_split(X, y, bins=bins, 
                                        bin_test_size=70, verbose=False, random_state=0)
    X_train, y_train = X[train_indices,:], y[train_indices]
    
    if strategy=='None':
        sns.kdeplot(y_train, bw=7, linewidth=lw, linestyle=style1, color='black', 
                    label='TOME')     
        
    elif strategy=='RO':
        relevance = resreg.sigmoid_relevance(y_train, cl=None, ch=60)
        X_train, y_train = resreg.random_oversample(X_train, y_train, relevance=relevance,
                                        relevance_threshold=0.5, over='balance', 
                                        random_state=0)
        sns.kdeplot(y_train, bw=7, linewidth=lw, label=strategy, color='blue', 
                    linestyle=style2)       
    
    elif strategy=='SMOTER':
        relevance = resreg.sigmoid_relevance(y_train, cl=None, ch=60)
        X_train, y_train = resreg.smoter(X_train, y_train, relevance=relevance, 
                                    relevance_threshold=0.5, k=10, over='average', 
                                    random_state=0)
        sns.kdeplot(y_train, bw=7, linewidth=lw, label=strategy, color='red', 
                    linestyle=style2)       
    
    elif strategy=='GN':
        relevance = resreg.sigmoid_relevance(y_train, cl=None, ch=72.2)
        X_train, y_train = resreg.gaussian_noise(X_train, y_train, relevance=relevance,
                                    relevance_threshold=0.5, delta=0.5, over='balance',
                                    random_state=0)
        sns.kdeplot(y_train, bw=7, linewidth=lw, label=strategy, color='magenta',
                    linestyle=style2)       
    
    elif strategy=='WERCS':
        relevance = resreg.sigmoid_relevance(y_train, cl=None, ch=72.2)
        X_train, y_train = resreg.wercs(X_train, y_train, relevance=relevance, over=0.5,
                                        under=0.5, noise=False, random_state=0)
        sns.kdeplot(y_train, bw=7, linewidth=lw, label=strategy, color='goldenrod',
                    linestyle=style2)
    elif strategy=='WERCS-GN':
        relevance = resreg.sigmoid_relevance(y_train, cl=None, ch=72.2)
        X_train, y_train = resreg.wercs(X_train, y_train, relevance=relevance, over=0.5,
                                        under=0.5, noise=True, delta=0.1, random_state=10)
        sns.kdeplot(y_train, bw=7, linewidth=lw, label=strategy, color='green',
                    linestyle=style2)       
    
plt.xlim((0,120)) 
plt.ylim(0, 0.040)
plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0), useMathText=True)
plt.xticks(**ticks_font)
plt.yticks(**ticks_font)
plt.xlabel(u'T$_{opt} $ (\N{DEGREE SIGN}C)', **label_font)
plt.ylabel('Density', labelpad=10, **label_font)

plt.legend(prop=legend_font, ncol=2, frameon=0, loc='upper center')
plt.tight_layout()
plt.savefig('plots/fig2e_resamp_dist.pdf')
plt.show()
plt.close()






# Figure 2F: Difference between training and testing error
#===============================================================#
strategies = ['TOME', 'RO', 'SMOTER', 'GN', 'WERCS', 'WERCS-GN', 'REBAGG-RO', 
              'REBAGG-SMOTER', 'REBAGG-GN', 'REBAGG-WERCS', 'REBAGG-WERCS-GN']

shortform = ['TOME', 'RO', 'SMOTER', 'GN', 'WERCS', 'WERCS-GN', 'BAGG-RO', 'BAGG-SMT', 
             'BAGG-GN', 'BAGG-WERCS','BAGG-WRGN']
bins = [30, 50, 65, 85]


# Evaluate training and testing error
msetrainstore, mseteststore = [], []
for i in range(50):
    print(i)
    storetrain, storetest = [], []
    
    for strategy in strategies:
        train_indices, test_indices = resreg.uniform_test_split(X, y, bins=bins, 
                                                    bin_test_size=70, verbose=False, 
                                                    random_state=i)
        X_train, y_train = X[train_indices,:], y[train_indices]
        X_test, y_test = X[test_indices,:], y[test_indices]
        
        if 'BAGG' not in strategy:
            if strategy=='TOME':
                pass
                
            elif strategy=='RO':
                relevance = resreg.sigmoid_relevance(y_train, cl=None, ch=60)
                X_train, y_train = resreg.random_oversample(X_train, y_train, 
                                        relevance=relevance, relevance_threshold=0.5, 
                                        over='balance', random_state=i)
            
            elif strategy=='SMOTER':
                relevance = resreg.sigmoid_relevance(y_train, cl=None, ch=60)
                X_train, y_train = resreg.smoter(X_train, y_train, relevance=relevance, 
                                        relevance_threshold=0.5, k=10, over='average', 
                                        random_state=i)
            elif strategy=='GN':
                relevance = resreg.sigmoid_relevance(y_train, cl=None, ch=72.2)
                X_train, y_train = resreg.gaussian_noise(X_train, y_train, 
                                        relevance=relevance, relevance_threshold=0.5, 
                                        delta=0.5, over='balance', random_state=i)
    
            elif strategy=='WERCS':
                relevance = resreg.sigmoid_relevance(y_train, cl=None, ch=72.2)
                X_train, y_train = resreg.wercs(X_train, y_train, relevance=relevance, 
                                        over=0.5, under=0.5, noise=False, random_state=i)
    
            elif strategy=='WERCS-GN':
                relevance = resreg.sigmoid_relevance(y_train, cl=None, ch=72.2)
                X_train, y_train = resreg.wercs(X_train, y_train, relevance=relevance, 
                                        over=0.5, under=0.5, noise=True, delta=0.1, 
                                        random_state=i)
        
            reg = RandomForestRegressor(n_jobs=-1, n_estimators=10, random_state=i)
            reg.fit(X_train, y_train)
            y_pred_train = reg.predict(X_train)
            y_pred_test = reg.predict(X_test)
        
        else:
            base_reg = DecisionTreeRegressor(random_state=i)
            
            if strategy=='REBAGG-RO':
                relevance = resreg.sigmoid_relevance(y_train, cl=None, ch=72.2)
                rebagg = resreg.Rebagg(m=100, s=600, base_reg=base_reg)
                rebagg.fit(X_train, y_train, relevance, relevance_threshold=0.5, 
                   sample_method='random_oversample', size_method='variation', 
                   random_state=i)
    
            
            elif strategy=='REBAGG-SMOTER':
                relevance = resreg.sigmoid_relevance(y_train, cl=None, ch=72.2)
                rebagg = resreg.Rebagg(m=100, s=600, base_reg=base_reg)
                rebagg.fit(X_train, y_train, relevance, relevance_threshold=0.5, 
                           sample_method='smoter', size_method='variation', k=5, 
                           random_state=i)
            elif strategy=='REBAGG-GN':
                relevance = resreg.sigmoid_relevance(y_train, cl=None, ch=72.2)
                rebagg = resreg.Rebagg(m=100, s=600, base_reg=base_reg)
                rebagg.fit(X_train, y_train, relevance, relevance_threshold=0.5, 
                          sample_method='gaussian', size_method='variation', delta=1.0, 
                          random_state=i)
        
            elif strategy=='REBAGG-WERCS':
                relevance = resreg.sigmoid_relevance(y_train, cl=25, ch=60)
                rebagg = resreg.Rebagg(m=100, s=600, base_reg=base_reg)
                rebagg.fit(X_train, y_train, relevance=relevance, sample_method='wercs', 
                           over=0.5, under=0.75, random_state=i)
           
            elif strategy=='REBAGG-WERCS-GN':
                relevance = resreg.sigmoid_relevance(y_train, cl=25, ch=60)
                rebagg = resreg.Rebagg(m=100, s=600, base_reg=base_reg)
                rebagg.fit(X_train, y_train, relevance=relevance, sample_method='wercs-gn', 
                           over=0.5, under=0.75, delta=0.1, random_state=i)
        
            y_pred_train = rebagg.predict(X_train)
            y_pred_test = rebagg.predict(X_test)
        
        mse_train = mean_squared_error(y_train, y_pred_train)
        mse_test = mean_squared_error(y_test, y_pred_test)
        storetrain.append(mse_train)
        storetest.append(mse_test)
    msetrainstore.append(storetrain)
    mseteststore.append(storetest)
        
dftrain = pd.DataFrame(msetrainstore)
dftest = pd.DataFrame(mseteststore)
error = pd.DataFrame()
error['train_error'] = dftrain.mean(axis=0).values
error['train_error_std'] = dftrain.std(axis=0).values
error['test_error'] = dftest.mean(axis=0).values
error['test_error_std'] = dftest.std(axis=0).values
error.index = strategies
error.to_excel('results/train_test_error.xlsx')




# Plot train and test error
ex = pd.read_excel('results/train_test_error.xlsx', index_col=0)

div = np.sqrt(50)/1.96
trainerror = ex['train_error'].values
testerror = ex['test_error'].values
trainconf = ex['train_error_std'].values/div
testconf = ex['test_error_std'].values/div



fnt='Arial'
ticks_font = {'fontname':fnt, 'size':'16'}
legend_font = {'family':fnt, 'size':'16'}
label_font = {'family':fnt, 'size':'20'}
title_font = {'family':fnt, 'size':'22'}
plt.rcParams['figure.figsize'] = [6,5.28]           
error_kw=dict(lw=1.2, capsize=3.0, capthick=1.2)

shortform = ['TOME', 'RO', 'SMOTER', 'GN', 'WERCS', 'WERCS-GN', 'BAGG-RO', 'BAGG-SMT', 
             'BAGG-GN', 'BAGG-WERCS','BAGG-WRGN']

plt.errorbar(range(len(testerror)), testerror, color='crimson', linewidth=2, marker='o', 
             yerr=testconf, capsize=3)
plt.errorbar(range(len(trainerror)), trainerror, color='blue', linewidth=2, marker='o', 
             yerr=trainconf, capsize=3)
plt.plot(testerror, color='crimson', label='Testing error')  # Just for legend         
plt.plot(trainerror, color='blue', label='Training error')
for i in range(len(trainerror)):
    plt.vlines(i, trainerror[i], testerror[i], color='grey', linestyle='--')
plt.xticks(range(len(trainerror)), shortform, rotation=90, **ticks_font)
plt.yticks(**ticks_font)
plt.ylabel('MSE', labelpad=10, **label_font)
plt.legend(prop=legend_font, loc='upper right', frameon=0, ncol=1)
plt.ylim(0,325)
plt.tight_layout()
plt.savefig('plots/fig2f_train_test_error.pdf')
plt.show()
plt.close()






# Figure S1: R2 of hyperparameter combinations for all strategies
#====================================================================#
strategies = ['RO', 'SMOTER', 'GN', 'WERCS', 'WERCS-GN', 'REBAGG-RO', 
              'REBAGG-SMOTER', 'REBAGG-GN', 'REBAGG-WERCS', 'REBAGG-WERCS-GN']

shortform = ['RO', 'SMOTER', 'GN', 'WERCS', 'WERCS-GN', 'BAGG-RO', 'BAGG-SMT', 
             'BAGG-GN', 'BAGG-WERCS','BAGG-WRGN']

fnt='Arial'
ticks_font = {'fontname':fnt, 'size':'18'}
legend_font = {'family':fnt, 'size':'15'}
label_font = {'family':fnt, 'size':'22'}
title_font = {'family':fnt, 'size':'22'}
plt.rcParams['figure.figsize'] = [6,4]

markersize = 9
capsize = 3
elinewidth = 1
color = 'blue'
color2 = 'red'

div = np.sqrt(50)/1.96
ex_tome = pd.read_excel('results/TOME.xlsx', index_col=0)
r2_tome, r2_std_tome = ex_tome.loc['r2', ['means', 'stds']]
r2_std_tome = r2_std_tome/div



for strategy, short in zip(strategies, shortform):
    ex = pd.read_excel(f'results/{strategy}.xlsx', index_col=0).sort_index()
    r2_vals, r2_stds = ex['r2'].values, ex['r2_std'].values
    r2_stds = r2_stds/div
    
    plt.errorbar(range(len(r2_vals)), r2_vals, fmt='.', yerr=r2_stds, color=color,
                 ecolor=color, elinewidth=elinewidth, markersize=markersize, 
                 capsize=capsize)
    
    xx = range(0-5, len(r2_vals)+5)
    plt.axhline(r2_tome, color=color2, linestyle='-', linewidth=1.25)
    plt.fill_between(xx, y1 = np.ones(len(xx)) * r2_tome, 
                     y2 = np.ones(len(xx)) * (r2_tome + r2_std_tome), color=color2,
                     alpha=0.2)
    plt.fill_between(xx, y1 = np.ones(len(xx)) * r2_tome, 
                     y2 = np.ones(len(xx)) * (r2_tome - r2_std_tome), color=color2,
                     alpha=0.2)
    
    plt.xticks([])
    plt.yticks(**ticks_font)
    plt.xlim(-1, len(r2_vals))
    plt.ylabel('R$^2$', **label_font)
    plt.title(short, **title_font)
    plt.tight_layout()
    plt.savefig(f'plots/figs1_r2_all/{strategy}.pdf')
    plt.show()
    plt.close()
    
    
    
    

# Figure 3: Performance of different base learners
#======================================================#
ex_tome = pd.read_excel('results/TOME.xlsx', index_col=0)
ex_dectree = pd.read_excel('results/REBAGG-RO.xlsx', 
                           index_col=0).sort_values('r2', ascending=False)
reg_other = ['SVR', 'KNR', 'ENET', 'BAYR']
div = np.sqrt(50)/1.96

titles = ['a', 'b', 'c']
metrics = ['r2', 'mcc', 'f1']
colors = ['blue', 'blueviolet', 'forestgreen']
labels = ['R$^2$', 'MCC', 'F$_1$ score']

markersize = 9
capsize = 6
elinewidth = 2

fnt='Arial'
ticks_font = {'fontname':fnt, 'size':'20'}
label_font = {'family':fnt, 'size':'30'}
plt.rcParams['figure.figsize'] = [6,6.3]

for title, metric, color, label in zip(titles, metrics, colors, labels):
    average = [ex_tome.loc[metric, 'means'], ex_dectree.iloc[0,:].loc[metric]]
    std = [ex_tome.loc[metric, 'stds'], ex_dectree.iloc[0,:].loc[metric + '_std']]
    for reg in reg_other:
        ex_reg = pd.read_excel('results/base_regressors/{0}.xlsx'.format(reg), 
                               index_col=0)
        ex_reg = ex_reg.sort_values('r2', ascending=False)
        average.append(ex_reg.iloc[0,:].loc[metric])
        std.append(ex_reg.iloc[0,:].loc[metric + '_std'])
    
    plt.errorbar(range(len(average)), average, fmt='o', yerr=np.array(std)/div,
                 color=color, ecolor=color, markersize=markersize, capsize=capsize, 
                 elinewidth=elinewidth)
    plt.xticks(range(len(average)), ['TOME', 'DEC-TREE'] + reg_other, **ticks_font,
               rotation=90)
    plt.yticks(**ticks_font)
    plt.ylabel(label, labelpad=10, **label_font)
    plt.tight_layout()
    plt.savefig(f'plots/fig3{title}_{metric}_diff_reg.pdf')
    plt.show()
    plt.close()
        


# Graphical Abstract
#============================#
ex_tome = pd.read_excel('results/TOME.xlsx', index_col=0)
ex_tomer = pd.read_excel('results/REBAGG-RO.xlsx', 
                         index_col=0).sort_values('r2', ascending=False)

msebins = ['mse_bin{0}'.format(x) for x in range(1,6)]
stdbins = ['mse_bin{0}_std'.format(x) for x in range(1,6)]
mse_tome = ex_tome.loc[msebins,'means'].values
std_tome = ex_tome.loc[msebins,'stds'].values
mse_tomer = ex_tomer.iloc[0].loc[msebins].values
std_tomer = ex_tomer.iloc[0].loc[stdbins].values


err_more65 = (1 - np.sum(mse_tomer[-2:])/np.sum(mse_tome[-2:])) * 100  # TOMER reduces error by 50%
err_more85 = (1 - mse_tomer[-1]/mse_tome[-1]) * 100 # TOMER reduces error by 60%

less = [np.mean(array[:4]) for array in [mse_tome, mse_tomer]]
more = [np.mean(array[4:]) for array in [mse_tome, mse_tomer]]
less_std = [np.sqrt(np.sum(array[:3]**2))/len(array) for array in [std_tome, std_tomer]]
more_std = [np.sqrt(np.sum(array[3:]**2))/len(array) for array in [std_tome, std_tomer]]
#div = np.sqrt(50)/3.50   # 99.95% conf interval
div = 1   # standard deviation

error_kw=dict(lw=0.5, capsize=1.5, capthick=0.5)
linewidth = 0.6
edgecolor = 'black'

fnt='Arial'
ticks_font = {'fontname':fnt, 'size':'8'}
label_font = {'fontname':fnt, 'size':'8'}
legend_font = {'family':fnt, 'size':'6'}
plt.rcParams['figure.figsize'] = [2.1, 1.75]



plt.bar([2, 5], less, color='blue', yerr=np.array(less_std)/div, label='< 85°C',
        width=0.95, error_kw=error_kw, linewidth=linewidth, edgecolor=edgecolor)
plt.bar([3, 6], more, color='crimson', yerr=np.array(more_std)/div, label='> 85°C',
        width=0.95, error_kw=error_kw, linewidth=linewidth, edgecolor=edgecolor)
plt.legend(loc='upper right', prop=legend_font)
plt.ylabel('Mean squared error (MSE)', **label_font)
plt.xticks([2.5, 5.5], ['TOME', 'TOMER'], **ticks_font)
plt.yticks(np.arange(0, 701, step=200), **ticks_font)
plt.tight_layout()
plt.savefig('plots/fig0_abstract.tiff', dpi=600)
plt.show()
plt.close()







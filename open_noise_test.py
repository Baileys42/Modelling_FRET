import numpy as np
import matplotlib.pyplot as plt
from pandas.io.pytables import IndexCol
import seaborn as sns
import pandas as pd
import os
import shutil
import glob as glob

folder = 'C:/Users/clj713/Bailey_2/Simulated_FRET_Data/Modelling_FRET/Mean_RMSD_output/Noise_Test/'
d = {}
empty_df = []
empty_df = pd.DataFrame(empty_df)
for file in os.listdir(folder):
    name = folder + file
    data = pd.read_csv(name, header=None)
    d[file] = data
#print(d)

for dfs in d:
    new_df = pd.DataFrame(d[dfs])
    empty_df[dfs] = new_df
    

empty_df = empty_df.sort_index(axis=1)

empty_df

df_values = {'1x\nNoise' : [empty_df.iloc[0,1]], '1.5x\nNoise' : [empty_df.iloc[0,0]], 
'2x\nNoise' : [empty_df.iloc[0,3]], '2.5x\nNoise' : [empty_df.iloc[0,2]], 
'3\nNoise' : [empty_df.iloc[0,5]], '3.5x\nNoise' : [empty_df.iloc[0,4]], 
'4x\nNoise' : [empty_df.iloc[0,6]]
}

new_df = pd.DataFrame(df_values)
print(new_df)

column_chart_x = ['1x\nNoise', '1.5\nNoise', '2x\nNoise', '2.5x\nNoise', '3x\nNoise', '3.5x\nNoise', '4x\nNoise']
values = [empty_df.iloc[0,1],empty_df.iloc[0,0], empty_df.iloc[0,3], empty_df.iloc[0,2], empty_df.iloc[0,5],empty_df.iloc[0,4], empty_df.iloc[0,6]]




def show_figure():
    plt.bar(column_chart_x,values,color="darkorange")
    plt.xlabel('Noise level')
    plt.ylabel('Mean RMSD')

show_figure()
#plot = sns.heatmap(new_df, vmin=0, vmax = 0.85, square =True, linewidths=True, cmap='inferno', annot = True)
#plot.set_xticklabels(plot.get_xticklabels(), rotation = 0)
#plot.set_yticklabels(plot.get_yticklabels(), rotation = 0)


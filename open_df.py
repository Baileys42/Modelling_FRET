import numpy as np
import matplotlib.pyplot as plt
from pandas.io.pytables import IndexCol
import seaborn as sns
import pandas as pd
import os
import shutil
import glob as glob

folder = 'C:/Users/clj713/Bailey_2/Simulated_FRET_Data/Modelling_FRET/Mean_RMSD_output/First_Molecules/'
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
    
print(empty_df)
row_1 = pd.DataFrame([empty_df.iloc[0,2], empty_df.iloc[0,1],empty_df.iloc[0,0]])

row_2 = pd.DataFrame([empty_df.iloc[0,5],empty_df.iloc[0,4],empty_df.iloc[0,3]])

row_3 = pd.DataFrame([empty_df.iloc[0,8], empty_df.iloc[0,7], empty_df.iloc[0,6]])

#print(row_1)


df_values = {'FRET efficiency transition' : ['∆ 0.6', '∆ 0.4', '∆ 0.2', '∆ 0.1', '∆ 0.05'], 
'Low\nNoise' : [(empty_df.iloc[0,2]), (empty_df.iloc[0,5]), (empty_df.iloc[0,8]), (empty_df.iloc[0,14]), (empty_df.iloc[0,11])],
'Medium\nNoise' : [(empty_df.iloc[0,1]), (empty_df.iloc[0,4]), (empty_df.iloc[0,7]), (empty_df.iloc[0,13]), (empty_df.iloc[0,10])],
'High\nNoise' : [(empty_df.iloc[0,0]), (empty_df.iloc[0,3]), (empty_df.iloc[0,6]), (empty_df.iloc[0,12]), (empty_df.iloc[0,9])]
}


new_df = pd.DataFrame(df_values)

new_df.set_index('FRET efficiency transition', inplace=True)

print(new_df)


plot = sns.heatmap(new_df, vmin=0, vmax = 0.2, square =True, linewidths=True, cmap='inferno', annot = True)
plot.set_xticklabels(plot.get_xticklabels(), rotation = 0)
plot.set_yticklabels(plot.get_yticklabels(), rotation = 0)
plt.figure(figsize= (10,10))
plt.show()
#format_df['']
#format_df.columns = ['Low Noise', 'Medium Noise', 'High Noise']

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import shutil
import glob as glob




data_path = ["C:/Users/clj713/Bailey_2/Simulated_FRET_Data/Trace_Output/vbFRET_output/Test_1/"]

output = "C:/Users/clj713/Bailey_2/Simulated_FRET_Data/Modelling_FRET/vbFRET_file_output/"

### finds text files in input folder and moves to output folder
def get_trace_file(input_folder, output):
    for folder in input_folder:
        new_folder = folder.split("/")[-2]
        if not os.path.exists(f"{output}{new_folder}/"):
            os.makedirs(f"{output}{new_folder}/")
        tracelist = [trace for trace in os.listdir(folder) if ".dat" in trace]
        for trace in tracelist:
            shutil.copyfile(f"{folder}{trace}",f"{output}{new_folder}/{trace}")
get_trace_file(data_path, output)

### failed import function
def load_trace(file):
    trace_df = pd.DataFrame(np.loadtext(file))
    trace_df.columns("time", "donor", "acceptor", "FRET", "Idealised")
    return trace_df


### failed import function
def file_read(input_folder):
    os.chdir(input_folder)
    filename = glob.glob(input_folder + "/*.dat")
    dfs = []
    for file in filename:
        dfs.append(pd.read_csv(filename))
    df = pd.concat(dfs)
    df = pd.DataFrame(df)
    return df

compiled_df = []
new_folder = "C:/Users/clj713/Bailey_2/Simulated_FRET_Data/Modelling_FRET/vbFRET_file_output/Test_1/"
bug = new_folder + "test.dat"
print(bug)

d = {}

for file in os.listdir(new_folder):
    name = new_folder + file
    df_name = "Trace_No_" + str(file[:1])
    print(df_name)
    data = pd.read_csv(name, sep = '\s+', engine = 'python')
    data.columns = ["time", "donor", "acceptor", "FRET", "Idealised"]
    d[df_name] = data



idealised_FRET = []
idealised_FRET = pd.DataFrame(idealised_FRET)

for df in d:
    new_df = pd.DataFrame(d[df])
    #print(new_df)
    ideal = new_df["Idealised"]
    idealised_FRET[df] = ideal
#print(idealised_FRET)



### state value
state_input = 'C:/Users/clj713/Bailey_2/Simulated_FRET_Data/Trace_Output/True_state/Test_1/'
state_d = {}
state_df_values = []
state_df_values = pd.DataFrame(state_df_values)


for file in os.listdir(state_input):
    print('bug')
    state_name = state_input + file
    state_df_name = "Trace_No_" + str(file[-5])
    print(state_df_name)
    state_data = pd.read_csv(state_name)
    state_d[state_df_name] = state_data



#print(state_d)

for df in state_d:
    state_df = pd.DataFrame(state_d[df])
    state_df_values[df] = state_df

state_df_values = state_df_values[1:]
state_df_values = state_df_values.reset_index()

print('state_df')
#print(state_df_values)


difference = idealised_FRET.sub(state_df_values, axis=0)
#print(idealised_FRET)
#print(state_df_values)
print(difference)

trace_1_sum = difference["Trace_No_1"].sum()
trace_1_RMSD = np.sqrt(trace_1_sum/999)
print(trace_1_RMSD)
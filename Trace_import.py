import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import shutil
import glob as glob



### where vbFRET output files are
data_path = ["C:/Users/clj713/Bailey_2/Simulated_FRET_Data/Trace_Output/vbFRET_output/Noise_Increase_2/0.7_0.8_1x/"]
### folder to move .dat files to
output = "C:/Users/clj713/Bailey_2/Simulated_FRET_Data/Modelling_FRET/vbFRET_file_output/Noise_Increase_2/"

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


### new location for .dat files from vbFRET
compiled_df = []
new_folder = "C:/Users/clj713/Bailey_2/Simulated_FRET_Data/Modelling_FRET/vbFRET_file_output/Noise_Increase_2/0.7_0.8_1x/"

### imports text files and converts to pd.DataFrame --> then into dictionary of dfs
d = {}

for file in os.listdir(new_folder):
    name = new_folder + file
    #print('bug')
    df_name = "Trace_No_" + str(file[-11:-9])
    #print(df_name)
    data = pd.read_csv(name, sep = '\s+', engine = 'python')
    data.columns = ["time", "donor", "acceptor", "FRET", "Idealised"]
    d[df_name] = data


### generates data frame of idealised trace columns from each trace
idealised_FRET = []
idealised_FRET = pd.DataFrame(idealised_FRET)

for df in d:
    new_df = pd.DataFrame(d[df])
    #print(new_df)
    ideal = new_df["Idealised"]
    idealised_FRET[df] = ideal
#print(idealised_FRET)



### state value - where state value files are located
state_input = 'C:/Users/clj713/Bailey_2/Simulated_FRET_Data/Trace_Output/True_state/Noise_Increase_2/0.7_0.8_1x/'

### generates dictionary of pd.dfs that contain true fret state values
state_d = {}
state_df_values = []
state_df_values = pd.DataFrame(state_df_values)


for file in os.listdir(state_input):
    #print('bug2')
    state_name = state_input + file
    if file[-7] == '1':
        state_df_name = "Trace_No_100"
    else:
        state_df_name = "Trace_No_" + str(file[-6:-4])
    state_data = pd.read_csv(state_name)
    state_d[state_df_name] = state_data





for df in state_d:
    state_df = pd.DataFrame(state_d[df])
    state_df_values[df] = state_df


### reformatting state values 
state_df_values = state_df_values[1:]
state_df_values.reset_index(drop = True, inplace=True)
state_df_values = state_df_values.sort_index(axis=1)
#print(state_df_values)
#print(state_df_values)
#print(state_df_values)

### finds difference between predicted and observed values
difference = idealised_FRET.sub(state_df_values, axis=0)
#print(idealised_FRET["Trace_No_48"])
#print(state_df_values['Trace_No_48'])
#print(difference["Trace_No_49"])
#print(state_df_values)
#print(difference)



### function to count number of states fitted to data
state_number = []
def num_states(input):
    tolist = input.to_list()
    newset = set(tolist)
    number = len(newset)
    print(newset)
    state_number.append(number)

def num_states_2(input):
    tolist = input.to_list()
    nplist = np.array(tolist)
    unique, freq = np.unique(nplist, return_counts = True)
    #print(unique)
    true_freq = []
    for index, value in enumerate(freq):
        if value > 10:
            true_freq.append(unique[index])
        else:
            pass
    length = len(true_freq)
    state_number.append(length)



print('ideal')
#print(idealised_FRET)

for column in idealised_FRET.columns:
    value = idealised_FRET[column]
    #print(value)
    num_states_2(value)

state_number_df = pd.DataFrame(state_number)

print(state_number)
### generates an RMSD value for each column
RMSD_values = []


for column in difference.columns:
    column_sum = difference[column].sum()
    column_squared = column_sum ** 2
    column_RMSD = np.sqrt(column_squared/999)
    RMSD_values.append(column_RMSD)


print(RMSD_values)
mean_RMSD = np.average(RMSD_values)
mean_RMSD = str(mean_RMSD)
print('mean is: ' +str(mean_RMSD))

#trace_1_sum = difference["Trace_No_1"].sum()
#trace_1_RMSD = np.sqrt(trace_1_sum/999)
#print(trace_1_RMSD)

main_output_folder = 'C:/Users/clj713/Bailey_2/Simulated_FRET_Data/Modelling_FRET/Output/Noise_Increase_2/0.7_0.8_1x/'


mean_df = pd.DataFrame()
mean_df['A'] = mean_RMSD
#print(mean_df)
mean_df_str = mean_df.to_string(index=False)
RMSD_df = pd.DataFrame(RMSD_values)
RMSD_str = RMSD_df.to_string(index=False)
state_num_str = state_number_df.to_string(index=False)
mean_count = np.average(state_number)
mean_count_str = str(mean_count)
print('av state is: ' + mean_count_str)


#print(mean_df_str)
folder_name = "0.7_0.8_1x_Noise"
file_name =  folder_name + '.txt'


mean_folder = "mean_RMSD"
if not os.path.exists(f"{main_output_folder}{mean_folder}/"):
    os.makedirs(f"{main_output_folder}{mean_folder}/")
mean_fol = str((f"{main_output_folder}{mean_folder}/"))
with open(os.path.join(mean_fol,file_name),'w') as file1:
    file1.write(mean_RMSD)

all_RMSD_folder = "All_RMSD"
if not os.path.exists(f"{main_output_folder}{all_RMSD_folder}/"):
    os.makedirs(f"{main_output_folder}{all_RMSD_folder}/")
all_fol = str(f"{main_output_folder}{all_RMSD_folder}/")
with open(os.path.join(all_fol,file_name), 'w') as file2:
    file2.write(RMSD_str)

state_count = "state_count"
if not os.path.exists(f"{main_output_folder}{state_count}/"):
    os.makedirs(f"{main_output_folder}{state_count}/")
state_fol = str(f"{main_output_folder}{state_count}/")
with open(os.path.join(state_fol,file_name), 'w') as file3:
    file3.write(state_num_str)

mean_state_count = "mean_state_count"
if not os.path.exists(f"{main_output_folder}{mean_state_count}/"):
    os.makedirs(f"{main_output_folder}{mean_state_count}/")
mean_state_fol = str(f"{main_output_folder}{mean_state_count}/")
with open(os.path.join(mean_state_fol,file_name), 'w') as file4:
    file4.write(state_num_str)

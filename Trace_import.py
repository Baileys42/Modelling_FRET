import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import shutil
import glob as glob




data_path = ["C:/Users/clj713/Bailey_2/Simulated_FRET_Data/Trace_Output/vbFRET_output/Test_output/"]

output = "C:/Users/clj713/Bailey_2/Simulated_FRET_Data/Modelling_FRET/vbFRET_file_output/"


def get_trace_file(input_folder, output):
    for folder in input_folder:
        new_folder = folder.split("/")[-2]
        if not os.path.exists(f"{output}{new_folder}/"):
            os.makedirs(f"{output}{new_folder}/")
        tracelist = [trace for trace in os.listdir(folder) if ".dat" in trace]
        for trace in tracelist:
            shutil.copyfile(f"{folder}{trace}",f"{output}{new_folder}/{trace}")
get_trace_file(data_path, output)


def load_trace(file):
    trace_df = pd.DataFrame(np.loadtext(file))
    trace_df.columns("time", "donor", "acceptor", "FRET", "Idealised")
    return trace_df



def file_read(input_folder):
    filename = glob.glob(input_folder + "/*.dat")
    dfs = []
    for file in filename:
        dfs.append(pd.read_table(filename, sep = ''))
    df = pd.concat(dfs)
    df = pd.DataFrame(df)

compiled_df = []
new_folder = ["vbFRET_file_output"]
for folder in new_folder:
    data = file_reader(new_folder)
    compiled_df.append(data)



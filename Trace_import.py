import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import shutil




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

new_folder = ["vbFRET_file_output"]
for folder in new_folder:
    tracelist = [trace for trace in os.listdir(folder)]
    for trace in tracelist 
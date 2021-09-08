import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import shutil




data_path = 


def file_load(file):
    trace_df = pd.DataFrame(np.loadtext(file))


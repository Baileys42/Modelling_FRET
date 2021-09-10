import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

### these values are the rate constants for transitioning between different states
P = [[0.1,0.9],[0.2,0.8]]
P_name = [['12','11'],['21','22']]
state = []
### function that determines initial starting state for molecule, 
# ## at the moment this is not dependent on probability
###  --> just random chance --> need to implement proper probabilty

def start_state(state_1,state_2):
    state = np.random.randint(0,2)
    if state == 0:
        state = state_1
        return state
    else:
        state = state_2
        return state


### mean time relates to mean dwell time for each state --> inverse of rate constant
mean_time_1 = 1/(P[0][0])
mean_time_2 = 1/(P[1][1])


dwell_times_df = []
states_df = []

### function that creates list of states depending on rate constants for 
### each transition. Generates list of states and dwell time for that state

def FRET_state(state_1,state_2,T):
    t = 0
    state = start_state(state_1,state_2)
    while t < T:
        U = np.random.random()
        if state == state_1:
            dwell_time = np.random.exponential(mean_time_1,1)
            dwell_times_df.extend(dwell_time)
            states_df.append(state)
            t += dwell_time
            if U <= P[0][0]:
                state = state_1
            else:
                state = state_2
        elif state == state_2:
            dwell_time = np.random.exponential(mean_time_2,1)
            dwell_times_df.extend(dwell_time)
            states_df.append(state)
            t += dwell_time
            if U <= P[1][1]:
                state = state_2
            else:
                state = state_1



FRET_state(0.6,0.8,100)

### function for interpolating function, needs to 'integrate' state_df values --> interpolate this data
### --> np.diff to differentiate back. 

def interp_states(time_points,noise=False):
    time = np.linspace(0,100,(time_points + 1))
    time_true = np.empty(len(time)+1)
    time_true[0] = 0
    time_true[1:] = time
    sum_dwell_times = np.empty(len(dwell_times_df)+1)
    sum_dwell_times[0] = 0
    sum_dwell_times[1:] = np.cumsum(dwell_times_df)
    multiple = np.empty(len(dwell_times_df)+1)
    multiple[0] = 0
    multiple[1:] = np.cumsum(np.multiply(dwell_times_df,states_df))
    multiple_int = np.interp(time_true,sum_dwell_times,multiple)
    sample_int = (np.diff(multiple_int)) * 10
    if noise == True:
        noise = np.random.normal(0,0.05,len(sample_int))
        noisy_signal = sample_int + noise
        return noisy_signal
    else:
        return sample_int

### My initial function for interpolating the state transitions
def interp_states2(time_points,noise):
    time = np.linspace(0,100,(time_points + 1))
    sum_dwell_times = np.cumsum(dwell_times_df)
    multiple_int = np.interp(time,sum_dwell_times,states_df)
    if noise == True:
        noise = np.random.normal(0,0.05,len(multiple_int))
        noisy_signal = multiple_int + noise
        return noisy_signal
    else:
        return multiple_int



### functions that prints figure, takes x and y variables as inputs
def show_figure(time_x,treatment_y):
    plot1 = plt.figure(figsize=(5,2))
    sns.set(style = "darkgrid")
    sns.lineplot(x = time_x, y = treatment_y, color = "darkorange")
    plt.ylabel("FRET")
    plt.xlabel("Time (s)")
    plt.ylim(0,1,0.20)
    plt.xlim(0,100,20)

### function for plotting donor + acceptor time traces 
def show_figure_AD(time_x,treatment_y_1,treatment_y_2):
    plot1 = plt.figure(figsize=(5,2))
    sns.set(style = "darkgrid")
    sns.lineplot(x = time_x, y = treatment_y_1, color = "forestgreen",label = "Donor")
    sns.lineplot(x = time_x, y = treatment_y_2, color = "firebrick", label = "Acceptor")
    plt.ylabel("Intensity")
    plt.xlabel("Time (s)")
    plt.ylim(0,100,20)
    plt.xlim(0,100,20)




state_values = interp_states(1000, noise = False)
noise_state_values = interp_states(1000,noise = True)
time = np.linspace(0,100,(len(state_values)))


show_figure(time,state_values)
show_figure(time,noise_state_values)

acc_signal = []
don_signal = []



### generates dye traces with noise as function of mean_photon_count * 0.2

# def dye_trace(intensity,dye):
#     ### donor trace + noise
#     if dye == "donor":
#         for state in state_values:
#             donor = (1-state) * intensity
#             don_signal.append(donor)
#         mean_photon_count_don = np.mean(don_signal)
#         noise_don = np.random.normal(0,(mean_photon_count_don*0.2),len(don_signal))
#         noisy_don = don_signal + noise_don
#         return noisy_don
#     elif dye == "acceptor":
#     ### acceptor trace + noise
#         for state in state_values:
#             acceptor = state * intensity
#             acc_signal.append(acceptor)
#         mean_photon_count_acc = np.mean(acc_signal)
#         noise_acc = np.random.normal(0,(mean_photon_count_acc*0.2),len(acc_signal))
#         noisy_acc = acc_signal + noise_acc
#         return noisy_acc



### Generates dye traces with noise added as function of sqrt(intensity)

# def dye_trace(intensity,dye):
#     ### donor trace + noise
#     if dye == "donor":
#         for state in state_values:
#             donor = (1-state) * intensity
#             don_signal.append(donor)
#         mean_photon_count_don = np.mean(don_signal)
#         noise_don = np.random.normal(0,(np.sqrt(intensity)),len(don_signal))
#         noisy_don = don_signal + noise_don
#         return noisy_don
#     elif dye == "acceptor":
#     ### acceptor trace + noise
#         for state in state_values:
#             acceptor = state * intensity
#             acc_signal.append(acceptor)
#         mean_photon_count_acc = np.mean(acc_signal)
#         noise_acc = np.random.normal(0,(np.sqrt(intensity)),len(acc_signal))
#         noisy_acc = acc_signal + noise_acc
#         return noisy_acc
current_don_noise = []
current_acc_noise = []

def dye_trace(intensity,dye):
    ### donor trace + noise
    if dye == "donor":
        for state in state_values:
            donor = (1-state) * intensity
            don_signal.append(donor)
            current_d_noise = np.random.normal(0,(np.sqrt(donor)*4),1)
            current_don_noise.append(current_d_noise)
    elif dye == "acceptor":
    ### acceptor trace + noise
        for state in state_values:
            acceptor = state * intensity
            acc_signal.append(acceptor)
            current_a_noise = np.random.normal(0,(np.sqrt(acceptor)*4),1)
            current_acc_noise.append(current_a_noise)





dye_trace(100,dye = "donor")
dye_trace(100, dye = "acceptor")

current_don_noise = np.concatenate(current_don_noise)
current_acc_noise = np.concatenate(current_acc_noise)

noise_don = don_signal + current_don_noise
noise_acc = acc_signal + current_acc_noise


# show_figure_AD(time,don_signal,acc_signal)
show_figure_AD(time,noise_don,noise_acc)

def FRET_E(donor, acceptor):
    Eff = (acceptor)/(acceptor + donor)
    return Eff

Eff = FRET_E(noise_don, noise_acc)



# show_figure(time, state_values)
# show_figure(time,noise_state_values)
show_figure(time,Eff)

# DAT = np.column_stack((noisy_donor,noisy_acceptor))

# dye_df = pd.DataFrame(DAT)
# # dye_df.columns = ["Donor", "Acceptor"]
# print(dye_df)
# dye_df_string = dye_df.to_string(index = False,header=False)


# name = "Intensity.txt"
# with open(os.path.join('/Users/baileyskewes/Documents/Python_Projects/Modelling_FRET/Trace_output',name),'w') as file1:
#     file1.write(dye_df_string)



# N = 5
# mol = range(N)
# for data in mol:
#     name = "molecule_No_" + str(data) + ".txt"
#     dwell_times_df = []
#     states_df = []
#     FRET_state(0.2,0.8,100)
#     state_values = interp_states(1000, noise = False)
#     acc_signal = []
#     don_signal = []
#     current_don_noise = []
#     current_acc_noise = []
#     dye_trace(100,dye = "donor")
#     dye_trace(100,dye = "acceptor")
#     current_don_noise = np.concatenate(current_don_noise)
#     current_acc_noise = np.concatenate(current_acc_noise)
#     noisy_donor = don_signal + current_don_noise
#     noisy_acceptor = acc_signal + current_acc_noise
#     DAT = np.column_stack((noisy_donor,noisy_acceptor))
#     dye_df = pd.DataFrame(DAT)
#     dye_df_string = dye_df.to_string(index = False,header = False)
#     with open(os.path.join("/Users/baileyskewes/Documents/Python_Projects/Modelling_FRET/Trace_output",name),'w') as file1:
#         file1.write(dye_df_string)



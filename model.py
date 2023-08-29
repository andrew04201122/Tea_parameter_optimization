import random
import os
import time
import pandas as pd
import glob
from smt_test import Surrogate_model
from sklearn.metrics import accuracy_score,r2_score
from smt.sampling_methods import LHS, Random
from smt.applications.mixed_integer import(
    FLOAT,
    ORD,
    ENUM,
    MixedIntegerSamplingMethod,
    MixedIntegerSurrogateModel,
    GOWER,
    MixedIntegerContext,
)
import csv
import argparse

# PATH = "C:/Users/USER/Desktop/Code/Full_Flow"
# DATA_PATH = f'{PATH}/data_for_vedio.txt'
BOX_MINIMUM = 300
BOX_MAXIMUM  = 500
# ANGLES = [0, 90]
# POSITIONS = ["up", "front", "back", "left", "right"]
#POSITIONS = ["0", "1", "2", "3", "4"]

# TODO: surrogate or RL
def initial_LHS_model():
    # randomly generate parameter

    # Box_X, Box_Y, Box_Z, Waveport1_angle, Waveport1_position, Waveport2_angle, Waveport2_position, Waveport1_x, Waveport1_y, Waveport2_x, Waveport2_y, frequency, Waveport1_phase, Waveport2_phase
    xtypes = [FLOAT, FLOAT, FLOAT, ORD, ORD, ORD, ORD, FLOAT, FLOAT, FLOAT, FLOAT, ORD, FLOAT, FLOAT]
    xlimits = [[BOX_MINIMUM, BOX_MAXIMUM], [BOX_MINIMUM, BOX_MAXIMUM], [BOX_MINIMUM, BOX_MAXIMUM], ["0", "90"], ["0"], ["0", "90"], ["2"], [-100, 100], [-100, 100], [-100, 100], [-100, 100], ["2", "2.45", "3"], [0, 360], [0, 360]]
    mixint = MixedIntegerContext(xtypes, xlimits)
    sampling_method = mixint.build_sampling_method(Random)
    sampling_value = sampling_method(1)[0]
    print(sampling_value)
    return sampling_value


if __name__ ==  "__main__":
    parser = argparse.ArgumentParser(description='hello!')
    parser.add_argument('-p','--path',help='The path to the file',default='C:/Users/USER/Desktop/Code/Full_Flow')
    parser.add_argument('-d','--data',help='data name',default='data_for_vedio')

    args = parser.parse_args()
    PATH = args.path
    data_name = args.data
    DATA_PATH = f'{PATH}/{data_name}.txt'

    # delete data
    file_patterns = ["input*.txt", "output*.fld"]
    delete_files = []
    for pattern in file_patterns:
        delete_files += glob.glob(os.path.join(f'{PATH}/Data', pattern))
    for f in delete_files:
        os.remove(f)
    try:
        os.remove(f'{PATH}/surrogate_result.csv')
    except:
        None

    # record length
    datamax_initial_len = 0
    with open(DATA_PATH, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        datamax_initial_len = len(list(reader))
    input_number = 0
    output_number = 0
    # TODO: R2 score rewrite
    for i in range(10000):
        # predict
        # parameters = initial_LHS_model()
        model = Surrogate_model()
        model.build(DATA_PATH)
        parameters = model.find_max(i)

        # export input
        with open(f'{PATH}/Data/input{input_number}.txt', 'w') as f:
            for parameter in parameters[0][:-1]:
                f.write(str(parameter) + " ")
        input_number += 1
        if len(parameters) == 2:
            with open(f'{PATH}/Data/input{input_number}.txt', 'w') as f:
                for parameter in parameters[1][:-1]:
                    f.write(str(parameter) + " ")
            input_number += 1
            
        ############### Ansys executing ###############

        # Waiting for output
        for num in range(len(parameters)):
            path = f"{PATH}/Data/output{output_number}.fld"
            print(f"Waiting for output{output_number}")
            while not os.path.exists(path):
                time.sleep(1)

            time.sleep(5) # without delay the file may create fail and cause error

            # analyze data
            data = pd.read_csv(path, sep='\s+', header=None, skiprows=2)
            data.columns = ["X", "Y", "Z", "Mag_E"]
            max_value = data["Mag_E"].mean()

            # print("max: ", max_value)

            # export output
            with open(DATA_PATH, 'a') as f:
                for parameter in parameters[num][:-1]:
                    f.write(str(parameter) + " ")
                f.write(str(max_value) + "\n")

            # show training result
            actual_data = []
            with open(DATA_PATH,'r') as f:
                lines = f.readlines()
                for line in lines:
                    ans = line.split(' ')
                    actual_data.append(float(ans[-1][:-1]))
            max_val = max(actual_data)
            max_index = [i for i, x in enumerate(actual_data) if x == max_val]
            print(f"actual data: {actual_data[-1]} predict_data: {parameters[num][-1]}")
            #print(f"R2 score : {r2_score(actual_data[datamax_initial_len:], predict_data)}")
            print(f"current max value: {max_val} index: {max_index}")
            print("------------------------------")

            output_number += 1  
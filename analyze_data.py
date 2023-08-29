import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data_0530.txt', sep=' ', header=None)
data.columns = ["box_x", "box_y", "box_z", "angle1", "position1" ,"angle2", "position2", "waveport1_x", "waveport1_y", "waveport2_x", "waveport2_y", "HZ", "phase1", "phase2", "max"]

data2 = pd.read_csv('data_RND_average.txt', sep=' ', header=None)
data2.columns = ["box_x", "box_y", "box_z", "angle1", "position1" ,"angle2", "position2", "waveport1_x", "waveport1_y", "waveport2_x", "waveport2_y", "max"]


max_values = data["max"].values
current_max_value = max_values[0]
max_index = -1
real_data = max_values[200:]
for i in range(len(real_data)):
    if real_data[i] > 70000:
        print(f"index>70000: {i}")
    if real_data[i] > current_max_value:
        current_max_value = real_data[i]
        max_index = i
    else:
        real_data[i] = current_max_value


max_values2 = data2["max"].values
current_max_value2 = max_values[0]
max_index2 = -1
real_data2 = max_values2[50:]
for i in range(len(real_data2)):
    # if real_data2[i] > 70000:
    #     print(f"index2>70000: {i}")
    if real_data2[i] > current_max_value2:
        current_max_value2 = real_data2[i]
        max_index2 = i
    else:
        real_data2[i] = current_max_value2

print(f"current_max_value2: {current_max_value2}")
# for i in range(len(max_values)):
#     if max_values[i] > current_max_value:
#         current_max_value = max_values[i]
#         max_index = i
#     else:
#         max_values[i] = current_max_value
# plt.plot(max_values)


plt.plot(real_data,'r-',label = 'new model')
plt.plot(real_data2,'b-', label = 'old model')
plt.xlabel("number of data")
plt.ylabel("current_max_value")
# print(f"current max value : {current_max_value}")
# print(f"Max index : {max_index}")


plt.legend()
plt.savefig("./max_value.png")
plt.show()



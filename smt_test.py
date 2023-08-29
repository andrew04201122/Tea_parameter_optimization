import smt
import numpy as np
from smt.applications.mixed_integer import(
    FLOAT,
    ORD,
    ENUM,
    MixedIntegerSamplingMethod,
    MixedIntegerSurrogateModel,
    GOWER,
    MixedIntegerContext,
)
from smt.sampling_methods import LHS, Random, FullFactorial
from smt.surrogate_models import LS, QP, KPLS, KRG, KPLSK, GEKPLS, MGP
import matplotlib.pyplot as plt
import random
import csv
import pickle
from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process import GaussianProcessRegressor
from RBF_discrete import SequenceKernel

from sklearn.svm import SVR


class Surrogate_model():
    def __init__(self):
        self.direction_dict = {'up': '0', 'front' : '1', 'back': '2', 'left' : '3', 'right' : '4'}
        self.inverse_direction_dict = {0 : 'up', 1: 'front', 2 : 'back', 3 : 'left', 4 : 'right'}
        self.ANGLES = [0, 90]
        self.POSITIONS = [0, 1, 2, 3, 4]
        self.FREQUENCY = ["2.0", "2.45", "3.0"]
        self.number_of_parameter = 14
        self.SAMPLING_SIZE = 800
        self.BOX_MINIMUM = 300
        self.BOX_MAXIMUM  = 500
        self.sampling_num = 30
        self.xtypes = [FLOAT, FLOAT, FLOAT, ORD, ORD, ORD, ORD, FLOAT, FLOAT, FLOAT, FLOAT, ORD, FLOAT, FLOAT]
        self.xlimits = [[self.BOX_MINIMUM, self.BOX_MAXIMUM], [self.BOX_MINIMUM, self.BOX_MAXIMUM], [self.BOX_MINIMUM, self.BOX_MAXIMUM], ["0", "90"], ["0"], ["0", "90"], ["2"], [-100, 100], [-100, 100], [-100, 100], [-100, 100], ["2", "2.45", "3"], [0, 360], [0, 360]]
        self.mixint = MixedIntegerContext(self.xtypes, self.xlimits)
        self.train_x = []
        self.train_y = []
        self.sorted_index_list = []

    def sort_list_index(self):
        origin_list = []
        sorted_list_index = []
        for i in range(len(self.train_y)):
            origin_list.append((self.train_y[i],i))
        sort_list = sorted(origin_list, key = lambda x : x[0],reverse= True)
        for i in range(len(self.train_y)):
            sorted_list_index.append(sort_list[i][1])
        self.sorted_index_list = sorted_list_index

    def build(self, data_path):
        with open(data_path, 'r') as f:
            for line in f.readlines():
                s = line.split(' ')
                s[0] = float(s[0])
                s[1] = float(s[1])
                s[2] = float(s[2])
                # lock front and back plane
                s[4] = '0'
                s[6] = '2'
                s[7] = float(s[7])
                s[8] = float(s[8])
                s[9] = float(s[9])
                s[10] = float(s[10])
                # s[11] = float(s[11])
                s[12] = float(s[12])
                s[13] = float(s[13])   
                self.train_x.append(s[:-1])
                self.train_y.append(int(float(s[-1][:-1])))
        self.train_x = np.array(self.train_x)
        self.train_y = np.array(self.train_y)
        self.sort_list_index()
        # traing model
        self.Mymodel = self.mixint.build_surrogate_model(KRG(print_global=False))
        self.Mymodel.set_training_values(self.train_x, self.train_y)
        self.Mymodel.train()
        with open('surrogate_model.pkl','wb') as f:
            pickle.dump(self.Mymodel, f)

        #self.secondModel = self.mixint.build_surrogate_model(MGP(print_global=False))
        self.secondModel = self.mixint.build_surrogate_model(KPLS(print_global=False))
        self.secondModel.set_training_values(self.train_x, self.train_y)
        self.secondModel.train()
        # build sklearn rbf
        # kernel = SequenceKernel()
        # self.MyRBF = SVR(kernel='rbf')
        # self.MyRBF.fit(self.train_x, self.train_y)

    def global_sampling(self):
        sampling_method = self.mixint.build_sampling_method(Random)
        sampling_value = sampling_method(self.sampling_num)
        # print(f"sampling_value: {sampling_value}")
        return sampling_value

    def medium_sampling(self):
        medium_xtypes = [FLOAT, FLOAT, FLOAT, ORD, ORD, ORD, ORD, FLOAT, FLOAT, FLOAT, FLOAT, ORD, FLOAT, FLOAT]
        medium_xlimits = [[float('inf'), float('-inf')], [float('inf'), float('-inf')], [float('inf'), float('-inf')], ["0", "90"], ["0"], ["0", "90"], ["2"], [float('inf'), float('-inf')], [float('inf'), float('-inf')], [float('inf'), float('-inf')], [float('inf'), float('-inf')], ["2", "2.45", "3"], [float('inf'), float('-inf')], [float('inf'), float('-inf')]]
        top_indices = self.sorted_index_list[:10]
        for top_index in top_indices:
            for i in range(14):
                if i in [0, 1, 2, 7, 8, 9, 10, 12, 13]:
                    if float(self.train_x[top_index][i]) < medium_xlimits[i][0]:
                        medium_xlimits[i][0] = float(self.train_x[top_index][i])
                    if float(self.train_x[top_index][i]) > medium_xlimits[i][1]:
                        medium_xlimits[i][1] = float(self.train_x[top_index][i])
        # print(f"ranges: {medium_xlimits}")
        medium_mixint = MixedIntegerContext(medium_xtypes, medium_xlimits)
        sampling_method = medium_mixint.build_sampling_method(Random)
        sampling_value = sampling_method(self.sampling_num)
        # print(f"sampling_value: {str(sampling_value)}")
        return sampling_value

    def local_sampling(self):
        top_indices = self.sorted_index_list[:5]
        candidate_sampling = []
        # print(f"train_x top 1: {str(self.train_x[top_indices])}")
        for top_index in top_indices:
            
            k = int(self.sampling_num/5)
            for j in range(k):
                sampling = [0] * 14
                # XYZ
                for i in range(3):
                    sampling[i] = float(self.train_x[top_index][i]) + random.uniform(-0.5, 0.5)

                rand_prob3 = random.random()
                if rand_prob3 < 0.1:
                    sampling[3] = random.choice(self.ANGLES)
                else:
                    sampling[3] = self.train_x[top_index][3]

                rand_prob5 = random.random()
                if rand_prob5 < 0.1:
                    sampling[5] = random.choice(self.ANGLES)
                else:
                    sampling[5] = self.train_x[top_index][5]

                # WaveportXY
                for i in range(4):
                    sampling[i+7] = float(self.train_x[top_index][i+7]) + random.uniform(-0.5, 0.5)
                
                rand_prob11 = random.random()
                if rand_prob11 < 0.1:
                    sampling[11] = random.choice(self.FREQUENCY)
                else:
                    sampling[11] = self.train_x[top_index][11]

                # phase
                for i in range(2):
                    sampling[i+12] = float(self.train_x[top_index][i+12]) + random.uniform(-10, 10)

                candidate_sampling.append(sampling)
        return candidate_sampling

    # TODO: infill criteria
    def sampling(self, iteration):
        if iteration < 80:
            self.sampling_num = 30
        elif iteration >= 80 and iteration < 160:
            self.sampling_num = 20
        else:
            self.sampling_num = 10
        if iteration % 5 == 1:
            candidate_sampling = self.global_sampling()
        elif iteration % 5 ==  3:
            candidate_sampling = self.medium_sampling()
        elif iteration % 5 == 0 or iteration % 5 == 2 or iteration % 5 == 4:
            candidate_sampling = self.local_sampling()
        candidate_sampling = self.local_sampling()
        return candidate_sampling

    #TODO : choose point into Ansys
    def find_max(self, iteration):
        test_x = np.array(self.sampling(iteration))
        test_y = self.Mymodel.predict_values(test_x)
        second_test_y = self.secondModel.predict_values(test_x)
        # print(f"test X : {test_x}")
        # test_RBF_y = self.MyRBF.predict(test_x)
        # print(f"test_RBF_Y {test_RBF_y}")

        max_val = 0
        max_index = -1
        second_model_max_val = 0
        second_model_max_index = -1
        for i in range(len(test_y)):
            if test_y[i] > max_val:
                max_val = test_y[i]
                max_index = i
                
        for i in range(len(second_test_y)):
            if second_test_y[i] > second_model_max_val:
                second_model_max_val = second_test_y[i]
                second_model_max_index = i
                

        if max_index == second_model_max_index :
            tmp = test_x[max_index].tolist()
            tmp.append(float(max_val))
            return [tmp]
        else :
            newPoint1 = test_x[max_index].tolist()
            newPoint1.append(float(max_val))

            newPoint2 = test_x[second_model_max_index].tolist()
            newPoint2.append(float(second_model_max_val))
            return [newPoint1,newPoint2]
        
        
        
    
    def predict(self, test_x):
        test_y = self.Mymodel.predict_values(test_x)
        return test_y

    def export_result(self, logger):
        with open('C:/Users/USER/Desktop/Code/Full_Flow/surrogate_result.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile,delimiter=',')
            writer.writerow(logger)


if __name__ == '__main__':
    data_path = "./Full_Flow/data_0530.txt"
    model = Surrogate_model()
    model.build(data_path)
    parameters = model.find_max(1)

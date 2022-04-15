import joblib

from Kitsune import Kitsune
import numpy as np
from numpy import pad
import time
from tensorflow import keras
from tensorflow.keras.models import load_model
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout, Activation
from tensorflow.keras.layers import Conv1D, MaxPooling1D
from tensorflow.python.keras.layers import BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.layers import LSTM

# ############################################################################# Kitsune a lightweight online network
# intrusion detection system based on an ensemble of autoencoders (kitNET). For more information and citation,
# please see our NDSS'18 paper: Kitsune: An Ensemble of Autoencoders for Online Network Intrusion Detection

# This script demonstrates Kitsune's ability to incrementally learn, and detect anomalies in recorded a pcap of the
# Mirai Malware. The demo involves an m-by-n dataset with n=115 dimensions (features), and m=100,000 observations.
# Each observation is a snapshot of the network's state in terms of incremental damped statistics (see the NDSS paper
# for more details)

# The runtimes presented in the paper, are based on the C++ implimentation (roughly 100x faster than the python implimentation)
###################  Last Tested with Anaconda 3.6.3   #######################

# Load Mirai pcap (a recording of the Mirai botnet malware being activated)
# The first 70,000 observations are clean...
# print("Unzipping Sample Capture...")
# import zipfile
# with zipfile.ZipFile("mirai.zip","r") as zip_ref:
#     zip_ref.extractall()


def getRes(filepath):
    # File location
    path = filepath  # the pcap, pcapng, or tsv file to process.

    packet_limit = np.Inf  # the number of packets to process
    # KitNET params:
    maxAE = 10  # maximum size for any autoencoder in the ensemble layer

    # 学习特i征映射(集合的体系结构)所需的实例数量
    FMgrace = 10  # the number of nstances taken to learn the feature mapping (the ensemble's architecture)

    # 用于训练异常检测器(集合本身)的实例数
    ADgrace = 50000  # the number of instances used to train the anomaly detector (ensemble itself)

    # Build Kitsune
    K = Kitsune(path, packet_limit, maxAE, FMgrace, ADgrace)

    print("Running Kitsune:")
    RMSEs = []
    i = 0
    start = time.time()
    a_np = np.empty(0)
    # Here we process (train/execute) each individual packet.
    # In this way, each observation is discarded after performing process() method.
    while True:
        i += 1
        if i % 1000 == 0:
            print(i)
        rmse = K.proc_next_packet()
        if rmse == -1:
            a_np = K.__dict__['a_np']
            break
        RMSEs.append(rmse)
        # if i > 20000:
        #     #
        #     # print(len(a_np))

        #     break
    stop = time.time()

    felen = K.__dict__['felen']
    a_np = a_np.reshape(int(len(a_np) / felen), felen)
    print("felen",felen)

    if(felen > 23):
        delete_index = []
        for i in range(23,felen):
            delete_index.append(i)
        print(delete_index)
        print("1",len(a_np[0]))
        a_np = np.delete(a_np, delete_index, axis=1)
        print("2",len(a_np[0]))
    else:
        a_np = np.array(a_np)
        a_np = pad(a_np, (0, 23-felen), 'constant')
    a_np = preprocessing.normalize(a_np, norm='l1')

    sc = StandardScaler()
    a_np = sc.fit_transform(a_np)

    file_bys = "E:\\AllProjects\\DaChuang\\Rear_end\\bys_all.pkl"
    bys_model = joblib.load(file_bys)
    bys_res = bys_model.predict_proba(a_np)

    file_lgbm = "E:\\AllProjects\\DaChuang\\Rear_end\\lgbm_model.pkl"
    lgbm_model = joblib.load(file_lgbm)
    lgbm_res = lgbm_model.predict_proba(a_np)

    file_lsvr = "E:\\AllProjects\\DaChuang\\Rear_end\\lsvr_all.pkl"
    lsvr_model = joblib.load(file_lsvr)
    lsvr_res = lsvr_model.decision_function(a_np)

    file_knn = "E:\\AllProjects\\DaChuang\\Rear_end\\lsvr_all.pkl"
    knn_model = joblib.load(file_knn)
    knn_res = lsvr_model.decision_function(a_np)

    b_np = a_np[:, :, np.newaxis]


    cnn = tf.keras.models.load_model("E:\\AllProjects\\DaChuang\\Rear_end\\cnn")
    cnn_res = cnn.predict(b_np)

    # lstm = tf.keras.models.load_model("E:\\AllProjects\\DaChuang\\Rear_end\\lstm_all")
    # lstm_res = lstm.predict(b_np)


    weight1 = 0.0
    weight2 = 0.0
    weight3 = 0.0
    weight4 = 0.0
    weight5 = 0.5
    weight6 = 0.5

    score = weight1 * lsvr_res + weight3 * lgbm_res + \
            weight4 * bys_res + \
            weight2 * knn_res + \
            cnn_res
    # weight6 * lstm_res



    maxindex = []
    for i in range(0, len(score)):
        # maxindex.append(np.argmax(y_score[i]))
        if np.argmax(score[i]) == 0:
            maxindex.append(0)
        elif np.argmax(score[i]) == 1:
            maxindex.append(1)
        elif np.argmax(score[i]) == 2:
            maxindex.append(2)
        elif np.argmax(score[i]) == 3:
            maxindex.append(3)
        elif np.argmax(score[i]) == 4:
            maxindex.append(4)
        elif np.argmax(score[i]) == 5:
            maxindex.append(5)
        elif np.argmax(score[i]) == 6:
            maxindex.append(6)
        elif np.argmax(score[i]) == 7:
            maxindex.append(7)
        elif np.argmax(score[i]) == 8:
            maxindex.append(8)
        elif np.argmax(score[i]) == 9:
            maxindex.append(9)
    # print(maxindex)
    return maxindex


# df = pd.read_csv('datas/Thursday-WorkingHours.csv', error_bad_lines = False)

# x = df.iloc[5001:15000, 1]
# x = x.values


# b_np = K.AnomDetector.a_np.reshape(i - 5000 - 1, 16)

# y = np.column_stack((a_np, x))
# pd_data = pd.DataFrame(a_np)


# #
# pd_data.to_csv('output/SSL_Renegotiation_pcap.csv', header=0, index=0)
# print("Complete. Time elapsed: " + str(stop - start))

# df = pd.read_csv('data_2.csv', header = None)
# d = df.drop([0])
# d = df.drop([0],axis=1)

# d.to_csv('data.csv')

# Here we demonstrate how one can fit the RMSE scores to a log-normal distribution (useful for finding/setting a
# cutoff threshold \phi) 这里我们演示了如何将RMSE分数拟合到对数正态分布(对于寻找/设置截止阈值很有用)
# from scipy.stats import norm
#
# benignSample = np.log(RMSEs[FMgrace + ADgrace + 1:100000])
# logProbs = norm.logsf(np.log(RMSEs), np.mean(benignSample), np.std(benignSample))
#
# # plot the RMSE anomaly scores
# # 绘制RMSE异常分数(画图)
# print("Plotting results")
# from matplotlib import pyplot as plt
# from matplotlib import cm
#
# plt.figure(figsize=(10, 5))
# fig = plt.scatter(range(FMgrace + ADgrace + 1, len(RMSEs)), RMSEs[FMgrace + ADgrace + 1:], s=0.1,
#                   c=logProbs[FMgrace + ADgrace + 1:], cmap='RdYlGn')
# plt.yscale("log")
# plt.title("Anomaly Scores from Kitsune's Execution Phase")
# plt.ylabel("RMSE (log scaled)")
# plt.xlabel("Time elapsed [min]")
# figbar = plt.colorbar()
# figbar.ax.set_ylabel('Log Probability\n ', rotation=270)
# plt.show()

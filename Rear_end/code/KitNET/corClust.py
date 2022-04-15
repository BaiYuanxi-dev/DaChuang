import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster, to_tree

# A helper class for KitNET which performs a correlation-based incremental clustering of the dimensions in X
# n: the number of dimensions in the dataset
# For more information and citation, please see our NDSS'18 paper: Kitsune: An Ensemble of Autoencoders for Online Network Intrusion Detection
#KitNET的一个助手类，对X中的维度进行基于相关性的增量聚类
# n:数据集中的维数
class corClust:
    def __init__(self,n):
        #parameter:
        self.n = n
        #varaibles
        self.c = np.zeros(n) #linear num of features线性特征数
        self.c_r = np.zeros(n) #linear sum of feature residules特征残差的线性和
        self.c_rs = np.zeros(n) #linear sum of feature residules特征残差的线性和
        self.C = np.zeros((n,n)) #partial correlation matrix部分相关矩阵
        self.N = 0 #number of updates performed执行的更新次数

    # x: a numpy vector of length n
    def update(self,x):
        self.N += 1
        self.c += x
        c_rt = x - self.c/self.N
        self.c_r += c_rt
        self.c_rs += c_rt**2
        self.C += np.outer(c_rt,c_rt)

    # creates the current correlation distance matrix between the features
    #创建要素之间的当前相关距离矩阵
    def corrDist(self):
        c_rs_sqrt = np.sqrt(self.c_rs)
        C_rs_sqrt = np.outer(c_rs_sqrt,c_rs_sqrt)
        C_rs_sqrt[C_rs_sqrt==0] = 1e-100 #this protects against dive by zero erros (occurs when a feature is a constant)
        D = 1-self.C/C_rs_sqrt #the correlation distance matrix
        D[D<0] = 0 #small negatives may appear due to the incremental fashion in which we update the mean. Therefore, we 'fix' them
        return D

    # clusters the features together, having no more than maxClust features per cluster
    #将特征聚集在一起，每个簇不超过最大簇特征
    def cluster(self,maxClust):
        D = self.corrDist()
        Z = linkage(D[np.triu_indices(self.n, 1)])  # create a linkage matrix based on the distance matrix
        if maxClust < 1:
            maxClust = 1
        if maxClust > self.n:
            maxClust = self.n
        map = self.__breakClust__(to_tree(Z),maxClust)
        return map

    # a recursive helper function which breaks down the dendrogram branches until all clusters have no more than maxClust elements
    def __breakClust__(self,dendro,maxClust):
        if dendro.count <= maxClust: #base case: we found a minimal cluster, so mark it
            return [dendro.pre_order()] #return the origional ids of the features in this cluster
        return self.__breakClust__(dendro.get_left(),maxClust) + self.__breakClust__(dendro.get_right(),maxClust)

# Copyright (c) 2017 Yisroel Mirsky
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
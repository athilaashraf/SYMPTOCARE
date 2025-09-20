import math
from tkinter import Tk, Label, Entry



import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import style
# import pandas as pd
import random
from collections import Counter
# from sklearn import preprocessing
import time
import pymysql
#for plotting
# from src.featureextract import glcm_feat


class CKNN:

    def __init__(self,id):
        self.accurate_predictions = 0
        self.total_predictions = 0
        self.accuracy = 0.0
        self.id=id
        ##########

        lines=[]

        # training_data1 = np.loadtxt("static/creditcard.csv", dtype=str, delimiter=",")
        #
        # training_data=[]
        # for i in range(1,len(training_data1)):
        #     training_data.append(training_data1[i][0:30])
        #     lines.append(training_data1[i][30])
        con = pymysql.connect(host="localhost", port=3306, user="root", password="123456789", db="symptocare")
        cmd = con.cursor()
        cmd.execute("SELECT DISTINCT `symptom` FROM `myapp_symptom_table`  WHERE `DISEASE_id` IN("+id+") order by symptom")
        s = cmd.fetchall()
        dsym = []
        for i in s:
            dsym.append(i[0])
        cmd.execute("select * from myapp_disease_table where id in ("+id+")")
        s = cmd.fetchall()
        dataset = []
        ansset = []
        disdis=[]
        for i in s:
            cmd.execute("select distinct symptom from myapp_symptom_table  where DISEASE_id=" + str(i[0]))
            ss = cmd.fetchall()
            myrow = []
            for ii in ss:
                myrow.append(ii[0])
            ansset.append(int(i[0]))
            row = []
            for w in dsym:
                if w in myrow:
                    row.append(1)
                else:
                    row.append(0)
            dataset.append(row)
            disdis.append(str(i[0]))
        self.training_set= { }
        for i in disdis:
            self.training_set[i]=[]

        #Split data into training and test for cross validation
        #training_data = lbls[: len(lbls)]
        test_data = []#[-int(test_size * len(dataset)):]

        #Insert data into the training set
        cnt=0

        for record in dataset:
            st=str(ansset[cnt])
            cnt+=1


            self.training_set[st].append( record[:])

    #########

    def predict(self,  to_predict, k = 1):
        # print(to_predict,training_data['6'][0])
        # if len(training_data) >= k:
        #     print("K cannot be smaller than the total voting groups(ie. number of training data points)")
        #     return

        distributions = []
        for group in self.training_set:
            i=0
            # print(group,'group')
            for features in self.training_set[group]:

                euclidean_distance = np.linalg.norm(np.array(features)- np.array(to_predict))

                distributions.append([euclidean_distance, group])

        # print(distributions)
        results = [i[1] for i in sorted(distributions)[:k]]
        result = Counter(results).most_common(1)[0][0]
        # print("rs",results,self.training_set.keys())
        confidence = Counter(results).most_common(1)[0][1]/k

        return result, confidence



def prep(filename,d):
    feat=filename
    knn = CKNN(d)
    res=knn.predict(feat)
    return res[0]





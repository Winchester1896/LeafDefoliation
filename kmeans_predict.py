# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 13:01:16 2020

@author: zhang.9325
"""

import pickle
import argparse
import cv2
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



ap = argparse.ArgumentParser()
ap.add_argument("-m", type=str, required=True,
                help="kmeans model file")
ap.add_argument("-f", type=str, required=True,
                help="folder containing test images")
ap.add_argument("-o", type=str, required=True,
                help="output txt file containing prediction results")
args = vars(ap.parse_args())


def LeafSegmentation(path, lowThreshold, ratio, kernel_size):
    folder = os.listdir(path)
    mean_garea = 0
    mean_gedge = 0
    ae_data = []
    for z in range(len(folder)):
        ae = []
        print('-----', folder[z], '-----')
        
        testimg = cv2.imread(path + folder[z])
        
        fimg = np.array(testimg, dtype=np.float32) / 255.0
        (b0, g0, r0) = cv2.split(fimg)
        gray = 2 * g0 - r0 - b0
        
        gray_h = np.rint(gray * 255)
        (minv, maxv, minl, maxl) = cv2.minMaxLoc(gray_h)
        gray_h1d = gray_h.flatten()
        plt.figure(figsize=(40, 40))
        sns_fig = sns.displot(gray_h1d)
        plt.close()
        
        (h0, w0, c0) = np.shape(testimg)
        bimg = np.zeros((h0, w0), dtype=np.uint8)
        garea = 0
        for hi in range(h0):
            for wi in range(w0):
                if gray_h[hi][wi] > 50:
                    bimg[hi][wi] = 255
                    garea += 1
        mean_garea += garea
        
        (b1, g1, r1) = cv2.split(testimg)
        cimg = cv2.merge([b1 & bimg, g1 & bimg, r1 & bimg])
        
        img = cv2.imread(path + folder[z])
        cnt, hie = cv2.findContours(bimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt_img = cv2.drawContours(img, cnt, -1, (0, 255, 0), 3)
        
        detected_edges = cv2.cvtColor(cimg, cv2.COLOR_BGR2GRAY)
        detected_edges = cv2.Canny(detected_edges,lowThreshold,lowThreshold*ratio,apertureSize = kernel_size)
        
        (h0, w0) = np.shape(detected_edges)
        gedge = 0
        for i in range(h0):
            for j in range(w0):
                if detected_edges[i][j] != 0:
                    gedge += 1
        print('Green area: ', garea)
        print('Edges: ', gedge)
        print('Green area / edges: %.2f' % (garea / gedge))
        ratio = round((garea/gedge), 3)
        ae.append(ratio)
        ae_data.append(ae)
        mean_gedge += gedge
    defo = float(mean_garea / mean_gedge)
    print('Defoliation rate: %.2f' % defo)
    return folder, ae_data



path = args['f'] + '/'
folder, ae_data = LeafSegmentation(path, 50, 3, 3)
ae_data = np.array(ae_data)
with open(args['m'], 'rb') as m:
    kmeans = pickle.load(m)

    with open('predictions.txt', 'a+') as f:
        for i in range(len(folder)):
            ae = ae_data[i].reshape(-1, 1)
            pred = kmeans.predict(ae)
            f.write(folder[i]+ ',' + str(ae_data[i]) + ',' + str(pred) + '\n')
    f.close()
m.close()
























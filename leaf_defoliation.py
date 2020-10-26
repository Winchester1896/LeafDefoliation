# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 19:45:28 2020

@author: tosee
"""

import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import pickle
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-f", type=str, required=True,
                help="input image folder")

args = vars(ap.parse_args())


path = args['f'] + '/'
ppath = args['f'] + '_data/'
npath = args['f'] + '_processed/'

if not os.path.exists(npath):
    os.mkdir(npath)
if not os.path.exists(ppath):
    os.mkdir(ppath)
sns.set(color_codes=True)


def CropImage(p, pp):
    folder = os.listdir(path)
    for file in folder:
        img = cv2.imread(path + file)
        h, w, c = np.shape(img)
        cuth = int(h * 0.15)
        cutw = int(w * 0.15)
        img = img[cuth:(h-cuth), cutw:(w-cutw)]
        cv2.imwrite(pp+file, img)
    print('done.')


def LeafSegmentation(path, lowThreshold, ratio, kernel_size):
    folder = os.listdir(path)
    mean_garea = 0
    mean_gedge = 0
    l = len(folder)
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
        # sns_fig.tick_params(labelsize=50)
        sns_fig.savefig(npath + 'hist_' + folder[z])
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
        cv2.imwrite(npath + 'binary_img_' + folder[z], bimg)
        
        (b1, g1, r1) = cv2.split(testimg)
        cimg = cv2.merge([b1 & bimg, g1 & bimg, r1 & bimg])
        
        cv2.imwrite(npath + 'colorimg_' + folder[z], cimg)
        
        img = cv2.imread(path + folder[z])
        cnt, hie = cv2.findContours(bimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt_img = cv2.drawContours(img, cnt, -1, (0, 255, 0), 3)
        
        cv2.imwrite(npath + 'contour_img_' + folder[z], cnt_img)
        
        detected_edges = cv2.cvtColor(cimg, cv2.COLOR_BGR2GRAY)
        detected_edges = cv2.Canny(detected_edges,lowThreshold,lowThreshold*ratio,apertureSize = kernel_size)
        # dst = cv2.bitwise_and(cimg,cimg,mask = detected_edges)
        
        cv2.imwrite(npath + 'edge_img_' + folder[z], detected_edges)
        
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




# CropImage(path, ppath)
image_list, ae_list = LeafSegmentation(path, 50, 3, 3)

kmeans = KMeans(n_clusters=5, random_state=0).fit(ae_list)
pickle.dump(kmeans, open('kmeans.pkl', 'wb'))
labels = kmeans.labels_

with open(ppath + 'data.txt', 'a+')as f:
    for i in range(len(image_list)):
        f.write(image_list[i] + ',' + str(ae_list[i]) + ',' + str(labels[i]))
        f.write('\n')
f.close()





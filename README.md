# LeafDefoliation

Since I don't have labelled data set yet. I'm using KMeans clustering algorithm to classify images of different defoliation rate. 

Python dependancies
pickle
argparse
opencv
numpy
seaborn
matplotlib

1. leaf_defoliation.py 
Usage example: python leaf_defoliation.py -f cropped_images
For calculating the AE ratio for each image and training a kmeans model. Input should be a folder containing leaf images, output contains (a) a folder with leaf edge image, leaf area image, leaf mask image and leaf ExG histogram figure for each imput image. (b) a folder containing AE ratio data and kmeans label for each image (All data in one file). (c) a kmeans model named "kmeans.pkl". 

2. kmeans_predict.py
Usage example: python kmeans_predict.py -m kmeans.pkl -f test -o results.txt
For predicting the classes of new data using the kmeans model. Input should be a folder containing all test images. Output contains one txt file containing image name, AE ratio and the predicted class for all test images.

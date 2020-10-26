# LeafDefoliation

Since I don't have labelled data set yet. I'm using KMeans clustering algorithm to classify images of different defoliation rate. 

1. leaf_defoliation.py 
For calculating the AE ratio for each image and training a kmeans model. Input should be a folder containing leaf images, output contains (a) a folder with leaf edge image, leaf area image, leaf mask image and leaf ExG histogram figure for each imput image. (b) a kmeans model named "kmeans.pkl". 

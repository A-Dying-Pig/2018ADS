You are required to install:
----"python 3.x"
----"tensorflow"
----"matplotlib"
----"sklearn"


To query image, do the following steps:
1.place the images in the folder---input
2.run "query.py", the result will be placed in folder --- output/result.txt
3.if you want to check the result images, run "view.py". The image in the first line is the query image and the following images are searched results. The priorer the image is, the higher the relevance is.
  type "a" or "d" in the console to change the query image
  type "q" in the console to quit

you can choose different ways to get k nearest neighbors in file "query.py", function--"straight_search" is direct search in which each query is O(N), function---"kdtree_search"  uses kd-tree to search in which each query is O(log N), function----"method3_search" uses hash function to search in which each query is O(1) and the initialization is O(NlogN)

image should be in the format "*.jpg","*.JPEG",".*jpeg"

folder "model" is placed with inception_v3 model
folder "retrained" is placed with retrained model
folder "features" restore the library's images' feature vectors 
folder "runs" restore the temporary data while retraining


file "retrain.py" is for retrain model
file "feature_extraction.py" is for calculating feature vector
file "resize_image.py" is to adapt the image to the size 299x299 which is required by the model--inception_v3


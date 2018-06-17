import tensorflow as tf
import numpy as np
import os
from PIL import Image
from sklearn.neighbors import NearestNeighbors
import glob
import matplotlib.pyplot as plt
import math

model_dir = 'retrained'
model_name = 'output_graph.pb'
image_dir = 'input/resized'
k = 10
MAX_DIS = 100
filename = "output/result.txt"

def create_graph():
    with tf.gfile.FastGFile(os.path.join(
            model_dir, model_name), 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')


def convertjpg(jpgfile,outdir,width=299,height=299):
    img=Image.open(jpgfile)   
    new_img=img.resize((width,height),Image.BILINEAR)   
    new_img.save(os.path.join(outdir,os.path.basename(jpgfile)))

def resize_image():
    for jpgfile in glob.glob("input/*.JPEG"): 
        convertjpg(jpgfile,"input/resized")
    for jpgfile in glob.glob("input/*.jpg"): 
        convertjpg(jpgfile,"input/resized")
    for jpgfile in glob.glob("input/*.jpeg"): 
        convertjpg(jpgfile,"input/resized")

def delete_image():
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            os.remove("./input/resized/"+file)

def read_features():
    vector = []
    name = []
    with open('features/write_data.txt') as f: 
        lines = f.readlines()
    total_len = len(lines)
    
    for line in lines:
        n = line.split(":")[0]
        vec = line.split(":")[1]
        arr = np.array([float(x) for x in vec.split(',')])
        vector.append(arr)
        name.append(n)
    return name,vector,total_len



def straight_search(vector,total_len,target_vector):
    nearest = []
    for i in range(k):
        ele = [0,MAX_DIS]
        nearest.append(ele)
    for i in range(total_len):
        dis = np.sqrt(np.sum(np.square(target_vector - vector[i])))
        #print(dis)
        for j in range(k):
            if dis < nearest[j][1]:
                for z in range(k - 1,j,-1):
                    #print(z)
                    nearest[z][0] = nearest[z-1][0]
                    nearest[z][1] = nearest[z-1][1]
                nearest[j][0] = i
                nearest[j][1] = dis
                break
    #print(nearest)
    return nearest

def kdtree_search(vector,total_len,target_vector):
    ve = []
    ve.append(target_vector)
    for i in range(total_len):
        ve.append(vector[i])
    nbrs = NearestNeighbors(n_neighbors = k + 1, algorithm="kd_tree").fit(ve)
    distances, indices = nbrs.kneighbors(ve)
    nearest = []
    for i in range(k):
        nearest.append([indices[0,1:][i] - 1,0])
    #print(indices[0,1:])
    #print(nearest)
    return nearest


def getLSH(onevector, k):
    tempresult = []
    result = 0
    for index in range(len(onevector)):
        #这里还要改进分布的离散程度,哈希方法
        temp = onevector[index] * 10 + index
        tempresult.append(temp)
    for alpha in range(0, 8):
        test = 0;
        for index in range(len(onevector)):
            if(pow(2, alpha) & tempresult[index] == pow(2, alpha)):
                delta = 1
            else:
                delta = -1
            test += k[index] * delta
        if(test > 0):
            result += pow(2, alpha)
    return result

def getDistance(onevector, anothervector, deminsion):
    result = 0
    for i in range(deminsion):
        result += math.pow(onevector[i] - anothervector[i], 2)
    result = math.sqrt(result)
    return result

def getNewVector(characters, total_len, deminsion):
    tempcharacters = []
    scales = []
    for index in range(total_len):
        temptempcharacters = []
        for i in range(deminsion):
            temptempcharacters.append(characters[index][i])
        temptempcharacters.append(index)
        tempcharacters.append(temptempcharacters)
    for i in range(deminsion):
        tempcharacters.sort(key = lambda x:x[i])
        j = 0
        tempscales = []
        for index in range(total_len):
            if(index < total_len * (j+1) / 16):
                tempcharacters[index][i] = j
            else:
                tempscales.append(tempcharacters[index][i])
                j += 1
                tempcharacters[index][i] = j
        scales.append(tempscales)
    tempcharacters.sort(key = lambda x:x[deminsion])
    for index in range(total_len):
        tempcharacters[index].pop(deminsion)
    return tempcharacters, scales

def getNewPredictions(predictions, scales, deminsion):
    newpredictions = []
    for i in range(deminsion):
        for j in range(len(scales[i])):
            if(predictions[i] < scales[i][j]):
                newpredictions.append(j)
                break
    return newpredictions

def create_hash(vector, k, total_len):
    result = [[] for i in range(256)]
    for index in range(total_len):
        hash = getLSH(vector[index], k)
        result[hash].append(index)
    return result

def hash_search(hash, k, total_len, deminsion, predictions):
    tempresult = getLSH(predictions, k)
    #print(tempresult)
    result = []
    for index in range(len(hash[tempresult])):
        result.append(hash[tempresult][index])
    return result

def getKfromResult(result, vector, predictions, k, deminsion):
    trueResult = []
    reallyTrueResult = []
    for index in range(len(result)):
        tempresult = []
        tempresult.append(result[index])
        tempresult.append(getDistance(vector[result[index]], predictions, deminsion))
        trueResult.append(tempresult)
    trueResult.sort(key = lambda x:x[1])
    if(len(result) < k):
        k = len(result)
    for i in range(k):
        reallyTrueResult.append(trueResult[i][0])
    return reallyTrueResult

def method3_search(vector, total_len, predictions):
    newvector, scales = getNewVector(vector, total_len, 10)
    newprediction = getNewPredictions(predictions, scales, 10)
    myk = [1] * 10
    my_hash = create_hash(newvector, myk, total_len)
    method3result = hash_search(my_hash, myk, total_len, 10, newprediction)
    kResult = getKfromResult(method3result, vector, predictions, 10, 10)
    return kResult


#------------------------------------------------main-------------------------------------------
delete_image()
resize_image()
create_graph()
name,vector,total_len = read_features()
#print(total_len)

with tf.Session() as sess:
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    
    with open(filename,'w') as output:
        for root, dirs, files in os.walk(image_dir):
            for file in files:
                print("reading:\t"+file)
                image_data = tf.gfile.FastGFile(os.path.join(root, file), 'rb').read()
                predictions = sess.run(softmax_tensor,{'DecodeJpeg/contents:0': image_data})
                predictions = np.squeeze(predictions)

                #-----Method 1 to get K nearest neighbors-----straight research
                #nearest = straight_search(vector,total_len,predictions)
                #-----Method 2 ------- kd tree
                #nearest = kdtree_search(vector,total_len,predictions)
                #-----Method 3 ------- hash
                kResult = method3_search(vector, total_len, predictions)

                output.write(file+":")

                #Method1/2-----output---------
                #for i in range(k):
                #    if i == k - 1:
                #        output.write(name[nearest[i][0]]+"\n")
                #    else:
                #        output.write(name[nearest[i][0]]+",")
                
                #-----Method3---output----hash-----
                for i in range(k):
                    if i == k - 1: 
                        output.write(name[kResult[i]]+"\n")
                    else:
                        output.write(name[kResult[i]]+",")


import tensorflow as tf
import numpy as np
import os
from PIL import Image
import glob
import matplotlib.pyplot as plt

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

delete_image()
resize_image()
create_graph()
name,vector,total_len = read_features()

with tf.Session() as sess:
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    
    with open(filename,'w') as output:
        for root, dirs, files in os.walk(image_dir):
            for file in files:
                print("reading:\t"+file)
                image_data = tf.gfile.FastGFile(os.path.join(root, file), 'rb').read()
                predictions = sess.run(softmax_tensor,{'DecodeJpeg/contents:0': image_data})
                predictions = np.squeeze(predictions)
                nearest = straight_search(vector,total_len,predictions)

                output.write(file+":")

                for i in range(k):
                    if i == k - 1:
                        output.write(name[nearest[i][0]]+"\n")
                    else:
                        output.write(name[nearest[i][0]]+",")
                
                


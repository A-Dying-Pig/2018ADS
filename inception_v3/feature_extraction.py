import tensorflow as tf
import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt

filename = 'features/write_data.txt'
model_dir = 'retrained'
model_name = 'output_graph.pb'
image_dir = 'data/images'

def create_graph():
    with tf.gfile.FastGFile(os.path.join(
            model_dir, model_name), 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

create_graph()

with tf.Session() as sess:
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    
    with open(filename,'w') as output:
        for root,dirs,files in os.walk(image_dir):
            for file in files:
                if file.endswith('.JPEG'): 
                    print(file)
                    image_data = tf.gfile.FastGFile(os.path.join(root, file), 'rb').read()
                    predictions = sess.run(softmax_tensor,{'DecodeJpeg/contents:0': image_data})
                    predictions = np.squeeze(predictions)
                    p_str = ','.join(str(x) for x in predictions) # '0,3,5'
                    #print (p_str)
                    output.write(file+":"+p_str+"\n")
            

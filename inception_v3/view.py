import tensorflow as tf
import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt

result_name = "output/result.txt"
NUM_PER_ROW = 4
plt.ion()

def image_union(origin,name):

	UNIT_SIZE = 299 # the size of image 
	img_num = len(name)
	if img_num % NUM_PER_ROW == 0:
		row = (int)((img_num/NUM_PER_ROW)+1)
	else:
		row = (int)((img_num/NUM_PER_ROW)+2)
	target = Image.new('RGB', (UNIT_SIZE*NUM_PER_ROW, UNIT_SIZE*row))

	origin_image_path = "input/resized/"+origin
	ori = Image.open(origin_image_path)
	target.paste(ori, (0, 0, UNIT_SIZE , UNIT_SIZE))
	images = []
	for i in range(img_num):
		image_path = "data/images/"+name[i].split("_")[0] + "/" + name[i]
		tmp_img = Image.open(image_path)	
		images.append(tmp_img)

	for i in range(img_num):
		i_row = int(i / NUM_PER_ROW) + 1
		i_col = i % NUM_PER_ROW
		target.paste(images[i], (i_col*UNIT_SIZE, i_row*UNIT_SIZE, i_col*UNIT_SIZE + UNIT_SIZE, i_row*UNIT_SIZE+UNIT_SIZE))
	return target


def view():
	with open(result_name) as f:
		lines = f.readlines()
		total_len = len(lines)
		i = 0
		while 1:
			origin = lines[i].split(",")[0]
			n1 = lines[i].split(",")[1]
			n = n1.split("\n")[0]
			name = [x for x in n.split(';')]
			image = image_union(origin,name)
			plt.imshow(image)
			plt.axis('off')
			plt.show()
			x = input()
			if x == "q":
				break
			if x == "d":
				i = (i + 1)%total_len
			if x == "a":
				i = (i - 1 + total_len)%total_len
			plt.close()

view()

	
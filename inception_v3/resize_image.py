from PIL import Image
import os.path
import glob
def convertjpg(jpgfile,outdir,width=299,height=299):
	img=Image.open(jpgfile)   
	new_img=img.resize((width,height),Image.BILINEAR)   
	new_img.save(os.path.join(outdir,os.path.basename(jpgfile)))

for jpgfile in glob.glob("data/image/*.JPEG"): 
	t1 = jpgfile.split("data/image/")[1]
	t2 = t1.split("_")[0]
	t3 = "retrained/bottleneck/" + t2
	print(t3)
	if not os.path.exists(t3):
		os.mkdir(t3)
	convertjpg(jpgfile,t3)
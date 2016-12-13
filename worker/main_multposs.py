import improcess as imp
import os
from multiprocessing import Pool
from PIL import Image

def sub_imgray(filename):
	print filename
	image = Image.open('process_image/'+filename)
	image = imp.imgray(image)
	image.save('gray_image/'+filename)

if __name__ == '__main__':

	piclist = os.listdir('process_image')

	num = len(piclist)
	p=Pool(4)
	
	if os.path.isdir('gray_image'):
		pass
	else:
		os.makedirs('gray_image')

	for i in range(num):
		#print 'Hello'
		filename = piclist[i]
		p.apply_async(sub_imgray,args=(filename,))
	print ('Waing for the Multi processing')
	p.close()
	p.join()
	print ('multi porcessing is over')
	

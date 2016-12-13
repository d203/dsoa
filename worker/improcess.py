from PIL import Image
from PIL import ImageDraw


def imgray(sourceimage):
	image1 = sourceimage
	image2 = ImageDraw.Draw(image1)
	image3 = image1.convert('RGB')
	height,width = image1.size
	for i in range(height):
		for o in range(width):
			R,G,B = image3.getpixel((i,o))
			L = (R+G+B)/3
			image3.putpixel((i,o),(L,L,L))
	return image3
	
	

from pylab import *
I=imread(input_file_path)
I=255-I
imsave(output_file_path,I)

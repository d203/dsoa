import numpy as np
import h5py
from pylab import *
import os
root_dir="../worker/process_image/"
path_ls=os.listdir(root_dir)
images=np.ndarray(len(path_ls),dtype=np.ndarray)
i=0
for file_name in path_ls:
    file_path=os.path.join('%s%s'%(root_dir,file_name))
    images[i]=imread(file_path)
    i=i+1


file=h5py.File('img_set.h5','w')
file.create_dataset('image',data=images)

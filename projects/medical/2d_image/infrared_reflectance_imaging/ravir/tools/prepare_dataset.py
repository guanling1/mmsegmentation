import glob
import os

import numpy as np
from PIL import Image
from tqdm import tqdm

# map = {255:2, 128:1, 0:0}

imgs = glob.glob(os.path.join('./masks/train', '*.png'))

for im_path in tqdm(imgs):
    im = Image.open(im_path)
    imn = np.array(im)
    imn[imn == 255] = 2
    imn[imn == 128] = 1
    imn[imn == 0] = 0
    new_im = Image.fromarray(imn)
    new_im.save(im_path)
#!/usr/bin/env python3
#
# gsboone@gmail.com
# Space Nerd
#
# For all your screen saver needs
#
# (might need to pip install requests and pillow)

import argparse
import requests
from PIL import Image
import os
import re
import random
import sys

d_help='Give a directory path to store your hubbletrek images. Default: ~/hubbletrek'
parser = argparse.ArgumentParser(description='Download hubble telescope images, and throw in a little ST:TNG')
parser.add_argument('-d', '--directory', type=str, default='~/hubbletrek', help=d_help)
args = parser.parse_args()

path = os.path.expanduser(args.directory)

def hubble_snatch(path):
    run_once(path,'check')
    for x in range(1000):
        num = str(x).zfill(3)
        Url = r'https://cdn.spacetelescope.org/archives/images/screen/heic0{}a.jpg'.format(num)
        hubble_img = os.path.expanduser('{}/hubbletrek{}.jpg'.format(path,num))
        sauce = requests.get(Url, stream=True)
        if sauce.status_code == 200:
            with open(hubble_img, 'wb') as f:
                for chunk in sauce:
                    f.write(chunk)
            f.close()

def img_combiner(path):
    ncc1701d_l = [ 'ncc1701d_1.png', 'ncc1701d_2.png', 'ncc1701d_3.png' ]
    images = []
    [ images.append(f) for f in os.listdir(path) if re.search(r'jpg', f) ]
    for image in images:
        image_path = os.path.join(path,image)
        background = Image.open(image_path)
        bw, bh = background.size
        foreground = Image.open(os.path.join(ncc1701d_l[random.randrange(3)]))
        fw, fh = foreground.size
        background.paste(foreground, (random.randrange(bw-fw),random.randrange(bh-fh)), foreground)
        background.save(image_path)
    run_once(path,'done')

def run_once(path,task):
    ro_file = 'hubbletrek_run_complete'
    complete = os.path.join(path,ro_file)
    if task == 'done':
        f = open(complete, 'a')
        f.close
    elif task == 'check':
        if os.path.isfile(complete):
            print('hubbletrek already ran in {}. Delete "{}" to force a rerun. Beware time traveling Enterprises on forced runs.'.format(path,complete))
            sys.exit(0)
        else:
            pass

def main():
    hubble_snatch(path)
    img_combiner(path)

if __name__ == '__main__':
    main()

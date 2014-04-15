# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import glob
import os
import shutil

# nacitani z adresare
def readImageDir(path):
    dirs = glob.glob(os.path.join(os.path.normpath(path) ,'*'))
    labels = []
    files = []
    for onedir in dirs:
        #print onedir
        base, lab = os.path.split(onedir)
        if os.path.isdir(onedir):
            filesInDir = glob.glob(os.path.join(onedir, '*'))
            for onefile in filesInDir:
                labels.append(lab)
                files.append(onefile)
        
    return files, labels

def splitDataset(path, outputpath, nfirst=10):
    dirs = glob.glob(os.path.join(os.path.normpath(path) ,'*'))

    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    labels = []
    files = []
    for onedir in dirs:
        #print onedir
        base, lab = os.path.split(onedir)
        
        directory = os.path.join(outputpath, lab)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        if os.path.isdir(onedir):
            filesInDir = glob.glob(os.path.join(onedir, '*'))
            # beru si prvních deset souborů
            # šlo by upravit i pro náhodný výběr
            filesInDir.sort()
            filesInDir = filesInDir[:nfirst]
            for onefile in filesInDir:
                base, srcfile = os.path.split(onefile)
                destfile = os.path.join(directory, srcfile)
                print onefile, '  ', destfile
                
                shutil.copy2(onefile, destfile)
                #labels.append(lab)
                #files.append(onefile)
        
    return files, labels

# <codecell>

# rozdělení datasetu. Vezme se vždy prvních deset souborů z daného adresáře
#splitDataset('/home/mjirik/data/zdo2014/znacky/','/home/mjirik/data/zdo2014/znacky-testing/')
import random
import numpy as np
arr = ['agg', 'bag', 'dada', 'rea', 'raw', 'rwew', 'sra', 'reew']
ind = np.random.random_integers(7,size=3)

arr.pop(ind)


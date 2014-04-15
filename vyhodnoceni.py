# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Vyhodnocovací systém

# <markdowncell>

# Hodhocení prací probíhá pomocí následujícího kódu.

# <codecell>


import signal
from contextlib import contextmanager
import skimage
import skimage.io
import numpy as np
import urllib
import glob
import zipfile
import shutil
import sys
import os
import os.path
import traceback
import datetime
import pickle

#print dir(urllib)
#import urllib.request

# ziskani seznamu 
import solutions_list
%run solutions_list

# <headingcell level=2>

# Načítání dat

# <codecell>

def readImageDir(path):
    """
    Načítání dat z adresářové struktury. Funkce vrací seznam souborů a seznam labelů.
    Ty jsou získávány z názvů jednotlivých složek.
    """
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

# <headingcell level=2>

# Funkce pro spuštení studenských řešení

# <codecell>

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException, "Timed out!"
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

       
def kontrola(ukazatel):
    """
    Kontrola jednoho studentského řešení
    """
    studentske_reseni = ukazatel() # tim je zavolán váš konstruktor __init__
    
    # Trenovani
    
    filesall, labelsall = readImageDir(
        '/home/mjirik/data/zdo2014/zdo2014-training/')
    #filesall, labelsall = readImageDir(
    #    '/home/mjirik/mnt/pole_korpusy/queetech/zdo/znacky/')
    
    obrazky = filesall[2::8]
    reseni = labelsall[2::8]
    
    print "Total image number: " + len(obrazky)
    
    vysledky = []
    
    for i in range(0, len(obrazky)):
        im = skimage.io.imread(obrazky[i])

        # Zde je volána vaše funkce rozpoznejZnacku
        try:
            with time_limit(1):
                result = studentske_reseni.rozpoznejZnacku(im)
        except TimeoutException, msg:
            print "Timed out!"
            result = None
            
        vysledky.append(result)

    hodnoceni = np.array(reseni) == np.array(vysledky)
    
    skore = np.sum(hodnoceni.astype(np.int)) / np.float(len(reseni))
    
    return skore

def my_import(name):
    __import__(name)
    return sys.modules[name]

    
def kontrolaVse():
    """
    Kontrola všech studentských řešení
    """
    scores = []
    teams = []
    stamps = []
    soldir = 'ZDO2014students'
    try:
        shutil.rmtree(soldir)
    except:
        print "Problem with rmtree"
            
    try:
        os.mkdir(soldir)
        open(os.path.join(soldir, "__init__.py"), 'a').close()  
    except:
        print "Problem with mkdir"

    # download all solutions
    for one in solutions_list:
        zip_path = os.path.join(soldir, one[1] + '.zip')
        urllib.urlretrieve(one[0], zip_path)
        
        zf = zipfile.ZipFile(zip_path, "r")
        zf.extractall(soldir)
        
        teamsoldir = zip_path = os.path.join(soldir, one[1])
        # create __init__.py 
        open(os.path.join(teamsoldir, "__init__.py"), 'a').close() 
        
        # remove '-' from package path
        teamsoldirnew = teamsoldir.replace('-', '')
        os.rename(teamsoldir, teamsoldirnew)

    # evaluate solutions
    for one in solutions_list:
        scoreone = 0
        try:
            imp1 = my_import('ZDO2014students.' + one[1].replace('-', ''))
            imp2 = my_import('ZDO2014students.' + one[1].replace('-', '') 
                             + '.' + one[2])
            #print imp2
            pointer = imp2.Znacky
            #import ZDO2014sample_solution
            #pointer = ZDO2014sample_solution.Znacky
            scoreone = kontrola(pointer)
        except:
            traceback.print_exc()
            print "Problem with: " + one[2]
        teams.append(one[2])
        scores.append(scoreone)

        #this is whole timestamp. I want only date
        dat = datetime.datetime.now()
        #nw = datetime.datetime.now()
        #dat = datetime.date(nw.year, nw.month, nw.day)
        stamps.append(dat)
        
        
    #print teams
    #print scores
    return teams, scores, stamps

# <headingcell level=2>

# Ukládání výsledků

# <codecell>

def saveAndMergeEvaluation(teams, scores, stamps, filename="ZDO2014evaluation.csv"):
    #evaluation = {'teams':[], 'scores':[], 'stamps': []}
    #try:
    #    stored_evaluation = pickle.load(open(filename, "rb" ))
    #    eval.update(stored_evaluation)
    #except:
    #    print "Cannot read stored data"
    #    
    #evaluation['teams'].append(teams)
    #evaluation['scores'].append(scores)
    #evaluation['stamps'].append(stamps)
    
    # write with pickle
    #pickle.dump(evaluation, open( filename, "wb" ))
    # write to csv
    import pandas as pd
    try:
        orig_data = pd.read_csv(filename)
        #print 'orig data'
        #print orig_data
    except:
        print "Cannot read stored data"
    
    dates = []
    times = []
    for stamp in stamps:
        dat = stamp.date()
        tm = stamp.time()
        dates.append(dat)
        times.append(tm)
        
    #data = np.array([evaluation['teams'], 
    #                 evaluation['scores'],
    #                 evaluation['stamps']]).T
    npdata = np.array([teams, scores, dates, times]).T
    df = pd.DataFrame(npdata, columns=['team', 'score', 'date', 'time'])
    
    try:
        # there could be wrong format
        df = orig_data.append(df, ignore_index=True)
    except:
        print "wrong format of input csv, rewriting"
    
    df.to_csv(filename, index=False)
    #print df
    #df = pd.DataFrame(data, columns=['team', 'score', 'timestamp'])
    #df.to_csv('ZDO2014evaluation.csv')
    
    
    return df

# <headingcell level=1>

# Vyhodnocení

# <codecell>

if __name__ == "__main__":
    teams, scores, stamps = kontrolaVse()
    tdf = saveAndMergeEvaluation(teams, scores, stamps)
    print tdf
    #printEvaluation(teams, scores, stamps)

# <codecell>



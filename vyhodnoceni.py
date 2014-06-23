# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Vyhodnocovací systém

# <markdowncell>

# Hodhocení prací probíhá pomocí následujícího kódu. Práce jsou automaticky staženy z adres zadaných v "solution_list.ipynb". Pak jsou spuštěny a všechny otestovány na shodné náhodné podskupině testovacího datasetu. Na výsledky je pak možno navázat ve skrpitu "ZDO2014tabulka.ipynb"

# <headingcell level=2>

# Poznámky pro spouštění testu

# <markdowncell>

# V případě opakovaného spouštění testování je z důvodu opakovaných importů modulů se stejnými jmnény nezbytné restartovat kernel. To lze udělat pomocí Kernel -> Restart
# 
# Výchozí adresář s testovacími daty je na staven na následující cestu
# 
#     /home/mjirik/data/zdo2014/znacky-testing/

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
import random

#print dir(urllib)
#import urllib.request

# ziskani seznamu 
import solutions_list
%run solutions_list

# cesta k trenovacim datum
test_data_path = '/home/mjirik/data/zdo2014/zdo2014-znacky-testing/'

# Nastaveni logovaciho souboru
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(filename='znacky.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

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

       
def kontrola(ukazatel, obrazky, reseni):
    """
    Kontrola jednoho studentského řešení
    """
    studentske_reseni = ukazatel() # tim je zavolán váš konstruktor __init__
    
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
    
    return skore, vysledky

def my_import(name):
    __import__(name)
    return sys.modules[name]

def downloadAll(soldir):
    try:
        shutil.rmtree(soldir)
    except:
        print "Problem with rmtree"
        traceback.print_exc()
            
    try:
        os.mkdir(soldir)
        open(os.path.join(soldir, "__init__.py"), 'a').close()  
    except:
        print "Problem with mkdir"
        traceback.print_exc()
        
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
        teamsoldirnew = teamsoldir.replace('-', '') + one[4]
        os.rename(teamsoldir, teamsoldirnew)
    
def kontrolaVse():
    """
    Kontrola všech studentských řešení
    """
    
    soldir = 'ZDO2014students'
    downloadAll(soldir)
    
    
    scores = []
    teams = []
    stamps = []
    classifs = []
    
   

    filesall, labelsall = readImageDir(test_data_path)
        
    #sklearn.cross_validation.train_test_split(

    init_seed = int(random.random()*5.0)
    
    obrazky = filesall[init_seed::6]
    reseni = labelsall[init_seed::6]
    
    classifs.append(reseni)
    
    print "Total image number: ", len(obrazky)
    logger.debug("Total image number: " + str(len(obrazky)))
    # evaluate solutions
    for one in solutions_list:
        logger.debug("Team: " + one[3])
        scoreone = 0
        vysledky = []
        try:
            imp1 = my_import('ZDO2014students.' + one[1].replace('-', '') + one[4])
            imp2 = my_import('ZDO2014students.' + one[1].replace('-', '') + one[4]
                             + '.' + one[2])
            #print imp2
            pointer = imp2.Znacky
            #import ZDO2014sample_solution
            #pointer = ZDO2014sample_solution.Znacky
            scoreone, vysledky = kontrola(pointer, obrazky, reseni)
        except:
            
            print "Problem with: " + one[3]
            exc = traceback.format_exc()
            print exc
            logger.debug("Problem with: " + one[3])
            logger.debug(exc)
            print "------------------------"
            vysledky = reseni
        teams.append(one[3])
        scores.append(scoreone)
        classifs.append(vysledky)
        

        #this is whole timestamp. I want only date
        dat = datetime.datetime.now()
        #nw = datetime.datetime.now()
        #dat = datetime.date(nw.year, nw.month, nw.day)
        stamps.append(dat)
        
        
    #print teams
    #print scores
    return teams, scores, stamps, classifs

# <headingcell level=2>

# Ukládání výsledků

# <codecell>

def saveAndMergeEvaluation(teams, scores, stamps, 
                           filename="ZDO2014evaluation.csv"):
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
        
    npdata = np.array([teams, scores, dates, times]).T
    df = pd.DataFrame(npdata, columns=['team', 'score', 'date', 'time'])
    
    try:
        # there could be wrong format
        df = orig_data.append(df, ignore_index=True)
    except:
        print "wrong format of input csv, rewriting"
    
    df.to_csv(filename, index=False)
   
    return df

def saveClassifs(teams, classifs, filename='ZDO2014classifs.csv'):
    """
    Zápis veškerých klasifikací do csv souboru
    """
    import pandas as pd
    cl = teams[:]
    cl.insert(0, 'reference')
    # vytvoř vhodný formát pro uložení
    aa = {cl[i]:classifs[i] for i in range(0, len(cl))}
    
    df = pd.DataFrame(aa)
    df.to_csv(filename, index=False)

# <headingcell level=1>

# Vyhodnocení

# <codecell>

if __name__ == "__main__":
    teams, scores, stamps, classifs = kontrolaVse()
    tdf = saveAndMergeEvaluation(teams, scores, stamps)
    saveClassifs(teams, classifs)
    
    #printEvaluation(teams, scores, stamps)

# <codecell>

print tdf.tail(50)

# <codecell>



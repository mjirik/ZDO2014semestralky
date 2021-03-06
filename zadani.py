# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Rozpoznávání dopravních značek

# <markdowncell>

# Cílem práce je napsat stroj na automatické rozpoznávání dopravních značek.
# 
# Trénovací data naleznete na následující adrese
# http://147.228.240.61/zdo/
# 
# 
# ![zn1](http://147.228.240.61/zdo/IS3d_id13277_ff7741-FL_1_131030_00067306-1.jpg)
# ![zn2](http://147.228.240.61/zdo/P1_id13258_ff7546-FL_1_131030_00066180-1.jpg)
# ![zn3](http://147.228.240.61/zdo/Z3_id18972_ff2347-FL_1_131030_00020439.jpg)
# ![zn3](http://147.228.240.61/zdo/P2_id14368_ff74-FL_1_131030_00002530.jpg)

# <headingcell level=2>

# Jakou podobu má mít řešení?

# <markdowncell>

# Cílem vaší práce je skript v jazyce python, který bude posouzen automatickým vyhodnocením. Proto je potřeba dbát na předepsanou formu. Hlavní skript musí obsahovat třídu Znacky. Ta má povinnou funkci rozpoznejZnacku(). 
# 
# Ve webově dostupné podobě lze studovat podrobnosti (nepříliš dobře) [fungujícího řešení](https://github.com/mjirik/ZDO2014sample_solution)
# 
# Nač je potřeba dát pozor:
# 
# * class Znacky
# * funkce rozpoznejZnacku()
# * případné datové soubory je nutné adresovat relativně pomocí `__file__` (viz init v navazujícím příkladu)
# * demo režim
# 
# Ty nejpodstatnější věci ukazuje následující kód. 

# <codecell>

class Znacky:
    """
    M. Jiřík
    I. Pirner
    P. Zimmermann
    
    Takto bude vytvořeno vaše řešení. Musí obsahovat funkci 'rozpoznejZnacku()', 
    která má jeden vstupní parametr. Tím je obraz. Doba trváná funkce je 
    omezena na 1 sekundu. Tato funkce rovněž musí obsahovat 
    ukázkový režim. V něm je pomocí obrázků vysvětleno, jak celá věc pracuje.
    """
    def __init__(self):
        # Načítání natrénovaných parametrů klasifikátoru ze souboru atd.
        
        # Soubory je nelze načítat pomocí prosté cesty
        # Je potřeba adresovat relativně k poloze aktuálnímu skriptu
        # vyzkoušet je to možné spuštěním skriptu z jiného než aktuálního adresáře
        # python ../projects/zdo/mujsuperskript.py
        
        ## cesta ke skriptu
        # path_to_script = os.path.dirname(os.path.abspath(__file__))
        ## spojení s relativní cestou
        # classifier_path = os.path.join(path_to_script, "../data/data.pkl")
        pass
    
    def rozpoznejZnacku(self, image, demo=False):
        
        # Nějaký moc chytrý kód
        if image.shape[0] > 10:
            retval = 'P2'
        else:
            retval = 'C4a'
            
        if demo:
            print "Výpisy parametrů, obrázky atd."
        
        return retval

# <codecell>

import glob
import os

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
    

files, labels = readImageDir('/home/mjirik/data/zdo2014/zdo2014-training/')
print "pocet souboru ", len(files)
print 'prvnich 3 soubory \n', files[0:3]
print 'prvnich 3 labely \n', labels[0:3]

# <headingcell level=2>

# Vyhodnocení

# <markdowncell>

# Vyhodnocení bude probíhat hromadně. Pythonovské (a případné jakékoliv další) soubory musejí být v adresáři, který je zabalen do zipu a zveřejněn kdekoliv na síti. 
# 
# 
# 
# Pro vyhodnocení:
# 
# 1. Vytvořte zip se skriptem a zveřejněte jej kdekoliv na internetu
# 2. Zašlete cvičícímu následující informace:
#     1. Veřejně dostupné url k zip souboru
#     2. Jméno adresáře v zipu
#     3. Jméno hlavního skriptu
#     4. Krátké pojmenování týmu
#     
# Ukázkové řešení je tedy toto:
# 
# 1. Ukázkový zip je [zde](https://github.com/mjirik/ZDO2014sample_solution/archive/master.zip)
# 2. Informace potřebné pro spuštění:
#     1. https://github.com/mjirik/ZDO2014sample_solution/archive/master.zip
#     2. 'ZDO2014sample_solution-master'
#     3. 'ZDO2014sample_solution'
#     4. 'sample M. Jirik'
# 
# 
# Tyto informace budou vloženy do [seznamu řešení](http://nbviewer.ipython.org/github/mjirik/ZDO2014semestralky/blob/master/solutions_list.ipynb?create=1). Jeho veřejná podoba nebude aktualizována, takže se adresu s vaším řešením tímto způsobem nikdo nedoví.
# 
# Výsledky budou vyhodnoceny dvakrát týdně. Veřejně dostupný je [vyhodnocovací skript](http://nbviewer.ipython.org/github/mjirik/ZDO2014semestralky/blob/master/vyhodnoceni.ipynb) i s [průběžnými výsledky](http://nbviewer.ipython.org/github/mjirik/ZDO2014semestralky/blob/master/table.ipynb).
# 
# Pro potřeby vašeho testování lze použít následující vyhodnocování:

# <codecell>

# Zjednodušená podoba kontroly

import signal

import skimage
import skimage.io
import numpy as np


# na windows nefunguje knihovna contextlib
# v kodu je proto náhrada od M. Červeného pomocí time
import time

        
def kontrola(ukazatel):
    studentske_reseni = ukazatel() # tim je zavolán váš konstruktor __init__
    
    obrazky = ['http://147.228.240.61/zdo/P2_id14368_ff74-FL_1_131030_00002530.jpg',
             'http://147.228.240.61/zdo/Z3_id18972_ff2347-FL_1_131030_00020439.jpg',
             'http://147.228.240.61/zdo/P1_id13258_ff7546-FL_1_131030_00066180-1.jpg'
             ]
    reseni = ['P2', 'Z3', 'P1']
    
    vysledky = []
    
    for i in range(0, len(obrazky)):
        cas1 = time.clock()
        im = skimage.io.imread(obrazky[i])
        result = studentske_reseni.rozpoznejZnacku(im)           

        cas2 = time.clock()   

        if((cas2 - cas1) >= 1.0):
            print "cas vyprsel"
            result = 0

        vysledky.append(result)
            
    hodnoceni = np.array(reseni) == np.array(vysledky)
    skore = np.sum(hodnoceni.astype(np.int)) / np.float(len(reseni))
    
    print skore

# <codecell>

ukazatel = Znacky
kontrola(ukazatel)


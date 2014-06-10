# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Nejlepší výsledky každého týmu

# <markdowncell>

# Zdrojová data pro tuto tabulku jsou dostupná [zde](https://raw.githubusercontent.com/mjirik/ZDO2014semestralky/master/ZDO2014evaluation.csv)

# <codecell>

import pandas as pd
orig_data = pd.read_csv("ZDO2014evaluation.csv")
#orig_data.sort(column=['score'], ascending=False)
#print orig_data
gb = orig_data.groupby('team')
#print gb.max().sort(column=['score'], ascending=False)

gbsort = gb.max().sort(column=['score'], ascending=False)
gbsort['score']
#tt.tolist()

# <headingcell level=2>

# Bodování za technickou část funkčnosti

# <markdowncell>

# K těmto bodům jsou pak v hodnocení funkčnosti ještě přidány body za dokumentaci v kódu, demo režim, git atd.

# <codecell>

%pylab inline --no-import-all
np.power(gbsort['score'].astype(np.double),2)*36

## vizualizace progrese
#te = np.arange(0,1.1,0.1)
#y = np.power(te,2)*36

#import matplotlib.pyplot as plt
#plt.plot(te,y)

# <headingcell level=1>

# Všechny experimenty

# <codecell>

#pd.set_option('display.max_columns', None)
print orig_data.tail(40)
#print dir(pd)

# <headingcell level=1>

# Logovací soubor

# <markdowncell>

# V průběhu vyhodnocování je vytvářen logovací soubor. Nahládnout do něj můžete [zde](https://raw.githubusercontent.com/mjirik/ZDO2014semestralky/master/znacky.log). Základem je modul logging. Ten pak používáte namísto printu. 

# <markdowncell>

# Tyto řádky přidejte na začátek souboru k ostatním importům

# <codecell>

import logging
logger = logging.getLogger(__name__)

# <markdowncell>

# Tento řádek přijde do funkce main

# <codecell>

logging.basicConfig(level=logging.DEBUG)

# <markdowncell>

# A takto si vypisujete libovolné zprávy pomocí loggeru.

# <codecell>

logger.debug('muj vypis cislo ' + str(1))

# <headingcell level=1>

# Matice záměn (confusion matrix)

# <markdowncell>

# Matice záměn ukazuje, kolikrát byl label $i$ klasifikován jako $j$. V ideálním případě jsou tedy nenulová čísla pouze na diagonále. Tam jsou správné klasifikace. Jak to mělo dopadnout ukazují data pojmenovaná *reference*
# 
# Zdrojová data lze najít [zde](https://raw.githubusercontent.com/mjirik/ZDO2014semestralky/master/ZDO2014classifs.csv)

# <codecell>

%pylab inline --no-import-all
import sklearn
import sklearn.metrics
import matplotlib.pyplot as plt

df = pd.read_csv("ZDO2014classifs.csv")

cols = df.columns


print cols

# získáme seznam všech labelů značek, které jsou v testu
unlabels = np.unique(df['reference'].values)
# převedeme do čísel (indexů)
y_true = np.searchsorted(unlabels, df['reference'].values)
print unlabels

for col in cols:
    y_pred = np.searchsorted(unlabels, df[col].values)
    cmat = sklearn.metrics.confusion_matrix(y_true, y_pred)
    plt.matshow(cmat)
    plt.title(col)


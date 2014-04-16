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
print gb.max().sort(column=['score'], ascending=False)

# <headingcell level=1>

# Všechny experimenty

# <codecell>

print orig_data

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


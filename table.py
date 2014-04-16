# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Nejlepší výsledky každého týmu

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


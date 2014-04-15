# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Všechny experimenty

# <codecell>

import pandas as pd
orig_data = pd.read_csv("ZDO2014evaluation.csv")
print orig_data


# <headingcell level=2>

# Seřazeno od nejlepších

# <codecell>

print orig_data.sort(column=['score'], ascending=False)


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def import_ranking():
    return 0

mydataframe = pd.read_csv(os.getcwd() + "Dataframes/myfile")


# heatmap test
print(mydataframe.corr(method='kendall'))
sns.heatmap(data=mydataframe.corr())
plt.show()
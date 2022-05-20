import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

mydataframe = pd.read_csv("myfile")


# heatmap test
print(mydataframe.corr())
sns.heatmap(data=mydataframe.corr())
plt.show()
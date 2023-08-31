import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


data = np.array([[0.000000,0.000000],[+0.231049,0.000000],[+0.231049,0.000000]])
labels = np.array([['A','B'],['C','D'],['E','F']])
fig, ax = plt.subplots()
ax = sns.heatmap(data, annot = labels, fmt = '')

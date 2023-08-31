import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statannotations.Annotator import Annotator
from itertools import product

foots = ["rtoe", "ltoe"]
angles = ['rankle',
          'rsubt',
          'rknee',
          'rhip_addu',
          'rhip_flex',
          'rhip_rot',
          'lankle',
          'lsubt',
          'lknee',
          'lhip_addu',
          'lhip_flex',
          'lhip_rot',
          ]

pairs = list(product(foots, angles))

df_datos = None
CICLO = None

fig, axs = plt.subplots(2, 1, sharey=True, sharex=True)
df_aux = df_datos[df_datos["ciclo"] == CICLO]

# colaterales
sns.boxplot(data=df_aux[(df_aux["lados"] == "R-R") | (df_aux["lados"] == "L-L")],
            x="angulo", y='mediana',
            hue="lados",
            ax=axs[0])

# contralaterales
sns.boxplot(data=df_aux[(df_aux["lados"] == "R-L") | (df_aux["lados"] == "L-R")],
            x="angulo", y='mediana',
            hue="lados",
            ax=axs[1])

fig.suptitle(f"Resultados para ciclo {CICLO}", fontsize=20)
axs[0].grid()
axs[1].grid()

annotator = Annotator(axs, pairs, ...)

plt.show()

# data = np.array([[0.000000,0.000000],[+0.231049,0.000000],[+0.231049,0.000000]])
# labels = np.array([['A','B'],['C','D'],['E','F']])
# fig, ax = plt.subplots()
# ax = sns.heatmap(data, annot = labels, fmt = '')

# https://levelup.gitconnected.com/statistics-on-seaborn-plots-with-statannotations-2bfce0394c00
with sns.plotting_context('notebook', font_scale = 1.4):
    # Create new plot
    ax = get_log_ax()

    # Plot with seaborn
    sns.boxplot(**plotting_parameters)

    # Add annotations
    annotator = Annotator(ax, pairs, **plotting_parameters)
    annotator.set_pvalues(pvalues)
    annotator.annotate()

    # Label and show
    label_plot_for_subcats(ax)
    plt.show()

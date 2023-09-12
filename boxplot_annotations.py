import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from statannotations.Annotator import Annotator
from itertools import product
from lectura import leer_jamovi

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
pairs = [('ankle',    'R-R'), ('ankle',    'L-L'),
         ('subt',     'R-R'), ('subt',     'L-L'),
         ('knee',     'R-R'), ('knee',     'L-L'),
         ('hip_addu', 'R-R'), ('hip_addu', 'L-L'),
         ('hip_flex', 'R-R'), ('hip_flex', 'L-L'),
         ('hip_rot',  'R-R'), ('hip_rot',  'L-L'),

         ('ankle',    'R-L'), ('ankle',    'L-R'),
         ('subt',     'R-L'), ('subt',     'L-R'),
         ('knee',     'R-L'), ('knee',     'L-R'),
         ('hip_addu', 'R-L'), ('hip_addu', 'L-R'),
         ('hip_flex', 'R-L'), ('hip_flex', 'L-R'),
         ('hip_rot',  'R-L'), ('hip_rot',  'L-R'),
         ]

df_datos = pd.read_csv("sim05_medianas_realizaciones.csv")
CICLO = "swing"

hue_plot_params = {
    'data': df_datos,
    'x': 'angulo',
    'y': 'mediana',
    # "order": subcat_order,
    "hue": "lados",
    # "hue_order": states_order,
    # "palette": state_palette
}

with sns.plotting_context("notebook", font_scale = 1.4):
    # Create new plot
    fig, ax = plt.subplots(1, 1)

    # Plot with seaborn
    ax = sns.boxplot(ax=ax, **hue_plot_params)

    # Add annotations
    annotator = Annotator(ax, pairs, **hue_plot_params)
    annotator.configure(test="Mann-Whitney", verbose=False)
    _, results = annotator.apply_and_annotate()

    plt.show()

#####################################
#
# fig, axs = plt.subplots(2, 1, sharey=True, sharex=True)
# df_aux = df_datos[df_datos["ciclo"] == CICLO]
#
# # colaterales
# sns.boxplot(data=df_aux[(df_aux["lados"] == "R-R") | (df_aux["lados"] == "L-L")],
#             x="angulo", y='mediana',
#             hue="lados",
#             ax=axs[0])
#
# # contralaterales
# sns.boxplot(data=df_aux[(df_aux["lados"] == "R-L") | (df_aux["lados"] == "L-R")],
#             x="angulo", y='mediana',
#             hue="lados",
#             ax=axs[1])
#
# fig.suptitle(f"Resultados para ciclo {CICLO}", fontsize=20)
# axs[0].grid()
# axs[1].grid()
#
# annotator = Annotator(axs, pairs, ...)
#
# plt.show()
#
# # data = np.array([[0.000000,0.000000],[+0.231049,0.000000],[+0.231049,0.000000]])
# # labels = np.array([['A','B'],['C','D'],['E','F']])
# # fig, ax = plt.subplots()
# # ax = sns.heatmap(data, annot = labels, fmt = '')
#
# # https://levelup.gitconnected.com/statistics-on-seaborn-plots-with-statannotations-2bfce0394c00
# with sns.plotting_context('notebook', font_scale=1.4):
#     # Create new plot
#     ax = get_log_ax()
#
#     # Plot with seaborn
#     sns.boxplot(**plotting_parameters)
#
#     # Add annotations
#     annotator = Annotator(ax, pairs, **plotting_parameters)
#     annotator.set_pvalues(pvalues)
#     annotator.annotate()
#
#     # Label and show
#     label_plot_for_subcats(ax)
#     plt.show()

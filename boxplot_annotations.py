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

pairs = ([('ankle',    'R-R'), ('ankle',    'L-L')],
         [('subt',     'R-R'), ('subt',     'L-L')],
         [('knee',     'R-R'), ('knee',     'L-L')],
         [('hip_addu', 'R-R'), ('hip_addu', 'L-L')],
         [('hip_flex', 'R-R'), ('hip_flex', 'L-L')],
         [('hip_rot',  'R-R'), ('hip_rot',  'L-L')],

         [('ankle',    'R-L'), ('ankle',    'L-R')],
         [('subt',     'R-L'), ('subt',     'L-R')],
         [('knee',     'R-L'), ('knee',     'L-R')],
         [('hip_addu', 'R-L'), ('hip_addu', 'L-R')],
         [('hip_flex', 'R-L'), ('hip_flex', 'L-R')],
         [('hip_rot',  'R-L'), ('hip_rot',  'L-R')],
         )

df_datos = pd.read_csv("sim05_medianas_realizaciones.csv")
CICLO = "swing"
df_datos = df_datos[df_datos["ciclo"] == CICLO]

state_palette = sns.color_palette("YlGnBu", n_colors=4)
states_order = ["ankle", "subt", "knee", "hip_addu", "hip_flex", "hip_rot"]
subcat_order = ["R-R", "L-L", "R-L", "L-R"]

hue_plot_params = {
    'data': df_datos,
    'x': 'angulo',
    'y': 'mediana',
    "order": states_order,
    "hue": "lados",
    "hue_order": subcat_order,
    "palette": state_palette
}

with sns.plotting_context("notebook", font_scale=1.4):
    # Create new plot
    fig, ax = plt.subplots(1, 1)

    # Plot with seaborn
    ax = sns.boxplot(ax=ax, **hue_plot_params)

    # add_stat_annotation(ax, data=None, x='x', y='y', hue='hue',
    #                     box_pairs=[("A", "B"), ("C", "D")],
    #                     text_format='full', loc='inside', verbose=2,
    #                     test=None, pvalues=[0.01, 0.05], test_short_name='custom')

    # Add annotations
    annotator = Annotator(ax, pairs, **hue_plot_params)
    # annotator.configure(test="Mann-Whitney", comparisons_correction="bonferroni", text_format='star')  # verbose=False)
    _, results = annotator.apply_and_annotate()

    plt.grid()
    plt.title(f"Datos para el cilo {CICLO}")
    plt.show()

# https://levelup.gitconnected.com/statistics-on-seaborn-plots-with-statannotations-2bfce0394c00

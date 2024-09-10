import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statannotations.stats.StatTest
import statannotations
from statannotations.Annotator import Annotator

plt.rcParams["figure.figsize"] = (10, 8.19)  # values in inches

PHASES = ['full', 'swing', 'stance', 'nods']
FOOTS = ["rtoe", "ltoe"]
ANGLES = ['rankle',
          'rsubt',
          'rknee',
          'rhip-addu',
          'rhip-flex',
          'rhip-rot',
          'lankle',
          'lsubt',
          'lknee',
          'lhip-addu',
          'lhip-flex',
          'lhip-rot',
          ]

PAIRS = ([('ankle',    'R-R'), ('ankle',    'L-L')],
         [('subt',     'R-R'), ('subt',     'L-L')],
         [('knee',     'R-R'), ('knee',     'L-L')],
         [('hip-addu', 'R-R'), ('hip-addu', 'L-L')],
         [('hip-flex', 'R-R'), ('hip-flex', 'L-L')],
         [('hip-rot',  'R-R'), ('hip-rot',  'L-L')],

         [('ankle',    'R-L'), ('ankle',    'L-R')],
         [('subt',     'R-L'), ('subt',     'L-R')],
         [('knee',     'R-L'), ('knee',     'L-R')],
         [('hip-addu', 'R-L'), ('hip-addu', 'L-R')],
         [('hip-flex', 'R-L'), ('hip-flex', 'L-R')],
         [('hip-rot',  'R-L'), ('hip-rot',  'L-R')],
         )


# def box_plot_medianas(filename, ciclo, to_file=False):
#     df_datos = pd.read_csv(filename)
#     df_datos = df_datos[df_datos["ciclo"] == ciclo]
#
#     state_palette = sns.color_palette("tab10", n_colors=4)
#     states_order = ["ankle", "subt", "knee", "hip-addu", "hip-flex", "hip-rot"]
#     subcat_order = ["R-R", "L-L", "R-L", "L-R"]
#
#     hue_plot_params = {
#         'data': df_datos,
#         'x': 'angulo',
#         'y': 'mediana',
#         "order": states_order,
#         "hue": "lados",
#         "hue_order": subcat_order,
#         "palette": state_palette
#     }
#
#     with sns.plotting_context("notebook", font_scale=1.4):
#         # Create new plot
#         fig, ax = plt.subplots(1, 1)
#         ax.set_ylim([0, 1])
#
#         # Plot with seaborn
#         ax = sns.boxplot(ax=ax, **hue_plot_params)
#
#         # add_stat_annotation(ax, data=None, x='x', y='y', hue='hue',
#         #                     box_pairs=[("A", "B"), ("C", "D")],
#         #                     text_format='full', loc='inside', verbose=2,
#         #                     test=None, pvalues=[0.01, 0.05], test_short_name='custom')
#
#         # Add annotations
#         annotator = Annotator(ax, PAIRS, **hue_plot_params)
#         annotator.test = statannotations.stats.StatTest.StatTest.from_library("Mann-Whitney")
#         annotator.comparisons_correction = statannotations.stats.ComparisonsCorrection.ComparisonsCorrection("Bonferroni")
#         _, results = annotator.apply_and_annotate()
#
#         plt.grid()
#         plt.title(f"Datos para el ciclo {ciclo}")
#
#         if to_file:
#             plt.savefig(to_file)
#             plt.close()
#         else:
#             plt.show()
#
#     # https://levelup.gitconnected.com/statistics-on-seaborn-plots-with-statannotations-2bfce0394c00
#

def box_plot_medianas_separado(filename: str, ciclo: str, lateralidad: str, add_label: bool = True, to_file: str = False):
    df_datos = pd.read_csv(filename)
    df_datos = df_datos[df_datos["ciclo"] == ciclo]

    if lateralidad == "ipsilateral":
        df_datos = df_datos[((df_datos["lados"] == "L-L") | (df_datos["lados"] == "R-R"))]
        subcat_order = ["L-L", "R-R"]
        colors_dict = {'L-L': '#1f77b4', 'R-R': '#ff7f0e'}  # blue and orange

    elif lateralidad == "contralateral":
        df_datos = df_datos[((df_datos["lados"] == "R-L") | (df_datos["lados"] == "L-R"))]
        subcat_order = ["R-L", "L-R"]
        colors_dict = {'L-R': '#2ca02c', 'R-L': '#d62728'}  # green and red

    else:
        print("Not a valid description")
        return None

    # state_palette = sns.color_palette("tab10", n_colors=4)
    states_order = ["ankle", "knee", "hip-flex", "hip-rot", "hip-addu", "subt"]

    hue_plot_params = {
        'data': df_datos,
        'x': 'angulo',
        'y': 'mediana',
        "order": states_order,
        "hue": "lados",
        "hue_order": subcat_order,
        "palette": colors_dict
    }

    with sns.plotting_context("notebook", font_scale=1.4):
        # Create new plot
        plt.rcParams.update({'font.size': 18})
        fig, ax = plt.subplots(1, 1)
        fig.set_size_inches((7, 6))
        plt.subplots_adjust(left=0.1,
                            bottom=0.1,
                            right=0.95,
                            top=0.95,
                            wspace=0.4,
                            hspace=0.2)
        ax.set_ylim([0, 0.7])
        if ciclo == "nods":
            ax.set_ylim([0, 0.2])

        # Plot with seaborn
        ax = sns.boxplot(ax=ax, **hue_plot_params)
        ax.set(xlabel=None)

        if ciclo != "full":
            ax.get_legend().set_visible(False)
        if ciclo != "swing":
            ax.set(ylabel=None)

        # Add annotations
        pairs = PAIRS[:6] if lateralidad == "ipsilateral" else PAIRS[6:]
        annotator = Annotator(ax, pairs, **hue_plot_params)
        annotator.test = statannotations.stats.StatTest.StatTest.from_library("Mann-Whitney")
        annotator.comparisons_correction = statannotations.stats.ComparisonsCorrection.ComparisonsCorrection(
            "Bonferroni")
        _, results = annotator.apply_and_annotate()

        ax.tick_params(axis="x", labelrotation=35)
        plt.grid()
        plt.tight_layout()

        if to_file:
            plt.savefig(to_file)
            plt.close()
        else:
            plt.show()


if __name__ == "__main__":
    data_file = "sim06_medianas_realizaciones.csv"
    CICLO = "nods"

    output_file = f'../Documento Final/figuras resultados/{CICLO}.pdf'
    # box_plot_medianas(data_file, CICLO)  # , output_file)

    phase = "swing"
    lado = "ipsilateral"
    # box_plot_medianas_separado(data_file, phase, lado)

    for phase in PHASES:
        for lado in ["ipsilateral", "contralateral"]:
            output_file = f'../Documento Final/figuras resultados/{phase}_{lado[:4]}.pdf'
            box_plot_medianas_separado(data_file, phase, lado, to_file=output_file)


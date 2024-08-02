import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np


def leer_dataframe_test2(filename):
    df_data = pd.read_csv(filename)
    df_data = df_data[["angulo", "lateral", "angulo.1", "lateral.1", "pbonferroni"]]  # dataframe slicing
    df_data.rename(columns={'pbonferroni': 'p',
                            'lateral': 'lateral 1',
                            'angulo': 'angulo 1',
                            'lateral.1': 'lateral 2',
                            'angulo.1': 'angulo 2'},
                   inplace=True)
    return df_data


def generar_matriz(filename, outfile=None):
    data = leer_dataframe_test2(filename)

    data["IM1"] = data["angulo 1"] + ["-" + i[0] for i in data["lateral 1"]]
    data["IM2"] = data["angulo 2"] + ["-" + i[0] for i in data["lateral 2"]]
    data["Rechazo H_0"] = [True if i[0] == "<" else False for i in data["p"]]
    del data["angulo 1"], data["angulo 2"], data["lateral 1"], data["lateral 2"]

    data2 = data.copy()
    data2.rename(columns={'IM1': 'IM2',
                          'IM2': 'IM1'},
                 inplace=True)

    data["Rechazo H_0"] = [False if i[0] == "<" else True for i in data["p"]]

    data_total = pd.concat([data, data2])
    map_data = data_total.pivot_table(index="IM1", columns="IM2", values="Rechazo H_0", fill_value=1)
    mask = np.triu(np.ones_like(map_data, dtype=bool))

    # Graficacion
    plt.figure(figsize=(12, 8))
    palette = sns.color_palette("rocket", 3)
    ax = sns.heatmap(map_data, mask=mask, center=0, square=False,
                fmt='.2f', linewidths=.42, cmap=palette)  # , cbar=False)
    colorbar = ax.collections[0].colorbar
    colorbar.set_ticks([0.25, 0.75])
    colorbar.set_ticklabels(['no rechazo $H_0$', 'rechazo $H_0$'])

    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.95,
                        top=0.95,
                        wspace=0.4,
                        hspace=0.2)

    if outfile:
        plt.savefig(outfile)
        plt.close()
    else:
        plt.show()


def boxplot_comparativo(filename, ciclo, lado, to_file=None):
    df_data = pd.read_csv(filename)
    df_data = df_data[df_data["ciclo"] == ciclo]
    df_data = df_data[df_data["lateral"] == lado]

    states_order = ["ankle", "subt", "knee", "hip-addu", "hip-flex", "hip-rot"]

    if lado == "ipsilateral":
        palette = sns.color_palette("bright")
    elif lado == "contralateral":
        palette = sns.color_palette("pastel")
        # my_colors = ["#FF9AA2",
        #              "#FFB7B2",
        #              "#FFDAC1",
        #              "#E2F0CB",
        #              "#B5EAD7",
        #              "#C7CEEA"]

    hue_plot_params = {
        'data': df_data,
        'x': 'angulo',
        'y': 'mediana',
        "order": states_order,
    }

    sns.set_palette(palette)
    fig, ax = plt.subplots(1, 1)
    ax.set_ylim([0, 1])

    # Plot with seaborn
    sns.boxplot(ax=ax, **hue_plot_params)

    plt.grid()

    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.95,
                        top=0.95,
                        wspace=0.4,
                        hspace=0.2)

    if to_file:
        plt.savefig(to_file)
        plt.close()
    else:
        plt.show()


if __name__ == "__main__":
    # Agregamos etiqueta de lateralidad de IM
    # data = pd.read_csv("sim06_medianas_realizaciones.csv")
    # data["lateral"] = ["ipsilateral" if data.loc[i, "lados"] in ["L-L", "R-R"] else "contralateral" for i in range(len(data))]
    # data.to_csv("sim06_medianas_realizaciones_nuevo.csv")

    ciclo = "full"
    datafile = f"data06/segundo_statistics_sim06_{ciclo}.csv"
    output_file = f"data06/matriz_{ciclo}.pdf"

    generar_matriz(datafile)  # , output_file)

    # for ciclo in ['full', 'swing', 'stance', 'nods']:
    #     for lado in ["ipsilateral", "contralateral"]:
    #         # ciclo = "full"
    #         # lado = "contralateral"
    #         datafile = "sim06_medianas_realizaciones_nuevo.csv"
    #         output_file = f"data06/boxplot_final_{ciclo}_{lado}.pdf"
    #         boxplot_comparativo(datafile, ciclo, lado, output_file)

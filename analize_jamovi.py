import pandas as pd


def leer_pvalores(filename, to_file=False):
    df = pd.read_csv(filename)
    # Me quedo solo con las columnas que me interesan
    df = df[["lados1", "angulo1", "lados2", "angulo2", "p_bonferroni"]]
    df.rename(columns={'p_bonferroni': 'p',
                       'lados1': 'par 1',
                       'angulo1': 'angulo 1',
                       'lados2': 'par 2',
                       'angulo2': 'angulo 2'},
              inplace=True)

    # Separamos en comparaciones ipsilaterales y contralaterales
    ipsi = df[((df["par 1"] == "L-L") | (df["par 1"] == "R-R"))
              & ((df["par 2"] == "L-L") | (df["par 2"] == "R-R"))]
    contra = df[((df["par 1"] == "R-L") | (df["par 1"] == "L-R"))
                & ((df["par 2"] == "R-L") | (df["par 2"] == "L-R"))]

    # Separamos comparaciones que son entre mismos angulos
    ipsi = ipsi[ipsi["angulo 1"] == ipsi["angulo 2"]]
    contra = contra[contra["angulo 1"] == contra["angulo 2"]]

    # Agregamos etiqueta de tipo de comparacion
    ipsi["comparación"] = "ipsilateral"
    contra["comparación"] = "contralateral"

    df = pd.concat([ipsi, contra], ignore_index=True)

    # Aclaro si rechazo o no H0
    df["rechazo $H_0^1$"] = df["p"] < 0.001
    df.loc[df["rechazo $H_0^1$"], "rechazo $H_0^1$"] = "Sí"
    df.loc[df["rechazo $H_0^1$"] == False, "rechazo $H_0^1$"] = "No"

    if to_file:
        df.to_csv(to_file)

    return df


def leer_pvalores_2da_parte(filename, to_file=False):
    df = pd.read_csv(filename)
    # Me quedo solo con las columnas que me interesan
    df = df[["angulo", "lateral", "angulo.1", "lateral.1", "pbonferroni"]]
    df.rename(columns={'pbonferroni': 'p',
                       'lateral': 'lado 1',
                       'angulo': 'angulo 1',
                       'lateral.1': 'lado 2',
                       'angulo.1': 'angulo 2'},
              inplace=True)

    df["p numerico"] = [float(i) if i.replace('.', '', 1).isdigit() else 0 for i in df["p"]]
    df["rechazo $H_0^2$"] = df["p numerico"] < 0.001
    del df["p numerico"]

    if to_file:
        df.to_csv(to_file)

    return df

# def generate_sample_table(filename, angle, outfile):
#     df = pd.read_csv(filename)
#     # Me quedo solo con las columnas que me interesan
#     df = df[["lados1", "angulo1", "lados2", "angulo2", "Difference", "p_bonferroni"]]
#     df.rename(columns={'p_bonferroni': 'p',
#                        'lados1': 'par 1',
#                        'angulo1': 'angulo 1',
#                        'lados2': 'par 2',
#                        'angulo2': 'angulo 2',
#                        "Difference": "Diferencia"},
#               inplace=True)
#     filtered = df[df["angulo 1"] == angle]
#     filtered = filtered.sort_values(by=['par 1', 'angulo 2', 'par 2'], ignore_index=True)
#     filtered.to_csv(outfile)


if __name__ == "__main__":
    # for CICLO in ["full", "swing", "stance", "nods"]:
    #     in_file = f"./data06/statistics_sim06_{CICLO}.csv"
    #     out_file = f"../Documento Final/apendice2/stats_filtered_{CICLO}.csv"
    #     df = leer_pvalores(in_file, out_file)

    #generate_sample_table(in_file, "knee", "./data06/stats_knee_sim06_full.csv")

    for CICLO in ["full", "swing", "stance", "nods"]:
        in_file = f"./data06/segundo_statistics_sim06_{CICLO}.csv"
        out_file = f"../Documento Final/apendice2/segundo_anexo_{CICLO}.csv"
        df = leer_pvalores_2da_parte(in_file, out_file)


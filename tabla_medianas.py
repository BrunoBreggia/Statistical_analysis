import pandas as pd


df = pd.read_csv("../Statistical_analysis/sim06_medianas_realizaciones_nuevo.csv")
grouped = df.groupby(["ciclo", "angulo", "lateral"])["mediana"].median()
grouped.to_csv("mediana_de_medianas.csv")


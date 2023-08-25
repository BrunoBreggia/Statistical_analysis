# python script
import pandas as pd


def leer_jamovi(filename):
    with open(filename, "r", encoding="utf-8") as file:
        heading = file.readline()
        columns = [data.strip() for data in heading.split(",")]
        data = pd.DataFrame({
            col: [] for col in columns
        })
        counter = 0
        row = []
        while content := file.readline():
            if content not in "-\n":
                counter += 1
                if content[0] == "<":
                    content = "0.0009\n"
                row.append(content[:-1])
                if counter == len(columns):
                    data.loc[len(data)] = row
                    counter = 0
                    row.clear()
    return data


if __name__ == '__main__':
    df = leer_jamovi("data/statistics_sim05_nods")
    df.to_csv("data/statistics_sim05_nods.csv")

import pandas as pd
import os

from sklearn.preprocessing import LabelEncoder

class Dataset:
    
    def __init__(self, name, col_types = None):

        path = os.path.join("donnees", name + ".csv")
        if os.path.exists(path):
            with open(path, "r") as f:
                self.df = pd.read_csv(f)
        else:
            raise ValueError(f"nom de dataset invalide ({name})")

        if col_types is not None:
            self.col_types = col_types
        else:
            self.col_types = {"cat" : ['type_1', 'type_2'],
                              "num" : ['hp', 'atk', 'def', 'spa', 'spd', 'spe', 'status', 'power', 'coverage'],
                              "target" : "tier"}

        self.labeler = LabelEncoder()
        self.labeler.fit(self.df[self.target])


    @property
    def X(self):
        X_cols = self.cats + self.nums
        return self.df[X_cols]

    @property
    def y(self):
        return self.labeler.transform(self.df[self.target])

    def relabel(self, table):
        return self.labeler.inverse_transform(table)

    @property
    def nums(self):
        return self.col_types["num"]

    @property
    def cats(self):
        return self.col_types["cat"]

    @property
    def target(self):
        return self.col_types["target"]


if __name__ == "__main__":
    d = Dataset("dataset2")
    print(d.X)
    print(d.relabel(d.y))
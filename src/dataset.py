import pandas as pd
import os

from sklearn.preprocessing import LabelEncoder

class Dataset:
    """Une classe qui représente un dataset utilisé pour entrainer et tester les modèles"""
    
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
                              "num" : ['dex', 'hp', 'atk', 'def', 'spa', 'spd', 'spe', 'status', 'power', 'coverage'],
                              "target" : "tier"}

        self.labeler = LabelEncoder()
        self.labeler.fit(self.df[self.target])


    @property
    def X(self):
        """Les données d'entrée du dataset, à utiliser dans les prédictions"""
        X_cols = self.cats + self.nums
        return self.df[X_cols]

    @property
    def y(self):
        """La colonne cible du dataset, à utiliser afin d'entrainer et tester les modeles."""
        return self.labeler.transform(self.df[self.target])

    def relabel(self, table):
        """Méthode d'aide pour réétiqueter les tiers d'une liste"""
        return self.labeler.inverse_transform(table)

    @property
    def nums(self):
        """La liste des noms des colonnes indépendantes qui ont des données numériques"""
        return self.col_types["num"]

    @property
    def cats(self):
        """La liste des noms des colonnes indépendantes qui ont des données qualitatives"""
        return self.col_types["cat"]

    @property
    def target(self):
        """Le nom de la colonne cible"""
        return self.col_types["target"]

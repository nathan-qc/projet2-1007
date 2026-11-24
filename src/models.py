from abc import ABC, abstractmethod

from dataset import Dataset

import os

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss

import joblib

class Model(ABC):

    def __init__(self, d: Dataset):
        self.d = d

        # Généré à l'origine à l'aide de Claude
        # L'étape de preprocessing est la même pour tous les modèles
        self.pre = ColumnTransformer([
            ("num", StandardScaler(), d.nums),
            ("cat", OneHotEncoder(handle_unknown="ignore"), d.cats), # Encodage One-hot pour les types
        ])

        self.model = self._init_model()

    @abstractmethod
    def _init_model(self):
        """Retourne le modèle de scikit"""
        pass

    def benchmark(self):
        """Retourne une ligne des probabilités de chaque classification pour chaque pokemon, testé avec training/testing 80/20"""

        # Généré à l'origine à l'aide de Claude
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
        proba = cross_val_predict(self.model, self.d.X, self.d.y, cv=cv, method="predict_proba")

        return proba

    def plot(self):
        """Montre un graphique représentant la sortie du modèle"""

        proba = pd.DataFrame(self.benchmark())
        proba["tiers"] = self.d.y
        proba = proba.sort_values("tiers") # Trier afin que les lignes se regroupent par tier voulu

        plt.imshow(proba.drop("tiers", axis=1), aspect="auto")
        plt.colorbar(label='valeur')
        plt.show()

    def metrics(self):
        """Fait quelques évaluationss de performance du modèle"""
        proba = self.benchmark()

        # Généré à l'origine à l'aide de Claude
        onehot = np.eye(9)[self.d.y]
        proba_log_loss = log_loss(self.d.y, proba)
        proba_brier = np.mean(np.sum((proba - onehot) ** 2, axis=1))
        freqs = np.bincount(self.d.y) / len(self.d.y)
        log_loss_baseline = log_loss(self.d.y, np.tile(freqs, (len(self.d.y), 1)))


        return {"log_baseline": log_loss_baseline, "log": proba_log_loss, "brier": proba_brier}

    def dump(self, name: str):
        """Entraine une version finale du modele et la sauvegarde dans modeles/[name]"""
        self.model.fit(self.d.X, self.d.y)
        path = os.path.join("modeles", name + ".joblib")
        dict = {"model": self.model, "le": self.d.labeler}
        joblib.dump(dict, path)


class DumbPredictor(Model):
    """Un modèle trivial pour comparer le succès des autres"""

    def __init__(self, d: Dataset, params):
        super().__init__(d, params)


class LogisticReg(Model):
    """Un modèle de régression logistique"""

    def _init_model(self):
        # Généré à l'origine à l'aide de Claude
        return Pipeline([
            ("pre", self.pre),
            ("clf", LogisticRegression(C=1.0, max_iter=2000)),
        ])


class RandomForest(Model):
    """Un ensemble de modèles "arbre" afin de prendre la moyenne de ceux-ci"""

    def _init_model(self):
        # Généré à l'origine à l'aide de Claude
        base = Pipeline([
            ("pre", self.pre),
            ("clf", RandomForestClassifier(n_estimators=300, min_samples_leaf=3, random_state=0, max_depth=3)),
        ])
        return CalibratedClassifierCV(base, method="sigmoid", cv=5)


if __name__ == "__main__":
    d = Dataset("dataset2")
    l = LogisticReg(d)
    l.dump("logistic")
    f = RandomForest(d)
    f.dump("forest")

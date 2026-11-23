import sys
sys.path.append("src")
import os, json, pytest
from dataset import Dataset

def test_dataset_col_types():
    d = Dataset("dataset")
    assert d.col_types is not None

def test_dataset_nom_invalide():
    with pytest.raises(ValueError):
        d = Dataset("les_recettes_de_grand_maman")
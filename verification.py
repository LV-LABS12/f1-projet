import sqlite3
import pandas as pd

connexion = sqlite3.connect("f1.db")

print(pd.read_sql("SELECT COUNT(*) AS nb_lignes FROM resultats", connexion))
print(pd.read_sql(
    "SELECT saison, COUNT(DISTINCT manche) AS nb_courses FROM resultats GROUP BY saison",
    connexion))
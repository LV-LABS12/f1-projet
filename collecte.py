import time
import sqlite3
import requests
import pandas as pd

SAISONS = range(2014, 2026)   # de 2014 à 2025 inclus
LIMITE = 100                  # maximum autorisé par page

lignes = []                   # on va y ranger une ligne par résultat

for saison in SAISONS:
    offset = 0
    total = 1                 # valeur provisoire, mise à jour après le 1er appel

    while offset < total:
        url = f"https://api.jolpi.ca/ergast/f1/{saison}/results.json"
        reponse = requests.get(url, params={"limit": LIMITE, "offset": offset})
        reponse.raise_for_status()          # stoppe le script si l'API renvoie une erreur
        donnees = reponse.json()["MRData"]
        total = int(donnees["total"])       # nombre total de lignes de la saison

        for course in donnees["RaceTable"]["Races"]:
            for r in course["Results"]:
                lignes.append({
                    "saison": int(course["season"]),
                    "manche": int(course["round"]),
                    "grand_prix": course["raceName"],
                    "circuit_id": course["Circuit"]["circuitId"],
                    "circuit": course["Circuit"]["circuitName"],
                    "date": course["date"],
                    "pilote": r["Driver"]["familyName"],
                    "ecurie": r["Constructor"]["name"],
                    "grille": int(r["grid"]),
                    "arrivee": int(r["position"]),
                    "statut": r["status"],
                    "points": float(r["points"]),
                })

        offset += LIMITE
        time.sleep(1)                       # pause d'1 seconde pour respecter l'API

    print(f"Saison {saison} OK")

# Liste de dictionnaires -> tableau pandas -> table SQLite
tableau = pd.DataFrame(lignes)
connexion = sqlite3.connect("f1.db")
tableau.to_sql("resultats", connexion, if_exists="replace", index=False)
connexion.close()

print(len(tableau), "lignes enregistrées")

import sqlite3
import pandas as pd

connexion = sqlite3.connect("f1.db")

def requete(titre, sql):
    print("\n" + titre)
    print(pd.read_sql(sql, connexion).to_string(index=False))

requete("1. Départs sans vraie place de grille (grille = 0)",
        "SELECT COUNT(*) AS nb FROM resultats WHERE grille = 0")

requete("2. Les 8 statuts d'arrivée les plus fréquents",
        """SELECT statut, COUNT(*) AS nb
           FROM resultats
           GROUP BY statut
           ORDER BY nb DESC
           LIMIT 8""")

requete("3. Le 1er de la grille gagne-t-il ?",
        """SELECT COUNT(*) AS departs_en_1ere_position,
                  SUM(arrivee = 1) AS victoires,
                  ROUND(100.0 * SUM(arrivee = 1) / COUNT(*), 1) AS pourcentage
           FROM resultats
           WHERE grille = 1""")

requete("4. Taux de victoire selon la position de départ (1 à 5)",
        """SELECT grille,
                  COUNT(*) AS departs,
                  SUM(arrivee = 1) AS victoires,
                  ROUND(100.0 * SUM(arrivee = 1) / COUNT(*), 1) AS pourcentage
           FROM resultats
           WHERE grille BETWEEN 1 AND 5
           GROUP BY grille
           ORDER BY grille""")
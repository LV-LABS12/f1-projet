import sqlite3
import pandas as pd
import plotly.express as px

connexion = sqlite3.connect("f1.db")

# Même logique que la requête 4, étendue aux 10 premières places
tableau = pd.read_sql("""
    SELECT grille,
           ROUND(100.0 * SUM(arrivee = 1) / COUNT(*), 1) AS pourcentage
    FROM resultats
    WHERE grille BETWEEN 1 AND 10
    GROUP BY grille
    ORDER BY grille
""", connexion)

figure = px.bar(
    tableau,
    x="grille",
    y="pourcentage",
    text="pourcentage",
    title="Taux de victoire selon la position de départ (F1, 2014-2025)",
    labels={"grille": "Position sur la grille", "pourcentage": "Victoires (%)"},
)
figure.update_xaxes(dtick=1)             # une graduation par position

figure.write_html("graphique_grille.html")   # sauvegarde pour ton portfolio
figure.show()                                # ouvre le graphique dans le navigateur

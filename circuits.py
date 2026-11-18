import sqlite3
import pandas as pd
import plotly.express as px

connexion = sqlite3.connect("f1.db")

tableau = pd.read_sql("""
    SELECT MAX(circuit) AS circuit,
           COUNT(*) AS courses,
           SUM(arrivee = 1) AS poles_converties,
           ROUND(100.0 * SUM(arrivee = 1) / COUNT(*), 0) AS pourcentage
    FROM resultats
    WHERE grille = 1
    GROUP BY circuit_id
    HAVING COUNT(*) >= 8
    ORDER BY pourcentage ASC
""", connexion)

print(tableau.to_string(index=False))

figure = px.bar(
    tableau,
    x="pourcentage",
    y="circuit",
    orientation="h",
    text="pourcentage",
    hover_data=["courses", "poles_converties"],
    title="Part des courses gagnées par le 1er de la grille, par circuit (2014-2025)",
    labels={"pourcentage": "Pole convertie en victoire (%)", "circuit": ""},
    height=700,
)

figure.write_html("graphique_circuits.html")
figure.show()
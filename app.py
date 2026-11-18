import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="F1 : la pole fait-elle gagner ?", layout="wide")

ROUGE = "#E10600"
GRIS = "#6B6B76"
FOND = "#15151E"


def habiller(figure):
    figure.update_layout(
        template="plotly_dark",
        paper_bgcolor=FOND,
        plot_bgcolor=FOND,
        margin=dict(l=10, r=10, t=30, b=10),
    )
    figure.update_traces(textposition="outside")
    return figure


@st.cache_data                      # évite de relire la base à chaque interaction
def charger(sql, params=()):
    connexion = sqlite3.connect("f1.db")
    tableau = pd.read_sql(sql, connexion, params=params)
    connexion.close()
    return tableau


st.title("La pole position fait-elle gagner en Formule 1 ?")
st.write("Analyse de 252 Grands Prix (2014-2025). Données : API Jolpica-F1.")

# --- Partie 1 : selon la position de départ ---
st.header("1. L'effet de la position de départ")

grille = charger("""
    SELECT grille,
           ROUND(100.0 * SUM(arrivee = 1) / COUNT(*), 1) AS pourcentage
    FROM resultats
    WHERE grille BETWEEN 1 AND 10
    GROUP BY grille
    ORDER BY grille
""")

figure1 = px.bar(
    grille, x="grille", y="pourcentage", text="pourcentage",
    labels={"grille": "Position sur la grille", "pourcentage": "Victoires (%)"},
)
figure1.update_xaxes(dtick=1)
habiller(figure1)
figure1.update_traces(marker_color=[ROUGE] + [GRIS] * 9)   # seule la pole en rouge
st.plotly_chart(figure1)

# --- Partie 2 : selon le circuit ---
st.header("2. L'effet de la pole selon le circuit")

minimum = st.slider("Nombre minimum de courses par circuit", 5, 12, 8)

circuits = charger("""
    SELECT MAX(circuit) AS circuit,
           COUNT(*) AS courses,
           SUM(arrivee = 1) AS poles_converties,
           ROUND(100.0 * SUM(arrivee = 1) / COUNT(*), 0) AS pourcentage
    FROM resultats
    WHERE grille = 1
    GROUP BY circuit_id
    HAVING COUNT(*) >= ?
    ORDER BY pourcentage ASC
""", params=(minimum,))

figure2 = px.bar(
    circuits, x="pourcentage", y="circuit", orientation="h", text="pourcentage",
    hover_data=["courses", "poles_converties"],
    labels={"pourcentage": "Pole convertie en victoire (%)", "circuit": ""},
    height=650,
)
habiller(figure2)
figure2.update_traces(                                      # Monaco mis en avant
    marker_color=[ROUGE if "Monaco" in nom else GRIS for nom in circuits["circuit"]]
)
st.plotly_chart(figure2)

# --- Limites ---
st.header("Limites de l'analyse")
st.write(
    "Ces chiffres montrent une corrélation, pas une cause : la meilleure voiture "
    "se qualifie souvent en pole et gagne la course. Par circuit, l'échantillon "
    "est petit (12 courses au maximum), donc les écarts sont indicatifs."
)
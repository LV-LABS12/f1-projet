# La pole position fait-elle gagner en Formule 1 ?

Projet d'analyse de données réalisé pendant ma formation BTS SIO (SLAM).

## Pourquoi ce projet
(Écris ici 2 ou 3 phrases avec tes mots : ta passion pour la F1, ce que tu voulais comprendre.)

## Question
Partir en pole position garantit-il la victoire ? L'effet varie-t-il selon les circuits ?

## Résultats clés
- Le 1er de la grille gagne 53,6 % des courses (135 sur 252).
- La 2e place tombe à 23,5 %, la 3e à 10,7 %.
- Environ 93 % des victoires viennent des cinq premières places de la grille.
- Par circuit, l'effet varie de 25 % à 92 %. Monaco (55 %) reste proche de la moyenne, ce qui contredit mon hypothèse de départ.

## Méthode
1. Collecte des résultats 2014-2025 via l'API Jolpica-F1 (Python, requests)
2. Stockage dans une base SQLite
3. Analyse avec SQL et Pandas
4. Visualisation avec Plotly et dashboard Streamlit

## Limites
Corrélation n'est pas causalité : la meilleure voiture obtient souvent la pole et gagne la course. Par circuit, l'échantillon est petit (12 courses au maximum), les écarts sont donc indicatifs.

## Lancer le projet
```
pip install -r requirements.txt
streamlit run app.py
```

## Source des données
API Jolpica-F1 (successeur d'Ergast).
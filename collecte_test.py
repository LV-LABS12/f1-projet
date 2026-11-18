import requests

# Adresse de l'API : saison 2023, course n°1, résultats
url = "https://api.jolpi.ca/ergast/f1/2023/1/results.json"

reponse = requests.get(url)        # on envoie la demande
donnees = reponse.json()           # on transforme la réponse en dictionnaire Python

# On descend dans la structure pour atteindre la course
course = donnees["MRData"]["RaceTable"]["Races"][0]
print(course["raceName"])

# On affiche les 5 premiers : pilote, position de départ, position d'arrivée
for resultat in course["Results"][:5]:
    print(resultat["Driver"]["familyName"], resultat["grid"], resultat["position"])
#!/usr/bin/env python3
import sys
import re
import csv

# re pour recuperer l'année entre parenthèses dans le titre
year_pattern = re.compile(r'\((\d{4})\)$')

# lire le fichier csv
reader = csv.reader(sys.stdin)

for row in reader:
    try:
        # sauter les lignes vides
        if len(row) < 3: continue 
        
        # les colonnes de la csv
        movie_id = row[0] 
        title_raw = row[1].strip()
        genres = row[2] 

        # ne pas prendre la premire ligne 
        if movie_id == 'movieId': continue

        # prendre l'année du titre 
        match = year_pattern.search(title_raw)
        if match:
            year = match.group(1) 
            # enlève l'année du titre pour le nettoyer
            title_clean = title_raw.replace(f'({year})', '').strip()
        else:
            year = "0000" # pas d'année trouvée
            title_clean = title_raw 

        # affichage des resultats apres : ID  Titre  Année  Genres
        print(f"{movie_id}\t{title_clean}\t{year}\t{genres}")
        
    except Exception:
        continue
import pandas as pd
import requests
import time
import csv
import os

# configuration api
api_key = "CLE_API"
base_url = "https://api.themoviedb.org/3/movie/"
image_base_url = "https://image.tmdb.org/t/p/w500"
output_file = "descriptions_api_tmdb.csv"

# chargement des ids depuis links.csv
links_df = pd.read_csv("links.csv")
links_df = links_df.dropna(subset=['tmdbId'])
links_df['tmdbId'] = links_df['tmdbId'].astype(int) 

# definition des colonnes du fichier de sortie
columns = [
    "tmdb_id", "description", "tmdb_url", "cover_url",  
    "vote_average", "vote_count", "original_language", "popularity" 
]

# creation du fichier csv avec l'en-tete
if not os.path.exists(output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL) 
        writer.writerow(columns)

print("demarrage de l'extraction...")

# ouverture du fichier en mode ajout
with open(output_file, mode='a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL) 

    # boucle sur chaque film
    for index, row in links_df.iterrows():
        tmdb_id = row['tmdbId']
        
        # construction de l'url api 
        url = f"{base_url}{tmdb_id}?api_key={api_key}&language=fr-FR" 
        
        try:
            # appel reel a l'api
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                # extraction des donnees
                description = data.get('overview', '') 
                poster_path = data.get('poster_path') 
                cover_url = f"{image_base_url}{poster_path}" if poster_path else ""
                vote_avg = data.get('vote_average', 0)
                vote_cnt = data.get('vote_count', 0) 
                lang = data.get('original_language', 'en')
                pop = data.get('popularity', 0)
                tmdb_url = f"https://www.themoviedb.org/movie/{tmdb_id}" 

                # ecriture de la ligne dans le csv
                writer.writerow([
                    tmdb_id,
                    description,
                    tmdb_url,
                    cover_url,
                    vote_avg,
                    vote_cnt,
                    lang,
                    pop
                ])
                
                print(f"succes id {tmdb_id}")
            
            # pause pour respecter les limites de l'api
            time.sleep(0.2)

        except Exception as e:
            print(f"erreur id {tmdb_id}: {e}")

print("terminé")
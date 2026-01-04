# Projet Big Data : Cinema Trends (Hadoop, Hive & NLP)

**Etudiant :** Bademba SANGARE
**Formation :** M1 Informatique & Big Data - Universite Paris 8
**Module :** Cadre Logiciel pour le Big Data
**Date de rendu :** 05 Janvier 2026

## Description du Projet
Ce projet a ete realise dans le cadre du module "Cadre Logiciel pour le Big Data". Il consiste a developper une architecture distribuee repondant a un besoin reel d'analyse de tendances (inspire des "Recaps" YouTube/Spotify). L'application traite le dataset MovieLens enrichi via l'API TMDB pour fournir des statistiques et un moteur de recommandation de films base sur le contenu (NLP).

## Acces au Projet (Deploye sur le Cloud)
L'application est actuellement hebergee et fonctionnelle sur le cluster GCP. Aucune installation n'est necessaire pour la tester.

* **Application en ligne (Dashboard) :** http://34.121.158.103:8501/
* **Video de demonstration :** https://www.youtube.com/watch?v=Y4SRKIWIckA
* **Depot GitHub (Code source) :** https://github.com/badembafr/projet_hadoop_cinema_trends_nlp_sangare

## Conformite avec le Sujet
Ce projet repond a l'ensemble des criteres demandes :
1. **Besoin reel :** Analyse de tendances et systeme de recommandation (Use case "Cinema Trends").
2. **Technologies Hadoop :** Utilisation complete de la stack :
   * **HDFS :** Stockage distribue des donnees CSV et enrichies.
   * **YARN :** Gestion des ressources du cluster.
   * **MapReduce :** Traitement via les jobs lances par Hive.
   * **Hive :** Brique analytique pour les aggregations et KPIs.
3. **Cluster Reel (Cloud) :** Deploiement sur Google Cloud Platform (Compute Engine) avec 3 nœuds (1 Master, 2 Slaves).
4. **Analyse & IA :** Scripts HiveQL pour les statistiques et Python (Scikit-learn) pour la partie NLP.


## Contenu du Livrable
L'archive ZIP est structuree pour repondre aux attendus du rendu Moodle :

projet_hadoop_cinema_trends_nlp_sangare/
|
|-- 1_Rapport_Video-lien_Presentation/     <-- (Livrable: Rapport PDF + Video)
|   |-- LIEN_VIDEO_YOUTUBE.txt
|   |-- miniature_video_youtube.png
|   |-- Presentation_Projet_Cinema_Trends_SANGARE.pdf
|   |-- Rapport_Projet_Cinema_Trends_SANGARE.pdf
|
|-- 2_Code_Source_data-hive-python-dashboard/  <-- (Livrable: Scripts Hive, Python & Donnees)
|   |-- 00_Donnees_Brutes/
|   |   |-- descriptions_api_tmdb.csv
|   |   |-- links.csv
|   |   |-- movies.csv
|   |   |-- ratings.csv
|   |
|   |-- 01_Enrichissement_Donnees/
|   |   |-- descriptions_api_tmdb.csv
|   |   |-- links.csv
|   |   |-- mapper.py
|   |   |-- requirements.txt
|   |   |-- tmdb_scraper_descriptions.py
|   |
|   |-- 02_Hive_MapReduce/
|   |   |-- requetes_analyse.hql           <-- (Les requetes HQL demandees)
|   |
|   |-- 03_Dashboard_Streamlit/
|   |   |-- dashboard_tendances_movies_nlp.py
|   |   |-- requirements.txt
|
|-- 3_Captures_Execution_Requete_Hive/     <-- (Preuves de fonctionnement sur Cluster)
    |-- 10_reussite_dl_yarn_slave1.png
    |-- 13_map_reduce_mapper_movies.png
    |-- 16_dashboard_web.png
    |-- 17_les_3_instances_hadoop_gcp.png
    |-- ... (Autres captures d'ecran configuration/execution)

## Note sur l'Architecture Technique
Le Dashboard Streamlit (Python) execute sur le nœud Master agit comme une interface de visualisation. Il est important de noter qu'il ne traite pas les fichiers bruts : il consomme exclusivement les resultats agreges produits par les traitements Hive et MapReduce stockes dans HDFS, validant ainsi l'architecture distribuee du projet.
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# configuration page
st.set_page_config(
    page_title="Analyse de Tendances Cinématographiques + Recommandations de films", 
    layout="wide",
    page_icon="🎬" 
)

# en-tete projet
with st.container():
    col_logo, col_text = st.columns([1, 5])
    with col_text:
        st.title("🎬 Analyse de Tendances Cinématographiques + Recommandations de films") 
        st.markdown("### 🏛️ Université Paris 8 - Master Informatique & Big Data") 
        st.markdown("**Étudiant :** Bademba SANGARÉ | **Module :** Cadre Logiciel pour le Big Data")
        
        # info infrastructure gcp
        st.info("☁️ Infrastructure Google Cloud : Cluster Hadoop de 3 Machines Virtuelles (1 Master + 2 Slaves) | Config : 2 vCPU, 8 Go RAM par nœud")

    st.markdown("---")

# fonction chargement hive
def load_data(folder_name, col_names, sep=','):
    base_path = "/home/sangarebademba_mail/"
    path = os.path.join(base_path, folder_name)
    try:
        files = os.listdir(path)
        # selection fichier resultat
        target_file = [f for f in files if f.startswith("0000")][0]
        full_path = os.path.join(path, target_file)
        return pd.read_csv(full_path, names=col_names, header=None, sep=sep)
    except Exception:
        return pd.DataFrame()

# section kpis
col1, col2, col3 = st.columns(3)
df_kpi_movies = load_data("resultats_kpi_movies", ["total_films"])
df_kpi_ratings = load_data("resultats_kpi_ratings", ["total_votes", "avg_rating"])

# affichage catalogue
with col1:
    if not df_kpi_movies.empty:
        st.metric("🎞️ Catalogue de Films", f"{df_kpi_movies['total_films'].iloc[0]:,}")
# affichage votes
with col2:
    if not df_kpi_ratings.empty:
        st.metric("👥 Votes Traités", f"{df_kpi_ratings['total_votes'].iloc[0]:,}")
# affichage moyenne
with col3:
    if not df_kpi_ratings.empty:
        val = df_kpi_ratings['avg_rating'].iloc[0]
        st.metric("⭐ Note Moyenne Globale", f"{val:.2f} / 5") 

st.markdown("---")

# section top 10
st.subheader("🏆 Top 10 des Films les Mieux Notés (> 50 votes)") 
# chargement donnees
df_top10 = load_data("resultats_top10", ["Titre", "Genres", "Note Moyenne", "Nombre de Votes"], sep='\t')

if not df_top10.empty:
    df_top10["Note Moyenne"] = df_top10["Note Moyenne"].round(2)
    st.dataframe(df_top10, use_container_width=True)
else:
    st.warning("Données Top 10 non disponibles.") 

st.markdown("---")

# section graphiques
c1, c2 = st.columns(2)

# camembert genres
with c1:
    st.subheader("🍕 Répartition des Genres")
    df_genres = load_data("resultats_genres", ["Genre", "Nombre"])
    if not df_genres.empty:
        fig_pie = px.pie(df_genres, values='Nombre', names='Genre', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

# histogramme users
with c2:
    st.subheader("🥇 Utilisateurs les plus actifs") 
    df_users = load_data("resultats_users", ["UserId", "Votes"])
    if not df_users.empty: 
        df_users["UserId"] = "User " + df_users["UserId"].astype(str)
        fig_bar = px.bar(df_users, x='Votes', y='UserId', orientation='h')
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# section analyse temporelle
st.subheader("📈 Analyse Temporelle")
tab1, tab2 = st.tabs(["Production Annuelle", "Activité des Votes"]) 

# courbe production
with tab1:
    df_evo_films = load_data("resultats_evolution_films", ["Année", "Nombre de Films"])
    if not df_evo_films.empty:
        st.line_chart(df_evo_films.set_index("Année")) 

# histogramme votes
with tab2:
    df_evo_votes = load_data("resultats_evolution_votes", ["Année", "Nombre de Votes"])
    if not df_evo_votes.empty:
        st.bar_chart(df_evo_votes.set_index("Année"))

st.markdown("---")

# section recommandation ia
st.header("🤖 Recommandations & Affiches (IA)") 
st.info("Ce module utilise l'analyse sémantique (NLP) des résumés pour trouver des films similaires.")

# chargement donnees enrichies
@st.cache_data
def load_enhanced_data():
    try:
        base_dir = "/home/sangarebademba_mail/ml-latest-small/" 
        df_movies = pd.read_csv(os.path.join(base_dir, "movies.csv"))
        df_links = pd.read_csv(os.path.join(base_dir, "links.csv"))
        df_tmdb = pd.read_csv(os.path.join(base_dir, "descriptions_api_tmdb.csv"))
        
        # fusion fichiers
        df_merged = pd.merge(df_movies, df_links, on='movieId', how='inner')
        df_final = pd.merge(df_merged, df_tmdb, left_on='tmdbId', right_on='tmdb_id', how='inner')
        # nettoyage description
        df_final['description'] = df_final['description'].fillna('')
        return df_final
    except Exception:
        return pd.DataFrame() 

df_ia = load_enhanced_data()

if not df_ia.empty:
    # vectorisation tf-idf
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_ia['description'])
    
    # similarite cosinus
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    
    # index films
    indices = pd.Series(df_ia.index, index=df_ia['title_x']).drop_duplicates()

    # liste films
    movie_list = sorted(df_ia['title_x'].unique()) 
    
    # spider-man par defaut
    default_film = "Spider-Man (2002)"
    try:
        # recherche index
        default_index = movie_list.index(default_film)
    except ValueError:
        # sinon premier film
        default_index = 0

    # selection film
    selected_movie = st.selectbox("🎥 Choisissez un film que vous avez aimé :", movie_list, index=default_index)

    # bouton lancement
    if st.button("Lancer la recommandation"):
        try:
            # recup index film
            idx = indices[selected_movie]
            if isinstance(idx, pd.Series): idx = idx.iloc[0]

            # calcul scores
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            # top 5 resultats
            sim_scores = sim_scores[1:6]
            
            st.success(f"Suggestions pour : **{selected_movie}**") 
            
            # affichage resultats
            cols = st.columns(5)
            for i, (movie_idx, score) in enumerate(sim_scores):
                row = df_ia.iloc[movie_idx]
                title = row['title_y']
                img_url = row['cover_url']
                # troncature description 
                desc = row['description'][:130] + "..." if len(row['description']) > 130 else row['description']
                
                with cols[i]:
                    # affichage image
                    if pd.notna(img_url) and img_url.startswith("http"):
                        st.image(img_url)
                    else:
                        st.write("🖼️ (Pas d'image)")
                    
                    st.markdown(f"**{title}**")
                    with st.expander("Résumé"):
                        st.write(desc)

        except Exception as e:
            st.error(f"Erreur sur ce film : {e}")

else:
    st.warning("⚠️ Fichiers pour l'IA manquants.")
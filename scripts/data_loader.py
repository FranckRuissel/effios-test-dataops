import pandas as pd
import requests
import os
import io
import logging

# Configuration du logger pour le suivi en console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_dnma_data():
    """
    Charge les données DNMA. 
    la priorité au fichier en local sinon on tente l'API si une clé est présente.
    """
    csv_local = "fr-en-dnma-par-uai-appareils.csv"
    api_key = os.environ.get("API_KEY")

    # On tente d'abord le local (plus rapide pour le testeur)
    if os.path.exists(csv_local):
        logger.info(f"Fichier local détecté : {csv_local}")
        try:
            # low_memory=False est crucial pour les gros CSV je l'utilise sur Mac afin d'éviter les erreurs de buffer
            df = pd.read_csv(csv_local, sep=';', low_memory=False)
            logger.info("Chargement des données locales réussi.")
            return prepare_data(df)
        except Exception as e:
            logger.error(f"Erreur lors de la lecture du CSV local : {e}")
            # Si le local échoue, on ne s'arrête pas, on essaiera l'API après

    # tentative via l'API si la clé est présente dans le .env
    if api_key:
        logger.info("Tentative de récupération des données via l'API...")
        url = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-dnma-par-uai-appareils/exports/csv"
        headers = {
            "Authorization": f"Apikey {api_key}",
            "Content-Type": "application/json"
        }
        try:
            # Timeout à 30s pour l'API
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                logger.info("Données récupérées avec succès via l'API.")
                df = pd.read_csv(io.StringIO(response.text), sep=';', low_memory=False)
                return prepare_data(df)
            else:
                logger.warning(f"L'API a répondu avec l'erreur {response.status_code}.")
        except Exception as e:
            logger.error(f"Erreur lors de l'appel API : {e}")

    logger.error("Échec critique : Aucune source de données disponible.")
    return None

def prepare_data(df):
    """
    Nettoyage et formatage des données pour l'analyse.
    """
    # Nettoyage des noms de colonnes (enlève les espaces éventuels)
    df.columns = df.columns.str.strip()

    # Conversion de la date
    if 'debutSemaine' in df.columns:
        df['debutSemaine'] = pd.to_datetime(df['debutSemaine'], errors='coerce')
        # On retire les lignes où la date n'est pas valide
        df = df.dropna(subset=['debutSemaine'])
        df['annee'] = df['debutSemaine'].dt.year
    
    # Conversion forcée en numérique pour les colonnes de visites
    visite_cols = [c for c in df.columns if 'visites_' in c]
    for col in visite_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    return df
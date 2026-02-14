
import os
import logging
from dotenv import load_dotenv
from scripts.data_loader import load_dnma_data
from scripts.analysis import DNMAnalysis

# Configuration du logging pour un suivi propre en console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    # 1. Chargement des variables pour l'API_KEY)
    load_dotenv()
    
    logger.info("Démarrage du programme d'analyse DNMA...")

    # 2. Récupération des données la logique ici est hybride API / Local 
    df = load_dnma_data()
    
    if df is None or df.empty:
        logger.error("Impossible de continuer : aucune donnée chargée.")
        return

    # 3. Initialisation de la classe d'analyse ici on passe le DataFrame une seule fois pour optimiser les performances
    analysis = DNMAnalysis(df)

    print("\n" + "="*50)
    print(" RÉSULTATS DES EXPRESSIONS DE BESOINS (EB)")
    print("="*50)

    # EB1 : Top 3 semaines pour l'UAI 0010024W en 2025 
    print("\n[EB1] - Top 3 semaines (Visites) pour 0010024W en 2025 :")
    top_3 = analysis.eb1_top_3_weeks("0010024W", 2025)
    print(top_3)

    # EB2 : Agrégation par UAI et Granularité par mois 
    print("\n[EB2] - Agrégation mensuelle pour l'UAI 0010024W :")
    agreg = analysis.eb2_aggregate("0010024W", "Mois")
    print(agreg)

    # EB3 : Graphique d'évolution 
    print("\n[EB3] - Génération du graphique d'évolution par appareil...")
    analysis.eb3_plot_evolution("0010024W", 2025)

    # EB4 : Fonctionnalité libre je teste une mobilité par Académie
    print("\n[EB4] - Analyse Bonus : Top 5 Académies 'Mobile First' (Ratio d'usage) :")
    bonus = analysis.eb4_mobile_first_index()
    print(bonus.head(5))

    print("\n" + "="*50)
    logger.info("Fin de l'exécution du test pratique.")

if __name__ == "__main__":
    main()
import pandas as pd
import matplotlib.pyplot as plt

class DNMAnalysis:
    """
    Classe pour analyser les données de visites.
    """

    def __init__(self, df: pd.DataFrame):
        # On garde les données en mémoire dans l'objet
        self.df = df
############ EB1 ###########
    def eb1_top_3_weeks(self, uai: str, annee: int):
        """
        EB1: Trouve les 3 meilleures semaines pour un établissement.
        """
        # On garde seulement l'établissement et l'année demandés
        filtre = self.df[(self.df['UAI'] == uai) & (self.df['annee'] == annee)].copy() 
        if filtre.empty:
            return "Aucune donnée trouvée."
            
        # On calcule le total des visites (ordinateur + smartphone + tablette)
        filtre['Nb Visites'] = (filtre['visites_ordinateur'] + 
                                filtre['visites_smartphone'] + 
                                filtre['visites_tablette']+
                               filtre['visites_autreappareil'])
        
        # On récupère le numéro de la semaine
        filtre['Semaine'] = filtre['debutSemaine'].dt.isocalendar().week
        
        # On prend les 3 lignes avec le plus grand nombre de visites
        top_3 = filtre.nlargest(3, 'Nb Visites')[['Semaine', 'Nb Visites']]
        return top_3
    
########### EB2 ################
    def eb2_aggregate(self, uai: str, granularite: str):
        """
        EB2: Additionne les visites par Mois ou par Année.
        """
        # On filtre sur l'établissement
        filtre = self.df[self.df['UAI'] == uai].copy()
        
        # On choisit si on groupe par mois ou par année, cette approche est a revoir 
        if granularite.lower() == "mois":
            filtre['Periode'] = filtre['debutSemaine'].dt.strftime('%Y-%m')
        else:
            filtre['Periode'] = filtre['annee']
            
        # Colonnes à additionner
        cols = ['visites_ordinateur', 'visites_smartphone', 'visites_tablette','visites_autreappareil']
        
        # On fait le calcul total par période
        return filtre.groupby('Periode')[cols].sum()

################## EB3 ################
    def eb3_plot_evolution(self, uai: str, annee: int):
        """
        EB3: Affiche un graphique de l'évolution des visites.
        """
        # On filtre les données
        filtre = self.df[(self.df['UAI'] == uai) & (self.df['annee'] == annee)].copy()
        filtre['mois'] = filtre['debutSemaine'].dt.month
        
        # On groupe les données par mois
        evol = filtre.groupby('mois')[['visites_ordinateur', 'visites_smartphone', 'visites_tablette']].sum()
        
        # Création du graphique
        evol.plot(kind='line', marker='o', figsize=(10, 6))
        plt.title(f"Visites par appareil - {uai} ({annee})")
        plt.xlabel("Mois")
        plt.ylabel("Nombre de visites")
        plt.grid(True)
        plt.legend(["Ordinateur", "Smartphone", "Tablette"])
        plt.show()
        
    ################### EB4 ###################
    def eb4_mobile_first_index(self):
        """
        EB4: Calcule la part d'utilisation des mobiles par Académie.
        """
        # On groupe tout par académie et on fait la somme
        df_acad = self.df.groupby('académie').sum(numeric_only=True)
        
        # Calcul du total global
        df_acad['total'] = (df_acad['visites_ordinateur'] + 
                            df_acad['visites_smartphone'] + 
                            df_acad['visites_tablette'])
        
        # Calcul du pourcentage (ratio) mobile + tablette
        df_acad['mobile_ratio'] = (df_acad['visites_smartphone'] + df_acad['visites_tablette']) / df_acad['total']
        
        # On trie du plus grand au plus petit
        return df_acad[['mobile_ratio']].sort_values(by='mobile_ratio', ascending=False)

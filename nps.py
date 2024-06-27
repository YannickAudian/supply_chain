import pandas as pd
import matplotlib.pyplot as plt

# Charger les données à partir du chemin correct
file_path = '/mnt/data/cleaned_trustpilot_reviews.csv'
df = pd.read_csv(file_path)

# Convertir la colonne date en datetime
df['date'] = pd.to_datetime(df['date'])

# Vérifier les valeurs uniques de rating
print(df['rating'].unique())

# Extraire le mois et l'année
df['month'] = df['date'].dt.to_period('M')

# Calculer le NPS pour chaque mois avec des impressions intermédiaires
def calculate_nps(df):
    promoters = df[df['rating'] >= 9].shape[0]
    detractors = df[df['rating'] <= 6].shape[0]
    total_responses = df.shape[0]
    print(f"Month: {df['month'].iloc[0]}, Promoters: {promoters}, Detractors: {detractors}, Total: {total_responses}")
    if total_responses == 0:
        return 0
    nps = ((promoters - detractors) / total_responses) * 100
    return nps

monthly_nps = df.groupby('month').apply(calculate_nps).reset_index(name='NPS')

# Tracer le graphique
plt.figure(figsize=(10, 6))
plt.plot(monthly_nps['month'].astype(str), monthly_nps['NPS'], marker='o')
plt.title('Net Promoter Score (NPS) by Month')
plt.xlabel('Month')
plt.ylabel('NPS')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Afficher le graphique
plt.show()

import ace_tools as tools; tools.display_dataframe_to_user(name="Monthly NPS", dataframe=monthly_nps)

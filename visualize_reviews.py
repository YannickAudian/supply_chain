import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# Charger les données depuis le fichier CSV
df = pd.read_csv("trustpilot_reviews.csv")

# Convertir la colonne 'date' en format datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Ajouter une colonne 'satisfied' si 'rating' existe
df['satisfied'] = df['rating'].apply(lambda x: 1 if x >= 4 else 0)

# Supprimer les doublons
df = df.drop_duplicates(subset=['title', 'body'], keep='first')

# Réorganiser les catégories
def categorize_review(body):
    body = body.lower()
    if "livre" in body or "book" in body:
        return "Books"
    elif "aliment" in body or "food" in body:
        return "Food"
    elif "vêtement" in body or "clothes" in body:
        return "Clothing"
    else:
        return "Uncategorized"

df['category'] = df['body'].apply(categorize_review)

# Analyser les sentiments
def analyze_sentiment(body):
    polarity = TextBlob(body).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity == 0:
        return "Neutral"
    else:
        return "Negative"

df['sentiment'] = df['body'].apply(analyze_sentiment)

# Distribution des avis par catégorie de produit
category_distribution = df['category'].value_counts()
print("Category distribution:")
print(category_distribution)

# Distribution des avis par sentiment
sentiment_distribution = df['sentiment'].value_counts()
print("Sentiment distribution:")
print(sentiment_distribution)

# Visualisation de la distribution des avis par catégorie de produit
plt.figure(figsize=(10, 6))
category_distribution.plot(kind='bar', color='skyblue')
plt.title('Distribution des avis par catégorie de produit')
plt.xlabel('Catégorie de produit')
plt.ylabel('Nombre d\'avis')
plt.xticks(rotation=45)
plt.show()

# Visualisation de l'analyse des sentiments par catégorie
sentiment_category_distribution = df.groupby(['category', 'sentiment']).size().unstack().fillna(0)
sentiment_category_distribution.plot(kind='bar', stacked=True, figsize=(10, 6), color=['red', 'grey', 'green'])
plt.title('Analyse des sentiments par catégorie de produit')
plt.xlabel('Catégorie de produit')
plt.ylabel('Nombre d\'avis')
plt.xticks(rotation=45)
plt.legend(title='Sentiment', loc='upper right')
plt.show()

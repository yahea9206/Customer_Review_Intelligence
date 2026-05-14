# ============================================================
# TOPIC CLUSTERING SECTION
# Customer Review Intelligence System
# ============================================================

# ============================================================
# IMPORTS
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from collections import Counter
from wordcloud import WordCloud

import warnings
warnings.filterwarnings('ignore')


# ============================================================
# PREPARE TEXT DATA
# ============================================================

# Make sure your cleaned review column exists
# Replace 'cleaned_review' with your actual cleaned text column name if different

reviews = df['cleaned_review'].dropna()

print("Total Reviews Used for Clustering:", len(reviews))


# ============================================================
# TF-IDF VECTORIZATION WITH BIGRAMS
# ============================================================

# IMPORTANT:
# Requirement specifically asked for bigram features

vectorizer = TfidfVectorizer(
    max_features=3000,
    stop_words='english',
    ngram_range=(1, 2),
    min_df=5,
    max_df=0.8
)

X_tfidf = vectorizer.fit_transform(reviews)

print("TF-IDF Matrix Shape:", X_tfidf.shape)


# ============================================================
# ELBOW METHOD TO FIND BEST K
# ============================================================

inertia_values = []
k_range = range(2, 11)

for k in k_range:
    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
)
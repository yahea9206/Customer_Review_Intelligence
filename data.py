import os
import pandas as pd
import numpy as np
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
    print("matplotlib is not installed; plotting will be skipped.")

# ── Load Real Amazon Reviews Dataset ──────────────────────────────────────────
# Download the "Amazon Fine Food Reviews" or similar dataset from Kaggle
# Ensure the CSV is in the same folder as this notebook

if os.path.exists('Reviews.csv'):
    print("Found 'Reviews.csv'. Loading real dataset...")
    df_raw = pd.read_csv('Reviews.csv')
    # Sample 10,000 reviews to keep the notebook fast during the live presentation
    df = df_raw.sample(n=10000, random_state=42).reset_index(drop=True)
    
    # Rename columns to match the rest of our notebook's pipeline
    df = df.rename(columns={'Text': 'review_text', 'Score': 'rating', 'Time': 'review_date'})
    
    # Convert Unix timestamp to a readable datetime format for time-series analysis
    if 'review_date' in df.columns:
        df['review_date'] = pd.to_datetime(df['review_date'], unit='s')
        
    print(f"Loaded {len(df)} real reviews successfully!\n")
else:
    print("⚠️ WARNING: 'Reviews.csv' not found. Using generated sample data for testing.")
    print("⚠️ ACTION REQUIRED: Download Amazon dataset from Kaggle before final presentation!\n")
    
    import random
    random.seed(42)
    np.random.seed(42)
    
    sample_reviews = [
        "Fast shipping arrived next day great delivery service",
        "Late delivery package was damaged when it arrived",
        "Amazing product high quality material very durable",
        "Poor quality broke after one week very disappointed",
        "Great value for money very affordable highly recommend",
        "Too expensive for what you get overpriced product",
        "Customer service was amazing solved my issue quickly",
        "Horrible support waited two weeks no reply"
    ]
    reviews_list = []
    ratings_list = []
    dates_list = []
    base_date = pd.to_datetime('2023-01-01')
    
    for i in range(500):
        base = random.choice(sample_reviews)
        if any(w in base for w in ['great', 'amazing', 'excellent', 'fast', 'good']): 
            rating = random.choice([4, 5])
        else:
            rating = random.choice([1, 2])
        reviews_list.append(base)
        ratings_list.append(rating)
        dates_list.append(base_date + pd.Timedelta(days=random.randint(0, 365)))
        
    df = pd.DataFrame({'review_text': reviews_list, 'rating': ratings_list, 'review_date': dates_list})

# ── Basic checks ──────────────────────────────────────────────────────────────
print(f'Total reviews loaded: {len(df)}')
print(f'Missing values: {df.isnull().sum().sum()}')
df.head(3)                                                                                                                                                    # ── EDA (Exploratory Data Analysis) — understand the data before processing ───
print('Rating distribution (how many reviews per star):')
print(df['rating'].value_counts().sort_index())

# Bar chart of rating counts
plt.figure(figsize=(7, 4))
df['rating'].value_counts().sort_index().plot(kind='bar', color=['#e74c3c','#e67e22','#f1c40f','#2ecc71','#27ae60'], edgecolor='black')
plt.title('Star Rating Distribution', fontsize=14)
plt.xlabel('Star Rating')
plt.ylabel('Number of Reviews')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
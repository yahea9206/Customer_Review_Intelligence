
# Import Libraries

import pandas as pd
import re
import nltk

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer

# تحميل ملفات nltk

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')


# Load Dataset


df = pd.read_csv("/reviews.csv")


print(df.columns)

df = df[['reviewText', 'overall', 'sentiment_label']]

df.dropna(inplace=True)

# Text Cleaning

def clean_text(text):

    text = str(text).lower()

    text = re.sub(r'\d+', '', text)

    text = re.sub(r'[^\w\s]', '', text)

    text = text.strip()

    return text


df['clean_text'] = df['reviewText'].apply(clean_text)

# Tokenization

df['tokens'] = df['clean_text'].apply(word_tokenize)

# Stopwords Removal

stop_words = set(stopwords.words('english'))

def remove_stopwords(words):

    filtered_words = []

    for word in words:
        if word not in stop_words:
            filtered_words.append(word)

    return filtered_words

df['filtered_tokens'] = df['tokens'].apply(remove_stopwords)

# Convert Tokens To Text

df['final_text'] = df['filtered_tokens'].apply(
    lambda words: " ".join(words)
)

# TF-IDF + Bigram

vectorizer = TfidfVectorizer(
    max_features=3000,
    ngram_range=(1,2)
)

X = vectorizer.fit_transform(df['final_text'])

# Results

print("\nTF-IDF Matrix Shape:")
print(X.shape)

print("\nFirst 20 Features:")
print(vectorizer.get_feature_names_out()[:20])

print("\nProcessed Data:")
print(df[['reviewText', 'final_text', 'sentiment_label']].head())

# Sentiment Analysis Code

import pandas as pd
import numpy as np
import re
import nltk
import matplotlib.pyplot as plt

from textblob import TextBlob

from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.model_selection import train_test_split

from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from wordcloud import WordCloud

nltk.download('stopwords')

df = pd.read_csv("reviews.csv")

print("\nFirst 5 Rows:\n")
print(df.head())

df = df.dropna(subset=['reviewText'])

stop_words = set(stopwords.words('english'))

def clean_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z\s]', '', text)

    words = text.split()

    words = [word for word in words if word not in stop_words]

    return " ".join(words)

df["Cleaned_Review"] = df["reviewText"].apply(clean_text)

def get_sentiment(text):

    analysis = TextBlob(text)

    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return "Positive"

    elif polarity < 0:
        return "Negative"

    else:
        return "Neutral"

df["Sentiment"] = df["Cleaned_Review"].apply(get_sentiment)

print("\nSample Results:\n")

print(df[["reviewText", "Sentiment"]].head())

print("\nSentiment Distribution:\n")

print(df["Sentiment"].value_counts())

X = df["Cleaned_Review"]

y = df["Sentiment"]

vectorizer = TfidfVectorizer(max_features=5000)

X_vectorized = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(

    X_vectorized,
    y,

    test_size=0.2,

    random_state=42
)

model = MultinomialNB()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:\n")

print(accuracy)

print("\nClassification Report:\n")

print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)

display = ConfusionMatrixDisplay(

    confusion_matrix=cm,

    display_labels=model.classes_
)

display.plot()

plt.title("Confusion Matrix")

plt.show()

sentiment_counts = df["Sentiment"].value_counts()

plt.figure(figsize=(6,6))

plt.pie(

    sentiment_counts,

    labels=sentiment_counts.index,

    autopct='%1.1f%%'
)

plt.title("Sentiment Distribution")

plt.show()

plt.figure(figsize=(6,5))

df["Sentiment"].value_counts().plot(kind='bar')

plt.title("Sentiment Count")

plt.xlabel("Sentiment")

plt.ylabel("Count")

plt.show()

all_words = " ".join(df["Cleaned_Review"])

wordcloud = WordCloud(

    width=800,

    height=400,

    background_color='white'

).generate(all_words)

plt.figure(figsize=(12,6))

plt.imshow(wordcloud)

plt.axis("off")

plt.title("Most Frequent Words")

plt.show()

df.to_csv("sentiment_results.csv", index=False)

print("\nResults Saved Successfully!")
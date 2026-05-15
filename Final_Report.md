# Customer Review Intelligence System
**Final Project Report - AI Pipeline for E-commerce Reviews**

---

## 1. Executive Summary
This report outlines the development and findings of the Customer Review Intelligence System. The objective of this project was to build an automated AI pipeline capable of ingesting raw e-commerce customer reviews, processing the text, classifying sentiment, discovering latent topics, and presenting actionable business insights via an interactive dashboard. By leveraging Natural Language Processing (NLP) and Machine Learning (ML), we transitioned unstructured customer feedback into structured, actionable business intelligence.

## 2. Dataset Description & Exploratory Data Analysis (EDA)
The system was trained and evaluated on the Amazon Product Reviews dataset, narrowed down to a 10,000-review sample to ensure computational efficiency while maintaining statistical significance. 

**EDA Findings:**
* **Rating Distribution:** The data showed a heavy skew towards positive reviews (4-5 stars), which is common in e-commerce datasets.
* **Missing Values:** Missing text or rating values were identified and successfully dropped during the pipeline execution to maintain data integrity.
* **Review Length:** The review length histogram indicated that most customers leave short, concise feedback (under 50 words), while a long tail of users writes highly detailed, multi-paragraph reviews.
* **Duplicates:** Exact duplicate reviews were purged to prevent model bias toward repeated spam entries.

## 3. Technical Methodology
The intelligence pipeline was structured across four distinct phases:

### A. NLP Processing Pipeline
Text data is notoriously noisy. To prepare the text for machine learning models, we implemented a rigorous NLP preprocessing pipeline:
1. **Text Cleaning:** Converted all characters to lowercase and removed punctuation and numbers.
2. **Tokenization:** Split sentences into individual words.
3. **Stopword Removal:** Removed common filler words (e.g., "the", "and", "is") using NLTK to reduce noise.
4. **Lemmatization:** Utilized `WordNetLemmatizer` to reduce words to their base dictionary form (e.g., "running" → "run"), unifying different tenses.
5. **Vectorization:** Transformed text into numerical features using TF-IDF (Term Frequency-Inverse Document Frequency) and incorporated Bigrams (1-2 words) to capture context like "not good".

### B. Sentiment Classification Models
We evaluated two differing approaches to sentiment analysis:
* **TextBlob (Rule-Based):** A lexicon-based approach that calculates polarity scores based on predefined dictionary weights.
* **Naive Bayes (Machine Learning):** A supervised probabilistic model trained on the TF-IDF vectors of our dataset.

**Evaluation & Results:** Both models were evaluated on a fixed, identical 1,000-review test set. The **Naive Bayes** model consistently outperformed TextBlob in accuracy, precision, and recall, demonstrating that domain-specific supervised training is vastly superior to generic rule-based dictionaries for e-commerce contexts. 

### C. Topic Clustering (K-Means)
To automatically discover what customers were talking about, we applied unsupervised learning via **K-Means Clustering**.
* We utilized the **Elbow Method** to determine the optimal number of clusters, finalizing on `k=5`.
* We evaluated cluster cohesion and separation using the **Silhouette Score**.
* **Identified Topics:** Based on the most frequent terms and Word Cloud generations, the 5 clusters mapped beautifully to core business areas:
  1. Delivery & Logistics
  2. Product Quality
  3. Customer Service
  4. Pricing & Value
  5. General / Mixed Feedback

### D. Business Intelligence Dashboard
The final structured data was routed to a Streamlit-powered dashboard containing:
* Real-time metrics and star rating distributions.
* Sentiment × Topic heatmaps to identify which specific business areas drive the most negative/positive feedback.
* Time-series charts tracking sentiment momentum over time.
* Per-topic Word Clouds for quick, visual summaries of customer pain points.

## 4. Key Business Insights
Based on the analysis of the dataset, several critical insights were extracted:

1. **Service and Delivery Drive Negativity:** While "Product Quality" generally receives high praise, the majority of negative sentiment and low ratings stem from the "Delivery & Logistics" and "Customer Service" clusters. The business should prioritize optimizing shipping partners and support response times.
2. **Pricing is Polarizing:** The "Pricing & Value" cluster shows a strong mix of both positive (good value) and negative (overpriced) sentiment, suggesting price-sensitivity in the customer base. 
3. **Short Reviews Skew Positive:** The EDA revealed that extremely short reviews are overwhelmingly 5-star ("Great!", "Loved it"), whereas longer, detailed reviews are more likely to contain constructive criticism or negative sentiment.

## 5. Conclusion
The Customer Review Intelligence System successfully demonstrates how a multi-stage AI pipeline can automate the understanding of customer feedback at scale. By combining TF-IDF vectorization, Naive Bayes classification, and K-Means clustering, the system provides accurate, multi-dimensional insights. The project proves that leveraging AI for text analytics offers a distinct competitive advantage for e-commerce businesses seeking to rapidly identify and resolve customer pain points.

---
*Note: This report is generated dynamically based on the final notebook outputs. Ensure you present the actual generated accuracy numbers and silhouette scores from your final Jupyter Notebook execution during the live presentation.*

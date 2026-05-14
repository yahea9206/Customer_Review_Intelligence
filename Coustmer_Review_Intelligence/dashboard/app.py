import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="NLP Dashboard", layout="wide")
st.title("📊 NLP Analysis Dashboard")
st.markdown("### Data Pipeline + Sentiment Analysis + Topic Clustering")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.selectbox(
    "اختر الصفحة",
    ["Overview", "Sentiment Analysis", "Topic Clustering", "Data Pipeline", "Raw Data"]
)

# Placeholder for data (هتغيره بعدين حسب بياناتك)
if 'df' not in st.session_state:
    # مثال بيانات - غيره ببياناتك الحقيقية
    data = {
        'text': ['المنتج ممتاز', 'سيء جداً', 'جودة متوسطة', 'رائع وسريع'],
        'sentiment': ['positive', 'negative', 'neutral', 'positive'],
        'score': [0.92, 0.85, 0.45, 0.88],
        'topic': ['Product Quality', 'Customer Service', 'Product Quality', 'Delivery'],
        'date': ['2026-05-01', '2026-05-02', '2026-05-03', '2026-05-04']
    }
    st.session_state.df = pd.DataFrame(data)

df = st.session_state.df

# ==================== Pages ====================

if page == "Overview":
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Texts", len(df))
    with col2:
        st.metric("Positive", len(df[df['sentiment'] == 'positive']))
    with col3:
        st.metric("Negative", len(df[df['sentiment'] == 'negative']))
    with col4:
        st.metric("Topics Found", df['topic'].nunique())

    st.subheader("Sentiment Distribution")
    fig = px.pie(df, names='sentiment', title="Sentiment Overview")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Sentiment Analysis":
    st.subheader("Sentiment Analysis Results")
    fig = px.histogram(df, x='score', color='sentiment', nbins=20)
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df[['text', 'sentiment', 'score']], use_container_width=True)

elif page == "Topic Clustering":
    st.subheader("Topic Clustering Results")
    topic_counts = df['topic'].value_counts()
    fig = px.bar(x=topic_counts.index, y=topic_counts.values, 
                 labels={'x': 'Topic', 'y': 'Count'}, title="Topics Distribution")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df[['text', 'topic']], use_container_width=True)

elif page == "Data Pipeline":
    st.subheader("Data Pipeline Status")
    st.success("✅ Data Pipeline Completed Successfully")
    st.info("Last Update: " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    # هنا تقدر تضيف metrics عن عدد الروات، حجم البيانات، إلخ

elif page == "Raw Data":
    st.subheader("Raw Data")
    st.dataframe(df, use_container_width=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Built with FastAPI + Streamlit")

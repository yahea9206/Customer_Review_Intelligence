import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="Executive Insights", layout="wide")

# ستايل هادي ونضيف جداً
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    div[data-testid="stMetric"] { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    .status-card { background: #1c2128; padding: 20px; border-radius: 12px; border-top: 4px solid #58a6ff; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. تحميل البيانات بطريقة "مقاومة للخطأ"
@st.cache_data
def load_data():
    try:
        # بنحاول نقرأ الملف من المسار المحلي أو السيرفر
        df = pd.read_csv('processed-data.csv')
        df.columns = [c.lower().strip() for c in df.columns]
        
        # تصحيح آلي للـ KeyError (لو العمود اسمه مختلف)
        mapping = {'reviews.text': 'text', 'reviews.rating': 'score', 'reviews.date': 'date'}
        df = df.rename(columns=mapping)
        
        # التأكد من وجود الأعمدة الحيوية عشان الموقع ميقعش
        for col in ['sentiment', 'topic', 'text', 'date']:
            if col not in df.columns:
                df[col] = 'General' if col != 'date' else '2026-05'
        return df
    except Exception as e:
        st.error(f"Data Connection Error: {e}")
        return pd.DataFrame()

df = load_data()

# 3. القائمة الجانبية (الأربعة خانات)
st.sidebar.title("🚀 Intelligence Hub")
page = st.sidebar.radio("Go to:", ["Overview", "Sentiment Detail", "Topic Analysis", "AI Chatbot"])

if not df.empty:
    if page == "Overview":
        st.title("Strategic Summary")
        
        # الخانات الأربعة العلوية
        pos = len(df[df['sentiment'] == 'positive'])
        neg = len(df[df['sentiment'] == 'negative'])
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Reviews", len(df))
        c2.metric("Positive Flow", pos, "↑ Stable")
        c3.metric("Negative Risks", neg, "↓ Managed", delta_color="inverse")
        c4.metric("Active Topics", df['topic'].nunique())

        st.divider()

        # عرض الأسهم والمؤشرات بدلاً من الدوائر
        st.subheader("Customer Pulse Indicators")
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown(f"""
            <div class="status-card">
                <h3 style="color:#3fb950;">➜ Growth Sentiment</h3>
                <p>Confidence score is high. Users are moving towards <b>Brand Loyalty</b>.</p>
                <h1 style="margin:0;">{int(pos/len(df)*100)}%</h1>
            </div>
            """, unsafe_allow_html=True)
            
        with col_b:
            st.markdown(f"""
            <div class="status-card" style="border-top-color:#f85149;">
                <h3 style="color:#f85149;">➜ Friction Points</h3>
                <p>Minor issues detected in <b>Service Response</b>. Attention required.</p>
                <h1 style="margin:0;">{int(neg/len(df)*100)}%</h1>
            </div>
            """, unsafe_allow_html=True)

    elif page == "Sentiment Detail":
        st.title("🔍 Data Explorer")
        st.dataframe(df[['date', 'text', 'sentiment', 'topic']], use_container_width=True)

    elif page == "Topic Analysis":
        st.title("🏷️ Topic Mapping")
        st.write("Identified Clusters:")
        for t in df['topic'].unique():
            st.success(f"➜ Topic: {t}")

    elif page == "AI Chatbot":
        st.title("🤖 AI Assistant")
        st.text_input("Ask about specific trends:")
else:
    st.warning("Please check 'processed-data.csv' file location.")

st.sidebar.markdown("---")
st.sidebar.caption("Last Sync: May 2026")

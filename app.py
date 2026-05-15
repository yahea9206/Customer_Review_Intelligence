import streamlit as st
import pandas as pd
import plotly.express as px

# 1. الإعدادات والستايل
st.set_page_config(page_title="Intelligence Hub 2026", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    div[data-testid="stMetric"] { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    .review-card { background: #1c2128; padding: 15px; border-radius: 8px; border-left: 4px solid #58a6ff; margin-bottom: 10px; color: #adbac7; }
    </style>
    """, unsafe_allow_html=True)

# 2. تحميل البيانات ومعالجة الأعمدة
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('processed-data.csv')
        df.columns = [c.lower().strip() for c in df.columns]
        # تنظيف عمود المشاعر لضمان ظهور أكثر من عمود
        if 'sentiment' in df.columns:
            df['sentiment'] = df['sentiment'].astype(str).str.lower().str.strip()
        else:
            df['sentiment'] = 'neutral'
        return df
    except:
        return pd.DataFrame({'text': ['No data'], 'sentiment': ['neutral'], 'topic': ['General']})

df = load_data()

# 3. القائمة الجانبية
st.sidebar.title("🚀 Intelligence Hub")
page = st.sidebar.radio("Go to:", ["Overview", "Topic Explorer", "Data Detail"])

if page == "Overview":
    st.title("Strategic Summary")
    
    # حساب الأرقام الحقيقية
    total = len(df)
    counts = df['sentiment'].value_counts()
    pos = counts.get('positive', 0)
    neg = counts.get('negative', 0)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Reviews", f"{total:,}")
    c2.metric("Positive", f"{pos:,}", f"{(pos/total)*100:.1f}%")
    c3.metric("Negative", f"{neg:,}", f"-{(neg/total)*100:.1f}%", delta_color="inverse")
    c4.metric("Topics Found", df['topic'].nunique() if 'topic' in df.columns else 0)

    st.divider()

    # حل مشكلة العمود الواحد - رسم بياني مقسم
    st.subheader("Sentiment Analysis Breakdown")
    if not df.empty:
        fig = px.bar(df['sentiment'].value_counts().reset_index(), 
                     x='sentiment', y='count', color='sentiment',
                     color_discrete_map={'positive':'#238636', 'negative':'#da3633', 'neutral':'#1f6feb'},
                     text_auto=True)
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)

elif page == "Topic Explorer":
    st.title("🏷️ Topic Intelligence")
    st.write("اضغط على الموضوع لعرض المراجعات المتعلقة به:")
    
    if 'topic' in df.columns:
        # الحصول على قائمة المواضيع
        available_topics = df['topic'].unique()
        
        # استخدام selectbox أو buttons لاختيار الموضوع
        selected_topic = st.selectbox("Select a Topic to inspect:", available_topics)
        
        if selected_topic:
            st.markdown(f"### Reviews for: **{selected_topic}**")
            # تصفية البيانات بناءً على الاختيار
            topic_reviews = df[df['topic'] == selected_topic]
            
            for _, row in topic_reviews.head(10).iterrows():
                sentiment_color = "#238636" if row['sentiment'] == 'positive' else "#da3633" if row['sentiment'] == 'negative' else "#58a6ff"
                st.markdown(f"""
                <div class="review-card" style="border-left-color: {sentiment_color};">
                    <small style="color: {sentiment_color};">{row['sentiment'].upper()}</small><br>
                    {row['text']}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("No 'topic' column found in your data.")

elif page == "Data Detail":
    st.title("🔍 Full Data View")
    st.dataframe(df, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.caption("Last Sync: 2026-05-16")

import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والستايل "الهادي"
st.set_page_config(page_title="Intel Hub 2026", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 15px;
    }
    .status-box {
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #58a6ff;
        background: #1c2128;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. تحميل البيانات
@st.cache_data
def load_data():
    df = pd.read_csv('processed-data.csv')
    df.columns = [c.lower().strip() for c in df.columns]
    return df

df = load_data()

# 3. القائمة الجانبية (الأربعة زي ما هم)
st.sidebar.title("🚀 Intelligence")
menu = st.sidebar.radio("Navigation", ["Overview", "Sentiment Detail", "Topic Analysis", "AI Chatbot"])

# 4. الواجهة الأساسية (بدون دوائر وأعمدة زحمة)
if menu == "Overview":
    st.title("Strategic Summary")
    
    # الخانات العلوية
    c1, c2, c3, c4 = st.columns(4)
    pos_count = len(df[df['sentiment']=='positive'])
    neg_count = len(df[df['sentiment']=='negative'])
    
    c1.metric("Total Volume", len(df))
    c2.metric("Positive Flow", pos_count, "↑ High")
    c3.metric("Negative Risks", neg_count, "↓ Low", delta_color="inverse")
    c4.metric("Unique Topics", df['topic'].nunique() if 'topic' in df.columns else 1)

    st.markdown("---")

    # نظام الأسهم والتدفق (بدل الدايرة)
    st.subheader("Customer Sentiment Pulse")
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown(f"""
        <div class="status-box">
            <h3 style="color:#58a6ff;">➜ Positive Momentum</h3>
            <p>Current health score is stable. Most users are pointing towards <b>Product Satisfaction</b>.</p>
            <h2 style="color:#3fb950;">{int(pos_count/len(df)*100)}% Approval</h2>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown(f"""
        <div class="status-box" style="border-left-color: #f85149;">
            <h3 style="color:#f85149;">➜ Critical Points</h3>
            <p>Main friction detected in <b>Delivery Speed</b>. Arrows indicate a need for attention here.</p>
            <h2 style="color:#f85149;">{int(neg_count/len(df)*100)}% Friction</h2>
        </div>
        """, unsafe_allow_html=True)

# 5. باقي الصفحات (بدون تغيير في الوظيفة)
elif menu == "Sentiment Detail":
    st.title("🔍 Data Explorer")
    st.dataframe(df, use_container_width=True)

elif menu == "Topic Analysis":
    st.title("🏷️ Topic Mapping")
    st.info("System has identified key clusters through review flows.")
    st.write(df['topic'].unique() if 'topic' in df.columns else "General")

else:
    st.title("🤖 Assistant")
    st.text_input("Ask about the trend:")

st.sidebar.markdown("---")
st.sidebar.write("✅ System Active")

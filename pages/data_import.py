import streamlit as st
import pandas as pd

st.set_page_config(page_title="Import data", layout="centered")

# ---------- CSS partagé ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');
    body {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #3a1c71);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        font-family: 'Space Grotesk', sans-serif;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .big-title {
        font-size: 3.2rem;
        font-weight: 700;
        text-align: center;
        color: rgba(255, 255, 255, 0.95);
        text-shadow: 0 0 25px rgba(0, 230, 118, 0.4);
        margin: 2rem 0;
        letter-spacing: -1px;
    }
    .stButton>button {
        font-size: 1.1rem;
        padding: 0.8rem 2.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #00e676 0%, #00bcd4 100%);
        color: black;
        border: none;
        transition: all 0.4s ease;
    }
</style>
""", unsafe_allow_html=True)

# ---------- State init ----------
if "df_uploaded" not in st.session_state:
    st.session_state.df_uploaded = False
if "df" not in st.session_state:
    st.session_state.df = None

# ---------- UI ----------
st.markdown('<div class="big-title">Import your data</div>', unsafe_allow_html=True)
csv = st.file_uploader("Upload your CSV file", type="csv")

if csv is not None:
    try:
        st.session_state.df_uploaded = False
        st.session_state.df = None

        df = pd.read_csv(csv, low_memory=False)
        for col in df.columns:
            df[col] = df[col].apply(lambda x: None if isinstance(x, type) else x)

        df = df.convert_dtypes()
        for col in df.select_dtypes(include="number").columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        for col in df.columns:
            if df[col].dtype == "object" and "id" not in col.lower() and "index" not in col.lower():
                unique_types = df[col].apply(type).unique()
                if all(t in [str, type(None)] for t in unique_types):
                    df[col] = df[col].astype("string")

        if "PassengerId" in df.columns:
            df["PassengerId"] = pd.to_numeric(df["PassengerId"], errors="coerce").astype("Int64")


        st.session_state.df = df
        st.session_state.df_uploaded = True
        st.success("File uploaded successfully!")

    except Exception as e:
        st.error(f"Error reading file: {e}")

# ---------- Navigation ----------
if st.session_state.df_uploaded:
    if st.button("Continue to Data info"):
        st.switch_page("pages/data_info.py")

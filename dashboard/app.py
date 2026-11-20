"""Dashboard dos indicadores. Rode: streamlit run dashboard/app.py"""
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://estudo:estudo@localhost:5432/indicadores")


@st.cache_data(ttl=600)
def carregar():
    return pd.read_sql("SELECT * FROM marts.indicadores_mensais ORDER BY mes", engine)


st.set_page_config(page_title="Inflação e Juros", layout="wide")
st.title("Inflação e Juros no Brasil")
st.caption("Fonte → API do Banco Central. Pipeline: extract → PostgreSQL → dbt → Streamlit")

df = carregar()
ultimo = df.iloc[-1]

c1, c2, c3 = st.columns(3)
c1.metric("IPCA do mês", f"{ultimo['ipca']:.2f}%")
c2.metric("IPCA 12 meses", f"{ultimo['ipca_12m']:.2f}%")
c3.metric("Selic do mês", f"{ultimo['selic']:.2f}%")

st.subheader("IPCA acumulado em 12 meses")
st.line_chart(df, x="mes", y="ipca_12m")

st.subheader("Selic x IPCA no mês")
st.line_chart(df, x="mes", y=["selic", "ipca"])

with st.expander("Ver tabela"):
    st.dataframe(df)

import streamlit as st
from processamento import analisar_coordenada

st.set_page_config(page_title="Análise de Furo", page_icon="🧪")

st.title("🔍 Análise de Coordenada para Furo")
st.markdown("Insira uma coordenada (X, Y) no sistema SIRGAS 2000 / UTM zona 23S (EPSG:31983):")

x = st.number_input("🟦 Coordenada X (Easting)", format="%.2f")
y = st.number_input("🟩 Coordenada Y (Northing)", format="%.2f")

if st.button("Analisar"):
    with st.spinner("Processando análise..."):
        resultado = analisar_coordenada(x, y)

        st.success("✅ Análise concluída!")
        st.markdown(f"**📍 Grupo:** `{resultado['Grupo']}`")
        st.markdown(f"**📊 Status:** `{resultado['Status']}`")

        st.markdown("### 🧾 Interseções encontradas:")
        for campo, valor in resultado['campos'].items():
            emoji = "✅" if valor == "Sim" else "❌"
            st.markdown(f"- {campo.capitalize()}: {emoji}")
